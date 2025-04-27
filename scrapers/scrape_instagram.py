import instaloader
from base64 import b64encode
import requests
from io import BytesIO
import os
import random


class InstagramScraper:
    # the class should have all the function that are below nad it should be able to return the data and the constructor should initialize the instaloader and login 
    def __init__(self, proxies_file="proxies_list.txt"):
        self.L = instaloader.Instaloader()
        with open(proxies_file, 'r') as f:
            self.all_proxies = [line.strip() for line in f if line.strip()]
            self._set_random_proxy()

        # try:
        #     # Try loading session from file
        #     self.L.load_session_from_file( "salamgetpost")
        # except instaloader.InstaloaderException as e:
        #     print(f"Session not loaded: {e}")
        #     # If session loading fails, login
        #     self.L.context.log_in("salamgetpost", "SalamCity@2023")
        #     # Save the session to file for future use
        #     self.L.save_session_to_file("salamgetpost")
        # self.L = instaloader.Instaloader()
        # session_file = os.path.join(os.getcwd(), "salamgetpost2_session")

        # try:
        #     # Try loading session from file
        #     # self.L.load_session_from_file(session_file, "salamgetpost_session")
        #     self.L.load_session_from_file( "salamgetpost")

        #     print("loading session")
        # except (instaloader.InstaloaderException, FileNotFoundError) as e:
        #     print(f"Session not loaded: {e}")
        #     # If session loading fails, login
        #     self.L.context.login("salamgetpost2", "SalamCity@2023")
        #     print("logged in")
        #     # Save the session to file for future use
        #     dir_path = "C:\\Users\\marwa\\Documents"
        #     session_file = os.path.join(dir_path, "salamgetpost2_session")
        #     self.L.save_session_to_file(session_file)
    
    def get_latest_posts(self, username, max_posts=3):
        try :
            print("getting latest posts for", username)
            profile = instaloader.Profile.from_username(self.L.context, username)
            print("profile", profile)
            posts = profile.get_posts()
            print("posts", posts.count)
            count = 0
            latest_posts = []
            skip_count = 2 if username.lower() == "carletonmsa" else 0
            skip_count = 1 if username.lower() == "algonquinmsa_" else 0

            for post in posts:
                print("post", post.url)
                if count < skip_count:
                    count += 1
                    continue
                elif post.is_video:
                    continue
                else:
                    latest_posts.append(post)
                count += 1
                if count == max_posts:
                    break

            posts = []
            for post in latest_posts:
                print("getting post", post.url)
                single_post = {}
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
                        single_post["image"] = image
                        single_post["description"] = post.caption
                        single_post["link"] = "https://www.instagram.com/p/" + post.shortcode
                        single_post["username"] = username
                        single_post["userid"] = profile.userid
                        single_post["is_video"] = post.is_video
                        posts.append(single_post)
                        # posts.append((post.caption, image, username, profile.userid, "https://www.instagram.com/p/" + post.shortcode))
                    else:
                        single_post["image"] = ""
                        single_post["description"] = post.caption
                        single_post["link"] = "https://www.instagram.com/p/" + post.shortcode
                        single_post["username"] = username
                        single_post["userid"] = profile.userid
                        single_post["is_video"] = post.is_video
                        posts.append(single_post)
                        # posts.append((post.caption, post.url, username, profile.userid, "https://www.instagram.com/p/" + post.shortcode))
                else:
                    single_post["image"] = ""
                    single_post["description"] = post.caption
                    single_post["link"] = "https://www.instagram.com/p/" + post.shortcode
                    single_post["username"] = username
                    single_post["userid"] = profile.userid
                    posts.append(single_post)
                    # posts.append((post.caption, post.url, username, profile.userid, "https://www.instagram.com/p/" + post.shortcode))

            print("posts", posts)
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
    def _set_random_proxy(self):
        """Pick one random proxy from the list and set it in Instaloader's session."""
        chosen_proxy = random.choice(self.all_proxies)
        # If you want HTTP and HTTPS to point to the same IP:port:
        proxies_dict = {
            'http':  f'http://{chosen_proxy}',
            'https': f'http://{chosen_proxy}'
        }
        # Assign the proxies to Instaloader's underlying requests.Session object
        self.L.context._session.proxies = proxies_dict
        print(f"Using proxy: {chosen_proxy}")
    
    # def update(self):
    #     self.L.close()
    #     self.L = instaloader.Instaloader()
    #     self.L.login("salamgetpost2", ",.@2023")