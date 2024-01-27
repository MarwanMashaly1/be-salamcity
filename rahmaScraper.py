from bs4 import BeautifulSoup
from urllib.request import urlopen


class RahmaSpider:
    def __init__(self):
        self.events_page = urlopen("https://www.mymasjid.ca/events").read()
        self.prayer_page = urlopen(
            "https://app.mymasjid.ca/protected/public/timetable").read()
        self.events_soup = BeautifulSoup(self.events_page, 'html.parser')
        self.prayer_soup = BeautifulSoup(self.prayer_page, 'html.parser')

    def get_events(self):
        events = []
        table = self.events_soup.find(lambda tag: tag.name == 'table' and tag.has_attr(
            'id') and tag['id'] == "tablepress-4")
        rows = table.findAll(lambda tag: tag.name == 'tr')
        for row in rows:
            if row.find('td') is not None:
                event_name = row.find('td').text
                event_link = row.find('a')['href']
                event_description = self.get_eventInfo(event_link)
                events.append((event_name, event_link, event_description, "Rahma"))
        return events

    def get_prayerTimes(self):
        prayerTimes = []
        prayerTimes.append(
            ("Masjid Ar-Rahma", "1216 Hunt Club Rd, Ottawa, ON K1V 2P1", "(613) 523-9977"))
        table = self.prayer_soup.find("table", {"class": "table table-sm"})
        if table is not None:
            for row in table.findAll("tr"):
                if row.find('td') is not None:
                    if row.find('td').text == "Salāh":
                        continue
                    prayer_eng = row.find('td').text
                    athan_time = row.find('td').find_next_sibling().text
                    iqama_time = row.find(
                        'td').find_next_sibling().find_next_sibling().text
                    # prayer_ar = row.find('td').find_next_sibling(
                    # ).find_next_sibling().find_next_sibling().text
                    prayerTimes.append(
                        (prayer_eng, athan_time, iqama_time))
        return prayerTimes

    def get_eventInfo(self, event_link):
        eventInfo = []
        event_page = urlopen(event_link).read()
        event_soup = BeautifulSoup(event_page, 'html.parser')
        event_description = event_soup.find(class_='content event_details')
        if event_description is not None:
            eventInfo.append(event_description.text)
            # for description in event_description.find_all('p'):
            #     eventInfo.append(description.text)
            # for description in event_description.find_all('li'):
            #     eventInfo.append("point: " + description.text)

        if event_soup.find(class_='content event_poster') is not None:
            event_image = event_soup.find(class_='content event_poster')
            eventInfo.append("https://events.mymasjid.ca" +
                             event_image.find('img')['src'])
        return eventInfo
