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
import time
import logging

# create a database object
db = Database(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

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
# jamiOmarPrayerCallTime = datetime.now()

# uomsaEvents =  insta.get_latest_posts("uomsa.aemuo")
# uomsaEventCallTime = datetime.now()

# cumsaEvents = insta.get_latest_posts("carletonmsa")
# cumsaEventCallTime = datetime.now()

# ottawaMosqueEvents = insta.get_latest_posts("theottawamosque")
# ottawaMosqueEventCallTime = datetime.now()

# bicEvents = insta.get_latest_posts("barrhavenislamiccentre")
# bicEventCallTime = datetime.now()

# add the events and prayer times to the database
for event in rahmaEvents:
    db.add_event(event)
    time.sleep(1)

for event in snmcEvents:
    db.add_event(event)
    time.sleep(1)

for event in kmaEvents:
    db.add_event(event)
    time.sleep(1)

for event in jamiOmarEvents:
    db.add_event(event)
    time.sleep(1)

# for event in uomsaEvents:
#     db.add_event(event)
#     time.sleep(1)
#
# for event in cumsaEvents:
#     db.add_event(event)
#     time.sleep(1)
#
# for event in ottawaMosqueEvents:
#     db.add_event(event)
#     time.sleep(1)
#
# for event in bicEvents:
#     db.add_event(event)
#     time.sleep(1)

for prayer in rahmaPrayerTimes:
    db.add_prayer_time(prayer)
    time.sleep(1)

for prayer in snmcPrayerTimes:
    db.add_prayer_time(prayer)
    time.sleep(1)

for prayer in kmaPrayerTimes:
    db.add_prayer_time(prayer)
    time.sleep(1)

# for prayer in jamiOmarPrayerTimes:
#     db.add_prayer_time(prayer)
#     time.sleep(1)
    
# print("rahma events: ", rahmaEvents)
# print("snmc events: ", snmcEvents)