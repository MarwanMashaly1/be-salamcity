import instaloader
from base64 import b64encode
import requests
from io import BytesIO
import os

class InstagramScraper:
    # the class should have all the function that are below nad it should be able to return the data and the constructor should initialize the instaloader and login 
    def __init__(self):
        # self.L = instaloader.Instaloader()
        # try:
        #     # Try loading session from file
        #     self.L.load_session_from_file( "salamgetpost")
        # except instaloader.InstaloaderException as e:
        #     print(f"Session not loaded: {e}")
        #     # If session loading fails, login
        #     self.L.context.log_in("salamgetpost", "SalamCity@2023")
        #     # Save the session to file for future use
        #     self.L.save_session_to_file("salamgetpost")
        self.L = instaloader.Instaloader()
        session_file = os.path.join(os.getcwd(), "salamgetpost_session")

        try:
            # Try loading session from file
            self.L.load_session_from_file(session_file, "salamgetpost_session")
        except (instaloader.InstaloaderException, FileNotFoundError) as e:
            print(f"Session not loaded: {e}")
            # If session loading fails, login
            self.L.context.login("salamgetpost", "SalamCity@2023")
            # Save the session to file for future use
            self.L.save_session_to_file(session_file)
    
    def get_latest_posts(self, username):
        try :
            profile = instaloader.Profile.from_username(self.L.context, username)
            posts = profile.get_posts()
            count = 0
            latest_posts = []
            skip_count = 2 if username.lower() == "carletonmsa" else 0
            total_posts = 2

            for post in posts:
                if count < skip_count:
                    count += 1
                    continue
                if post.is_pinned:
                    print("pinned post: ", post.url)
                else:
                    latest_posts.append(post)

                count += 1

                if count == total_posts:
                    break

            posts = []

            for post in latest_posts:
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
                        posts.append(single_post)
                        # posts.append((post.caption, image, username, profile.userid, "https://www.instagram.com/p/" + post.shortcode))
                    else:
                        single_post["image"] = ""
                        single_post["description"] = post.caption
                        single_post["link"] = "https://www.instagram.com/p/" + post.shortcode
                        single_post["username"] = username
                        single_post["userid"] = profile.userid
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