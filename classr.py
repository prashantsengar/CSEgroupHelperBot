import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import download

NLP = "56103600610"

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.announcements",
]

def init():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("classroom", "v1", credentials=creds, cache_discovery=False)

    return service


def main():
    """Shows basic usage of the Classroom API.
    Prints the names of the first 10 courses the user has access to.
    """
    service = init()

    # Call the Classroom API
    results = service.courses().list(pageSize=10).execute()
    courses = results.get("courses", [])

    if not courses:
        print("No courses found.")
    else:
        print("Courses:")
        print(courses)
        for course in courses:
            print(course["name"])


def get_announcements(course_id):
    service = main()

    topics = []
    page_token = None
    while True:
        response = (
            service.courses()
            .announcements()
            .list(pageToken=page_token, pageSize=30, courseId=course_id)
            .execute()
        )
        topics.extend(response.get("announcements", []))
        page_token = response.get("nextPageToken", None)
        if not page_token:
            break
    if not topics:
        print("No announcement found.")
    else:
        return topics


##        files = []
##        texts = []
##        print('Announcements:')
##        c=0
##        for topic in topics:
##            if c==0:
##                print(topic)
##                c=1
##            print('{0}'.format(topic['text']))
##            print(topic['materials'])
##            print('\n\n-----\n\n')
##            text = topic['text']
##            for i in topic['materials']:
##                try:
##                    file = download.get_file(i['driveFile']['driveFile']['id'])
##                    file.name = i['driveFile']['driveFile']['title']
##                    files.append(file)
##                    texts.append(text)
##                    return texts, files
##                except KeyError:
##                    print('Key not found')
##
##
##        return texts, files

if __name__ == "__main__":
    main()
