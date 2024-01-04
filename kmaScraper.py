from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from datetime import datetime
import json

class KmaSpider:
    def __init__(self):
        self.events_page = urlopen("https://kanatamuslims.ca/events/").read()
        prayer_req = Request(
            url='https://mawaqit.net/en/w/kma-masjid-ottawa?showOnly5PrayerTimes=0', headers={'User-Agent': 'Mozilla/5.0'})
        self.prayer_page = urlopen(prayer_req).read()
        self.events_soup = BeautifulSoup(self.events_page, 'html.parser')
        self.prayer_soup = BeautifulSoup(self.prayer_page, 'html.parser')

    def get_events(self):
        events = []
        single_event = []
        # Find events under the specified article tag
        article_events = self.events_soup.find_all('article', class_='mec-event-article')

        # Loop through each article tag containing event information
        for article_event in article_events:
            # Extract information from the article tag
            title = article_event.find('h3', class_='mec-event-title')
            event_date = article_event.find('span', class_='mec-start-date-label', itemprop='startDate')
            event_time_start = article_event.find('span', class_='mec-start-time')
            event_time_end = article_event.find('span', class_='mec-end-time')
            event_location = article_event.find('div', class_='mec-venue-details')
            event_description_short = article_event.find('div', class_='mec-event-description')
            event_link = article_event.find('a', class_='mec-booking-button')
            if event_link is not None:
                event_description_full =  self.get_eventInfo(event_link['href'])

            if title is not None:
                single_event.append(title.text)
            if event_date is not None:
                single_event.append(event_date.text)
            if event_time_start is not None:
                single_event.append(event_time_start.text)
            if event_time_end is not None:
                single_event.append(event_time_end.text)
            if event_location is not None:
                single_event.append(event_location.text)
            if event_description_short is not None:
                single_event.append(event_description_short.text)
            if event_link is not None:
                single_event.append(event_link['href'])
            if event_description_full is not None:
                single_event.append(event_description_full)
            events.append(single_event)
            single_event = []
        
        clean_events = []
        for i in range(len(events)):
            if len(events[i]) > 6:
                clean_events.append(events[i])            
        return clean_events

    def get_eventInfo(self, event_link):
        #
        eventInfo = []
        event_page = urlopen(event_link).read()
        event_soup = BeautifulSoup(event_page, 'html.parser')
        event_description = event_soup.find('div', class_='post-content')
        if event_description is not None:
            content_text = event_description.get_text()
            embedded_links = event_description.find_all('a')
            link_list = [link['href'] for link in embedded_links if link.has_attr('href')]
            iframes = event_description.find_all('iframe')
            iframe_list = [iframe['src'] for iframe in iframes if iframe.has_attr('src')]

            eventInfo.append(content_text)
            eventInfo.append(iframe_list)
            eventInfo.append(link_list)
        event_image = event_soup.find('div', class_='mec-events-event-image')
        if event_image is not None:
            eventInfo.append("https://kanatamuslims.ca/" + event_image.find('img')['data-lazy-src'])
        return eventInfo
    
    def get_prayerTimes(self):
        prayer_times = []

        script_text = self.prayer_soup.find_all('script')[1]
        data = script_text.contents[0]
        prayer_times.append(
            ("KMA", "2210 Innes Rd, Gloucester, ON K1B 4Z5", "(613) 741-5590"))

        athan_times = json.loads(data.split('"times":')[1].split(',"shuruq"')[0])
        iqamaCalendar = data.split('"iqamaCalendar":')[1].split('};')[0]
        jumua = data.split('"jumua":')[1].split(',"jumua2"')[0]
        jumua2 = data.split('"jumua2":')[1].split(',"jumuaAsDuhr"')[0]
        # shuruq_time = data.split('"shuruq":')[1].split(',"calendar"')[0]

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
        prayer_times.append(("Jumuʿah", jumua.strip('"'), '-'))
        prayer_times.append(("Jumuʿah 2", jumua2.strip('"'), '-'))
        # prayer_times.append(("Shuruq", shuruq_time, '-'))
        
        return prayer_times