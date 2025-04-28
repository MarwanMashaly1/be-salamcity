import logging
from datetime import datetime
import time
from categorize import categorize_events
import re
from dateutil import parser as date_parser


organization_mapping = {
            "BIC": {
                "organization_id": 8,
                "organization_name": "Barrhaven Islamic Centre",
            },
            "uOttawa": {
                "organization_id": 10,
                "organization_name": "University of Ottawa MSA",
            },
            "Carleton": {
                "organization_id": 9,
                "organization_name": "Carleton MSA",
            },
            "Algonquin": {
                "organization_id": 11,
                "organization_name": "Algonquin MSA",
            },
            "Ottawa Mosque": {
                "organization_id": 1,
                "organization_name": "Ottawa Muslim Association",
            },
        }

def process_message_event(db, message):
    try:
        msg_type = message.get('type', 'unknown')
        chat_name = message.get('chat_name', '').strip()
        logging.info(f"Processing message from chat: {chat_name}")
        print(f"Processing message from chat: {chat_name}")
        # Check if the chat name matches any known organization
        

        org_info = None
        for key, value in organization_mapping.items():
            if key.lower() in chat_name.lower():
                print(f"Chat name '{chat_name}' recognized as '{key}'")
                org_info = value
                break

        if not org_info:
            logging.warning(f"Chat name '{chat_name}' not recognized; ignoring message.")
            return  # Or handle unknown communities as needed

        # Initialize event properties
        full_description = ''
        image = None
        link = None
        is_video = False
        title = None
        print("message: ", message)

        if msg_type == 'text':
            # For text messages, assume the text is in a nested 'text' field.
            full_description = message.get('text', {}).get('body', '')
            title = full_description.split('\n', 1)[0]  # Use the first line as title if appropriate.
        elif msg_type == 'image':
            # For document messages, extract details from the 'document' field.
            document_info = message.get('document', {})
            full_description = document_info.get('caption', '')
            link = document_info.get('link', '')
            image = document_info.get('preview')  # Optional thumbnail image.
            title = document_info.get('file_name', '')
        else:
            logging.info(f"Unhandled message type: {msg_type}")
            return

        # Categorize events using your categorization function.
        categories = categorize_events(title, full_description)

        parsed = parse_event_from_message(full_description)
        if parsed['is_event']:

            # Insert the event into the database using a rate-limited call if necessary.
            db.add_event(
                full_description=full_description,
                image=image,
                link=link,
                organization_id=org_info['organization_id'],
                created_at=datetime.now(),
                organization_name=org_info['organization_name'],
                is_video=is_video,
                categories=categories,
                date=parsed['date'],
                time=parsed['time'],
                location=parsed['location'],
            )
            logging.info(
                f"Added event to database for organization {org_info['organization_name']}: {link}"
            )
        else:
            logging.info(f"Message does not appear to be an event: {full_description}")

    except Exception as e:
        logging.error(f"Error processing message: {e}")
        print(f"Error processing message: {e}")
        
def parse_event_from_message(msg: str):
    result = {
        "is_event": False,
        "date": None,
        "time": None,
        "location": None,
    }

    score = 0

    # --------- Date Extraction ---------
    date_match = None
    date_patterns = [
        r'(?:Saturday|Sunday|Monday|Tuesday|Wednesday|Thursday|Friday),?\s*(?:April|May|June|July|August|September|October|November|December)\s*\d{1,2}(?:,\s*\d{4})?',
        r'\b(?:April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:,\s*\d{4})?',
        r'\b\d{1,2}/\d{1,2}/\d{2,4}',  # e.g., 04/12/2025
    ]

    for pattern in date_patterns:
        match = re.search(pattern, msg, re.IGNORECASE)
        if match:
            try:
                parsed_date = date_parser.parse(match.group(), fuzzy=True)
                result['date'] = parsed_date.date().isoformat()
                score += 1
                break
            except:
                pass

    # --------- Time Extraction ---------
    time_match = re.search(r'\b\d{1,2}(:\d{2})?\s?(AM|PM|am|pm)', msg)
    if time_match:
        result['time'] = time_match.group().strip()
        score += 1

    # --------- Location Extraction ---------
    location_match = re.search(r'(📍|Location:|location:)?\s*(.*?)(\n|$)', msg, re.IGNORECASE)
    if location_match:
        location = location_match.group(2).strip()
        if len(location) > 5 and not any(x in location.lower() for x in ['zoom', 'online']):
            result['location'] = location
            score += 1

    # --------- Event Likelihood Score ---------
    event_keywords = [
        "join us", "register", "event", "camp", "lecture", "program", "seminar",
        "conference", "starts", "workshop", "RSVP", "starting", "don't miss"
    ]
    if any(word.lower() in msg.lower() for word in event_keywords):
        score += 1

    # Use emoji presence as signal
    if '🗓' in msg or '📅' in msg or '⏰' in msg or '📍' in msg:
        score += 1

    # Declare it an event if it hits threshold
    result["is_event"] = score >= 2

    print(f"Parsed event: {result}")
    logging.info(f"Parsed event: {result}")

    return result