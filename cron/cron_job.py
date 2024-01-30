# call all the webscrapers and update the database with the new information however if the information is already in the database then do not add it again
# import models from the db folder
from db.models import Database
from db.config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from scrapers.scrape_instagram import InstagramScraper
from scrapers.rahmaScraper import RahmaSpider
from scrapers.snmcScraper import SnmcSpider
from scrapers.kmaScraper import KmaSpider
from scrapers.jamiOmarScraper import JamiOmarSpider
from datetime import datetime
import utils.rateLimiter as RateLimiter
import time
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
# uomsaEvents =  insta.get_latest_posts("uomsa.aemuo")
# cumsaEvents = insta.get_latest_posts("carletonmsa")
# ottawaMosqueEvents = insta.get_latest_posts("theottawamosque")
# bicEvents = insta.get_latest_posts("barrhavenislamiccentre")

# add the events and prayer times to the database
for event in rahmaEvents:
    with rate_limiter:
        db.add_event(event)

for event in snmcEvents:
    with rate_limiter:
        db.add_event(event)

for event in kmaEvents:
    with rate_limiter:
        db.add_event(event)

for event in jamiOmarEvents:
    with rate_limiter:
        db.add_event(event)

for prayer_time in rahmaPrayerTimes:
    with rate_limiter:
        db.add_prayer_time(prayer_time)

for prayer_time in snmcPrayerTimes:
    with rate_limiter:
        db.add_prayer_time(prayer_time)

for prayer_time in kmaPrayerTimes:
    with rate_limiter:
        db.add_prayer_time(prayer_time)

# for prayer_time in jamiOmarPrayerTimes:
#     with rate_limiter:
#         db.add_prayer_time(prayer_time)
        
# for event in uomsaEvents:
#     with rate_limiter:
#         db.add_event(event)
        
# for event in cumsaEvents:
#     with rate_limiter:
#         db.add_event(event)
        
# for event in ottawaMosqueEvents:
#     with rate_limiter:
#         db.add_event(event)
        
# for event in bicEvents:
#     with rate_limiter:
#         db.add_event(event)
        
# close the database connection
db.close_connection()
