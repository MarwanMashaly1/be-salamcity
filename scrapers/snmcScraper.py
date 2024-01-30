from datetime import datetime
import json
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request


class SnmcSpider:
    def __init__(self):
        self.events_page = urlopen("https://snmc.ca/").read()
        prayer_req = Request(
            url='https://mawaqit.net/en/south-nepean-muslim-community-snmc-ottawa-k2j-4g3-canada', headers={'User-Agent': 'Mozilla/5.0'})
        self.prayer_page = urlopen(prayer_req).read()
        self.events_soup = BeautifulSoup(self.events_page, 'html.parser')
        self.prayer_soup = BeautifulSoup(self.prayer_page, 'html.parser')

    def get_events(self):
        events_t = []
        events = self.events_soup.find_all('div', {'class': 'sbi_item'})
        for event in events:
            events_t.append([event.find('img')['alt'],
                            event.find('a')['data-full-res'], "snmc"])
        return events_t

    def get_prayerTimes(self):
        prayer_times = []
        script_text = self.prayer_soup.find_all('script')[1]
        data = script_text.contents[0]

        prayer_times.append(
            ("SNMC", "3020 Woodroffe Ave, Nepean, ON K2J 4G3", "(613) 440-6300"))

        athan_times = json.loads(data.split('"times":')[
                                 1].split(',"shuruq"')[0])

        iqamaCalendar = data.split('"iqamaCalendar":')[
            1].split('};')[0]
        iqama_json = json.loads(iqamaCalendar)
        today = datetime.now()

        current_month = today.month
        current_day = today.day

        # Find the iqama time for today's date
        if 1 <= current_day <= len(iqama_json[current_month - 1]):
            today_iqama = iqama_json[current_month - 1][str(current_day)]
        else:
            today_iqama = None

        for i in range(len(athan_times)):
            if i == 0:
                prayer_times.append(("Fajr", athan_times[i], today_iqama[i]))
            elif i == 1:
                prayer_times.append(("Zuhr", athan_times[i], today_iqama[i]))
            elif i == 2:
                prayer_times.append(("Asr", athan_times[i], today_iqama[i]))
            elif i == 3:
                prayer_times.append(
                    ("Maghrib", athan_times[i], today_iqama[i]))
            elif i == 4:
                prayer_times.append(("Isha", athan_times[i], today_iqama[i]))

        prayer_times.append(
            ("Jumuʿah", "12:00 PM", "-"))
        prayer_times.append(
            ("Jumuʿah 2", "1:15 PM", "-", ))
        return prayer_times
