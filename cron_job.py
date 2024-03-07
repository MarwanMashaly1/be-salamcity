# call all the webscrapers and update the database with the new information however if the information is already in the database then do not add it again
# import models from the db folder
from db.models import Database, Event, PrayerTime
from db.config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from scrapers.scrape_instagram import InstagramScraper
from scrapers.rahmaScraper import RahmaSpider
from scrapers.snmcScraper import SnmcSpider
from scrapers.kmaScraper import KmaSpider
from scrapers.jamiOmarScraper import JamiOmarSpider
from datetime import datetime
# import the rate limiter
from utils.rateLimiter import RateLimiter
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
cumsaEvents = insta.get_latest_posts("carletonmsa")
ottawaMosqueEvents = insta.get_latest_posts("theottawamosque")
bicEvents = insta.get_latest_posts("barrhavenislamiccentre")
algonquinEvents = insta.get_latest_posts("algonquinmsa_")
bukharicenterEvents = insta.get_latest_posts("bukharicentre")
print("bukhari center events: ", bukharicenterEvents)

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
            organization_id=3,
            organization_name="Masjid Ar-Rahmah"
        )

    db.add_event(title=new_event.title, link=new_event.link, image=new_event.image, full_description=new_event.full_description, created_at=new_event.created_at, organization_id=new_event.organization_id, organization_name=new_event.organization_name)

for event in snmcEvents:
    with rate_limiter:
        db.add_event(full_description=event.get("description"), image=event.get("image"), link=event.get("link"), organization_id=5, created_at=datetime.now(), organization_name="SNMC")
        logging.info("Added snmc event to database: " + event.get("description"))
for event in kmaEvents:
    with rate_limiter:
        db.add_event(title=event.get("title"), full_description=event.get("full_description"), image=event.get("image"), link=event.get("link"), start_time=event.get("start_time"), end_time=event.get("end_time"), other_info=event.get("iframe"), sub_links=event.get("other_links"), organization_id=4, created_at=datetime.now(), organization_name="KMA")
        logging.info("Added kma event to database: " + event.get("title"))
for event in jamiOmarEvents:
    with rate_limiter:
        db.add_event(title=event.get("title") ,full_description= event.get("description"), image= event.get("image"), link= event.get("link"), location=event.get("location"), start_time=event.get("start_time"), end_time=event.get("end_time"), sub_links=event.get("registration_link"), cost=event.get("cost"), organization_id=6, created_at=datetime.now(), organization_name="Jami Omar")
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
# for prayer_time in jamiOmarPrayerTimes:
#     with rate_limiter:
#         db.add_prayer_time(prayer_time)
        
for event in uomsaEvents:
    with rate_limiter:
        db.add_event(full_description= event.get("description"), image= event.get("image"), link= event.get("link"), organization_id=10, created_at=datetime.now(), organization_name="UOMSA", is_video=event.get("is_video"))
        logging.info("Added uomsa event to database: " + event.get("description"))

for event in cumsaEvents:
    with rate_limiter:
        db.add_event(full_description= event.get("description"), image= event.get("image"), link= event.get("link"), organization_id=9, created_at=datetime.now(), organization_name="CUMSA", is_video=event.get("is_video"))
        logging.info("Added cumsa event to database: " + event.get("description"))

for event in ottawaMosqueEvents:
    with rate_limiter:
        db.add_event(full_description= event.get("description"), image= event.get("image"), link= event.get("link"), organization_id=1, created_at=datetime.now(), organization_name="OMA", is_video=event.get("is_video"))
        logging.info("Added ottawa mosque event to database: " + event.get("description"))

for event in bicEvents:
    with rate_limiter:
        db.add_event(full_description= event.get("description"), image= event.get("image"), link= event.get("link"), organization_id=8, created_at=datetime.now(), organization_name="BIC", is_video=event.get("is_video"))
        logging.info("Added bic event to database: " + event.get("image"))

for event in algonquinEvents:
    with rate_limiter:
        db.add_event(full_description= event.get("description"), image= event.get("image"), link= event.get("link"), organization_id=11, created_at=datetime.now(), organization_name="AMSA", is_video=event.get("is_video"))
        logging.info("Added algonquin event to database: " + event.get("description"))

for event in bukharicenterEvents:
    with rate_limiter:
        db.add_event(full_description= event.get("description"), image= event.get("image"), link= event.get("link"), organization_id=13, created_at=datetime.now(), organization_name="Bukhari Centre", is_video=event.get("is_video"))
        logging.info("Added bukhari center event to database: " + event.get("link"))
# close the database connection
db.close_connection()
logging.info("Database connection closed")
