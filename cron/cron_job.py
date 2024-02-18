# call all the webscrapers and update the database with the new information however if the information is already in the database then do not add it again
# import models from the db folder
from ..db.models import Database, Event, PrayerTime
from ..db.config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from ..scrapers.scrape_instagram import InstagramScraper
from ..scrapers.rahmaScraper import RahmaSpider
from ..scrapers.snmcScraper import SnmcSpider
from ..scrapers.kmaScraper import KmaSpider
from ..scrapers.jamiOmarScraper import JamiOmarSpider
from datetime import datetime
# import the rate limiter
from ..utils.rateLimiter import RateLimiter
import logging

# create a database object
db = Database(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
rate_limiter = RateLimiter(rate=1, burst=1)

# create a webscraper object`
rahma = RahmaSpider()
snmc = SnmcSpider()
kma = KmaSpider()
jamiOmar = JamiOmarSpider()
insta = InstagramScraper()

# get the events and prayer times from the webscrapers
rahmaEvents = rahma.get_events()
rahmaPrayerTimes = rahma.get_prayerTimes()
snmcEvents = snmc.get_events()
snmcPrayerTimes = snmc.get_prayerTimes()
kmaEvents = kma.get_events()
kmaPrayerTimes = kma.get_prayerTimes()
jamiOmarEvents = jamiOmar.get_events()
# jamiOmarPrayerTimes = jamiOmar.get_prayerTimes()

uomsaEvents =  insta.get_latest_posts("uomsa.aemuo")
print("reach here after uomsa")
cumsaEvents = insta.get_latest_posts("carletonmsa")
print("reach here after cumsa")
ottawaMosqueEvents = insta.get_latest_posts("theottawamosque")
bicEvents = insta.get_latest_posts("barrhavenislamiccentre")
algonquinEvents = insta.get_latest_posts("algonquinmsa_")

# add the events and prayer times to the database
for event in rahmaEvents:
    created_at = datetime.now()
    created_at = created_at.strftime("%Y-%m-%d %H:%M:%S")
    with rate_limiter:
        new_event = Event(
            title = event.get("title"),
            link=event.get("link"),
            image=event.get("image"),
            full_description=event.get("description"),
            created_at=datetime.now(),
            organization_id=3
    )

    db.add_event(title=new_event.title, link=new_event.link, image=new_event.image, full_description=new_event.full_description, created_at=new_event.created_at, organization_id=new_event.organization_id)

for event in snmcEvents:
    with rate_limiter:
        db.add_event(full_description=event.get("description"), image=event.get("image"), link=event.get("link"), organization_id=5, created_at=datetime.now())
        logging.info("Added snmc event to database: " + event.get("description"))
for event in kmaEvents:
    with rate_limiter:
        db.add_event(title=event.get("title"), full_description=event.get("full_description"), image=event.get("image"), link=event.get("link"), start_time=event.get("start_time"), end_time=event.get("end_time"), other_info=event.get("iframe"), sub_links=event.get("other_links"), organization_id=4, created_at=datetime.now())
        logging.info("Added kma event to database: " + event.get("title"))
for event in jamiOmarEvents:
    with rate_limiter:
        db.add_event(title=event.get("title") ,full_description= event.get("description"), image= event.get("image"), link= event.get("link"), location=event.get("location"), start_time=event.get("start_time"), end_time=event.get("end_time"), sub_links=event.get("registration_link"), cost=event.get("cost"), organization_id=6, created_at=datetime.now())
        logging.info("Added jami omar event to database: " + event.get("title"))
for prayer_time in rahmaPrayerTimes:
    with rate_limiter:
        db.add_prayer_time(prayer_time.get("prayer_name"), prayer_time.get("athan_time"), prayer_time.get("iqama_time"), organization_id=3)
        logging.info("Added rahma prayer time to database: " + prayer_time.get("prayer_name"))
for prayer_time in snmcPrayerTimes:
    with rate_limiter:
        db.add_prayer_time(prayer_time.get("prayer_name"), prayer_time.get("athan_time"), prayer_time.get("iqama_time"), organization_id=5)
        logging.info("Added snmc prayer time to database: " + prayer_time.get("prayer_name"))
for prayer_time in kmaPrayerTimes:
    with rate_limiter:
        db.add_prayer_time(prayer_time.get("prayer_name"), prayer_time.get("athan_time"), prayer_time.get("iqama_time"), organization_id=4)
        logging.info("Added kma prayer time to database: " + prayer_time.get("prayer_name"))
# for prayer_time in jamiOmarPrayerTimes:
#     with rate_limiter:
#         db.add_prayer_time(prayer_time)
        
for event in uomsaEvents:
    with rate_limiter:
        db.add_event(full_description= event.get("description"), image= event.get("image"), link= event.get("link"), organization_id=10, created_at=datetime.now())
        logging.info("Added uomsa event to database: " + event.get("description"))

for event in cumsaEvents:
    with rate_limiter:
        db.add_event(full_description= event.get("description"), image= event.get("image"), link= event.get("link"), organization_id=9, created_at=datetime.now())
        logging.info("Added cumsa event to database: " + event.get("description"))

for event in ottawaMosqueEvents:
    with rate_limiter:
        db.add_event(full_description= event.get("description"), image= event.get("image"), link= event.get("link"), organization_id=1, created_at=datetime.now())
        logging.info("Added ottawa mosque event to database: " + event.get("description"))

for event in bicEvents:
    with rate_limiter:
        db.add_event(full_description= event.get("description"), image= event.get("image"), link= event.get("link"), organization_id=8, created_at=datetime.now())
        logging.info("Added bic event to database: " + event.get("image"))

for event in algonquinEvents:
    with rate_limiter:
        db.add_event(full_description= event.get("description"), image= event.get("image"), link= event.get("link"), organization_id=11, created_at=datetime.now())
        logging.info("Added algonquin event to database: " + event.get("description"))
# close the database connection
db.close_connection()
logging.info("Database connection closed")
