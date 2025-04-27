# file: utils/browser.py
from playwright.sync_api import sync_playwright
import random

def get_html(url, proxy_list=None, headless=True, timeout=60000):
    """
    Opens a browser context with Playwright, optionally using a proxy (rotated from the given list),
    navigates to the URL, and returns the rendered HTML content.
    """
    selected_proxy = None
    if proxy_list:
        # Choose a random proxy from the list
        selected_proxy = random.choice(proxy_list)
    
    with sync_playwright() as p:
        launch_options = {"headless": headless}
        # Launch browser
        browser = p.chromium.launch(**launch_options)
        
        # Create a new context with proxy option if available
        context_args = {}
        if selected_proxy:
            # Example: "http://username:password@proxyserver:port"
            context_args["proxy"] = {"server": selected_proxy}
        
        context = browser.new_context(**context_args)
        page = context.new_page()
        # Go to the URL and wait for full render
        page.goto(url, timeout=timeout)
        # Optionally, wait for network idle or for a selector:
        # page.wait_for_load_state("networkidle")
        content = page.content()
        context.close()
        browser.close()
    return content
