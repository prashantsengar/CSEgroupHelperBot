# CSEgroupHelperBot
Group helper bot for my class of IIIT Una CSE 2017

This is a Telegram bot which downloads posts and attachments from Google Classroom and posts them to the class Telegram group.
It works only in the given Telegram group.

## Running on your local machine
- Clone the repo on your local machine 

`git clone https://github.com/prashantsengar/CSEgroupHelperBot.git`

- Change your current working directory 

`cd CSEgroupHelperBot`

- Activate your Google classroom API (of the account which has access to the classroom) and download the JSON credential file and name it as 'credentials.json'

- Run classr.py 

`python3 classr.py`

- Activate your Google drive API (of the account which has access to the classroom) and download the JSON credential file and name it as 'drive.json'

- Run download.py 

`python3 download.py`

- Change the values of ENV variables 

  - tok: Telegram bot token

  - id: Your Telegram API ID

  - hash: Your Telegram API Hash

  - group: ID of the Telegram group in which you want it to work

You can get API ID and API hash from [here](https://core.telegram.org/api/obtaining_api_id)

- Add the bot to the group
- Use /get command in the group

## To-do
- [ ] Make it work for different groups by authenticating users

- [ ] Make it work in chat
