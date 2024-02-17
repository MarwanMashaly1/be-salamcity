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
                event = {}
                # event_name = row.find('td').text
                event["title"] = row.find('td').text
                event_link = row.find('a')['href']
                event["link"] = event_link
                event_info = self.get_eventInfo(event_link)
                if "image" in event_info:
                    event["image"] = event_info["image"]
                # else:
                #     event_image = None
                if "description" in event_info:
                    event["description"] = event_info["description"]

                events.append(event)
                # else:
                #     event_description = None
                    
                # if len(event_info) > 0:
                #     event_description = event_info[0]
                # else:
                #     event_description = None
                # if len(event_info) > 1:
                #     event_image = event_info[1]
                # else:
                #     event_image = None
                # append to events based on how it should look like in the orm
                # events.append((event_name, event_link, event_image, event_description))
                # events.append((event_name, event_link, event_description, "Rahma"))
        return events

    def get_prayerTimes(self):
        prayerTimes = []
        # prayerTimes.append(
        #     ("Masjid Ar-Rahma", "1216 Hunt Club Rd, Ottawa, ON K1V 2P1", "(613) 523-9977"))
        table = self.prayer_soup.find("table", {"class": "table table-sm"})
        if table is not None:
            for row in table.findAll("tr"):
                if row.find('td') is not None:
                    if row.find('td').text == "Salāh":
                        continue
                    prayer = {}
                    prayer_eng = row.find('td').text
                    athan_time = row.find('td').find_next_sibling().text
                    iqama_time = row.find(
                        'td').find_next_sibling().find_next_sibling().text
                    # prayer_ar = row.find('td').find_next_sibling(
                    # ).find_next_sibling().find_next_sibling().text
                    prayer["prayer_name"] = prayer_eng
                    prayer["athan_time"] = athan_time
                    prayer["iqama_time"] = iqama_time
                    prayerTimes.append(prayer)
        return prayerTimes

    def get_eventInfo(self, event_link):
        eventInfo = {}
        event_page = urlopen(event_link).read()
        event_soup = BeautifulSoup(event_page, 'html.parser')
        event_description = event_soup.find(class_='content event_details')
        if event_description is not None:
            eventInfo["description"] = event_description.text
            # eventInfo.append(event_description.text)
            # for description in event_description.find_all('p'):
            #     eventInfo.append(description.text)
            # for description in event_description.find_all('li'):
            #     eventInfo.append("point: " + description.text)

        if event_soup.find(class_='content event_poster') is not None:
            event_image = event_soup.find(class_='content event_poster')
            eventInfo["image"] = "https://events.mymasjid.ca" + event_image.find('img')['src']
            # eventInfo.append("https://events.mymasjid.ca" +
            #                  event_image.find('img')['src'])
        return eventInfo