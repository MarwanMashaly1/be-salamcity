import time
from categorization.categoriy import Categorize

cat = Categorize(token_counter_min=0, rpd=0, rpm=0)

def categorize_events(event_name, event_description):
    while True:
        categories = cat.classify(event_name, event_description)
        if categories == "token limit reached per minute" or categories == "requests limit reached per minute":
            time.sleep(90)
        elif categories == "token limit reached per day":
            return "uncategorized"
        else:
            return categories