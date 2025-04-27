# call all the webscrapers and update the database with the new information however if the information is already in the database then do not add it again
# import models from the db folder
from db.models import Database, Event, PrayerTime
from db.config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from scrapers.scrape_instagram import InstagramScraper
from scrapers.rahmaScraper import RahmaSpider
from scrapers.snmcScraper import SnmcSpider
from scrapers.kmaScraper import KmaSpider
from scrapers.jamiOmarScraper import JamiOmarSpider
from scrapers.bukhariScraper import BukhariSpider
from datetime import datetime
# import the rate limiter
import time
from utils.rateLimiter import RateLimiter
import logging
from categorization.categoriy import Categorize
import utils.proxies as proxies

# create a database object
db = Database(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
rate_limiter = RateLimiter(rate=1, burst=1)
#  initalize the categorization class
cat = Categorize(token_counter_min=0, rpd=0, rpm=0)

def add_details():
    print("Adding details")
    proxy_list = proxies.get_proxies()
    # create a webscraper object`
    rahma = RahmaSpider(proxy_list=proxy_list)
    snmc = SnmcSpider(proxy_list=proxy_list)
    kma = KmaSpider(proxy_list=proxy_list)
    jamiOmar = JamiOmarSpider(proxy_list=proxy_list)
    # bukhari = BukhariSpider(proxy_list=proxy_list)
    # insta = InstagramScraper() 

    # get the events and prayer times from the webscrapers
    rahmaEvents = rahma.get_events()
    rahmaPrayerTimes = rahma.get_prayerTimes()
    snmcEvents = snmc.get_events()
    snmcPrayerTimes = snmc.get_prayerTimes()
    kmaEvents = kma.get_events()
    kmaPrayerTimes = kma.get_prayerTimes()
    jamiOmarEvents = jamiOmar.get_events()
    # # jamiOmarPrayerTimes = jamiOmar.get_prayerTimes()
    # bukharicenterEvents = bukhari.get_events()
    # ottawaMosqueEvents = insta.get_latest_posts("theottawamosque", 2)
    # print("ottawa mosque events: ", ottawaMosqueEvents)
    # time.sleep(60)

    # add the events and prayer times to the database
    for event in rahmaEvents:
        category = categorize_events(event.get("title"), event.get("description"))
        with rate_limiter:
            new_event = Event(
                title = event.get("title"),
                link=event.get("link"),
                image=event.get("image"),
                full_description=event.get("description"),
                created_at=datetime.now(),
                organization_id=3,
                organization_name="Masjid Ar-Rahmah"
            )

        db.add_event(title=new_event.title, link=new_event.link, image=new_event.image, full_description=new_event.full_description, categories=category, created_at=new_event.created_at, organization_id=new_event.organization_id, organization_name=new_event.organization_name)
    print("rahma events added")
    for event in snmcEvents:
        category = categorize_events(event.get("title"), event.get("description"))
        with rate_limiter:
            print("snmc event: ", event)
            db.add_event(full_description=event.get("description"), image=event.get("image"), link=event.get("link"), organization_id=5, created_at=datetime.now(), organization_name="SNMC", is_video=event.get("is_video"), categories=category)
            logging.info("Added snmc event to database: " + event.get("link"))
    print("snmc events added")
    for event in kmaEvents:
        category = categorize_events(event.get("title"), event.get("description"))
        with rate_limiter:
            db.add_event(title=event.get("title"), full_description=event.get("full_description"), image=event.get("image"), link=event.get("link"), start_time=event.get("start_time"), end_time=event.get("end_time"), other_info=event.get("iframe"), sub_links=event.get("other_links"), organization_id=4, created_at=datetime.now(), organization_name="KMA", categories=category)
            logging.info("Added kma event to database: " + event.get("title"))
    for event in jamiOmarEvents:
        category = categorize_events(event.get("title"), event.get("description"))
        with rate_limiter:
            db.add_event(title=event.get("title") ,full_description= event.get("description"), image= event.get("image"), link= event.get("link"), start_time=event.get("start_time"), end_time=event.get("end_time"), sub_links=event.get("registration_link"), cost=event.get("cost"), organization_id=6, created_at=datetime.now(), organization_name="Jami Omar", categories=category)
            logging.info("Added jami omar event to database: " + event.get("title"))
    for prayer_time in rahmaPrayerTimes:
        with rate_limiter:
            db.add_prayer_time(prayer_time.get("prayer_name"), prayer_time.get("athan_time"), prayer_time.get("iqama_time"), organization_id=3, organization_name="Masjid Ar-Rahmah")
            logging.info("Added rahma prayer time to database: " + prayer_time.get("prayer_name"))
    for prayer_time in snmcPrayerTimes:
        with rate_limiter:
            db.add_prayer_time(prayer_time.get("prayer_name"), prayer_time.get("athan_time"), prayer_time.get("iqama_time"), organization_id=5, organization_name="SNMC")
            logging.info("Added snmc prayer time to database: " + prayer_time.get("prayer_name"))
    for prayer_time in kmaPrayerTimes:
        with rate_limiter:
            db.add_prayer_time(prayer_time.get("prayer_name"), prayer_time.get("athan_time"), prayer_time.get("iqama_time"), organization_id=4, organization_name="KMA")
            logging.info("Added kma prayer time to database: " + prayer_time.get("prayer_name"))
            
    # close the database connection
    db.update_old_activity()
    db.close_connection()
    logging.info("Database connection closed")

def categorize_events(event_name, event_description):
    while True:
        categories = cat.classify(event_name, event_description)
        if categories == "token limit reached per minute" or categories == "requests limit reached per minute":
            time.sleep(90)
        elif categories == "token limit reached per day":
            return "uncategorized"
        else:
            return categories