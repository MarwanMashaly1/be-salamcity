import requests
from db.models import Database
from db.config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

db = Database(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

events = db.get_all_events_created_today()
url = "https://gate.whapi.cloud/messages/image?token=yB2QPi0JYCRVhnGzTPCWjEcEZOnfJoFT"
for event in events:
    if event.get("is_new") == None:
        continue
    elif event.get("is_new") == False:
        continue
    else:
        media = event.get("image")
        if media == None:
            url = "https://gate.whapi.cloud/messages/text?token=yB2QPi0JYCRVhnGzTPCWjEcEZOnfJoFT"
        body_parts = []
        if event.get("title"):
            body_parts.append(event.get("title"))
        if event.get("organization_name"):
            body_parts.append("Organization: " + event.get("organization_name"))
        if event.get("link"):
            body_parts.append("link: " + event.get("link"))
        if event.get("full_description"):
            body_parts.append("Description: " + event.get("full_description"))
        body_parts.append("Website: salamcity.ca")
        if url.find("text") != -1:
            payload = {
                "typing_time": 5,
                "to": "120363262282954758@g.us",
                "body": "\n".join(body_parts)
            }
        else:
            payload = {
                "typing_time": 5,
                "to": "120363262282954758@g.us",
                "caption": "\n".join(body_parts),
                "media": media
            }

        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        print(response.text)
        print("Event sent to whatsapp")

