from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlparse, urlunparse, parse_qs

class JamiOmarSpider:
    def __init__(self) -> None:
        self.page = urlopen("https://www.jamiomar.org/")
        self.soup = BeautifulSoup(self.page, 'html.parser')
    
    
    def get_events(self):
        events = []
        main_div = self.soup.find_all('div', class_='Zc7IjY')
        # list_items = main_div.find_all('div', class_='Zc7IjY')
        count = 0
        for item in main_div:
            if count > 7:
                break
            event_title = item.find('h4', class_='font_4').text.strip()

            button_link = item.find('div', class_='comp-kimeej6i').find('a')
            
            btn_url = ''
            btn_label = ''
            if button_link:
                # Extract link URL
                btn_url = button_link['href']
                # Extract button label
                btn_label = button_link.find('span', class_='StylableButton2545352419__label').text.strip()
            else:
                # Extract button label
                btn_label = item.find('span', class_='StylableButton2545352419__label').text.strip()
                btn_url = None

            # Extract donation instructions
            donation_instructions = item.find('div', class_='comp-kyqk9s96').find('p', class_='font_8').text.strip()

            # Extract image URL
            image_url = item.find('img')['src']

            # Check if 'blur_2' is present in the query parameters
            if 'blur_2' in image_url:
                image_url = image_url.replace(',blur_2', '')
            if 'w_101' in image_url and 'h_57' in image_url:
                image_url = image_url.replace('w_101', 'w_496')
                image_url = image_url.replace('h_57', 'h_264')
            events.append((image_url, event_title, donation_instructions, btn_url, btn_label))
            count +=1

        return(events)
    def get_prayertimes(self):
        times = []
        main_div = self.soup.find_all('div', class_='comp-kimeej6i')
        for item in main_div:
            if item.find('div', class_='comp-kimeej6i'):
                continue
            else:
                prayer_name = item.find('div', class_='font_4').text.strip()
                prayer_time = item.find('div', class_='font_5').text.strip()
                times.append((prayer_name, prayer_time))
        return(times)
        