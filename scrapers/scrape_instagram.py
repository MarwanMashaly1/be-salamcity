import instaloader
from base64 import b64encode
import requests
from io import BytesIO

class InstagramScraper:
    # the class should have all the function that are below nad it should be able to return the data and the constructor should initialize the instaloader and login 
    def __init__(self):
        self.L = instaloader.Instaloader()
        try:
            # Try loading session from file
            self.L.load_session_from_file("ig_session", "./ig_session")
        except instaloader.InstaloaderException as e:
            print(f"Session not loaded: {e}")
            # If session loading fails, login
            self.L.context.log_in("salamgetpost", "SalamCity@2023")
            # Save the session to file for future use
            self.L.save_session_to_file("ig_session")
    
    def get_latest_posts(self, username):
        try :
            profile = instaloader.Profile.from_username(self.L.context, username)
            # check for pinned posts and remove them
            posts = profile.get_posts()
            count = 0
            latest_posts = []
            for post in posts:
                if count == 1:
                    break
                if post.is_pinned:
                    count -= 1
                else:
                    latest_posts.append(post)
                count += 1

            posts = []

            for post in latest_posts:
                # get image url and extract image from it then forward it instead of url
                # response = requests.get(post.url)
                response = requests.get(post.url, timeout=20)
                if response.status_code == 200:
                    # scrape the image from the url
                    content = BytesIO(response.content)
                    if content:
                        # Encode image content to base64
                        image_base64 = b64encode(content.read()).decode('utf-8')
                        # print(image_base64)
                        image = "data:image/png;base64," + image_base64
                        posts.append((post.caption, image, username, profile.userid, "https://www.instagram.com/p/" + post.shortcode))
                    else:
                        posts.append((post.caption, post.url, username, profile.userid, "https://www.instagram.com/p/" + post.shortcode))
                else:
                    posts.append((post.caption, post.url, username, profile.userid, "https://www.instagram.com/p/" + post.shortcode))
            return posts
        except Exception as e:
            print(e)
            return []
    
    def get_profile_picture(self, username):
        profile = instaloader.Profile.from_username(self.L.context, username)

        return profile.profile_pic_url
    
    def get_profile_info(self, username):
        profile = instaloader.Profile.from_username(self.L.context, username)

        return profile.biography
    
    def get_profile_name(self, username):
        profile = instaloader.Profile.from_username(self.L.context, username)

        return profile.full_name
    
    # def update(self):
    #     self.L.close()
    #     self.L = instaloader.Instaloader()
    #     self.L.login("salamgetpost2", "SalamCity@2023")