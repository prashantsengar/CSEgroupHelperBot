import os
from telethon import TelegramClient, events, types, custom, utils, errors
import logging
logging.basicConfig(filename="log.txt", filemode="w")
import shelve

import download
import classr

# Dict to store Class IDs to Hashtags(hashtags are used for
# better search within a group)
HASHTAGS = {
    "56280784232": "#SE",
    "56103600610": "#NLP",
    "56147130005": "#DIP",
    "56147166362": "#ADBMS",
}

BOT_TOKEN = os.getenv("tok")
API_ID = int(os.getenv("id"))
API_HASH = os.getenv("hash")

GROUP_ID = int(os.getenv("group"))

bot = TelegramClient("grouphelper", API_ID, API_HASH)

file = None


@bot.on(events.NewMessage(GROUP_ID, pattern="/get", forwards=False))
async def help_handler(event):
    sent = 0
    shelf = shelve.open("classes")

    for CID in HASHTAGS:
        logging.info(f"Getting for {CID}")
        if not CID in shelf:
            logging.info(f"{CID} not in shelf")
            shelf[CID] = set()
            shelf.close()
            shelf = shelve.open("classes")

        ans = classr.get_announcements(CID)

        for ann in ans[::-1]:
            if ann["id"] in shelf[CID]:
                logging.debug("Already posted")
                continue
            else:
                logging.debug(f'Saving {ann["id"]} in shelf')
                shelf[CID].add(ann["id"])
                shelf.close()
                shelf = shelve.open("classes")

            try:
                text = ann["text"]
            except:
                text = ""
            files = []
            for i in ann["materials"]:
                try:
                    file = download.get_file(i["driveFile"]["driveFile"]["id"])
                    file.name = i["driveFile"]["driveFile"]["title"]
                    file.seek(0)
                    files.append(file)
                except KeyError:
                    logging.debug("Key not found")
                    print(i)
                    try:
                        URL = i["link"]["url"]
                        text = f"{text}\n{URL}"
                    except KeyError:
                        logging.debug("No URL found")
            text = f'{text}\n{ann["alternateLink"]}\nUpdate time: {ann["updateTime"]}\n\n#DigitalClass {HASHTAGS[CID]}'
            print(text, files)
            text_m = await event.reply(message=text)
            sent += 1
            for file in files:
                await text_m.reply(file=file)
                sent += 1
            logging.debug("replied")

    await event.reply("No new updates")
    raise events.StopPropagation


@bot.on(events.NewMessage())
async def start_handler(event):
    await event.reply("This bot currently only works in IIIT CSE (Official) Group")


bot.start(bot_token=BOT_TOKEN)
print("started")
bot.run_until_disconnected()
