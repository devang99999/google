'''import os
import json
import time
import random
from datetime import datetime
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# === Setup ===
os.makedirs("logs", exist_ok=True)
os.makedirs("data/urls", exist_ok=True)

CATEGORIES = [
    "best food in ahmedabad",
    "vayu app"
]

def extract_urls(html, query):
    soup = BeautifulSoup(html, "html.parser")
    urls = []
    for a in soup.select('a[href^="/url?q="]'):
        href = a['href'].split("/url?q=")[1].split("&")[0]
        if "google.com" not in href and "youtube.com" not in href:
            urls.append(href)

    # Save HTML
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    with open(f"logs/{query.replace(' ', '_')}_{timestamp}.html", "w", encoding="utf-8") as f:
        f.write(html)

    return list(dict.fromkeys(urls))  # De-duplicate

def run_search(playwright, query):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent=random_user_agent(),
        viewport={"width": 1280, "height": 800}
    )
    page = context.new_page()

    print(f"➡️  Searching for: {query}")
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&num=20"
    page.goto(search_url, timeout=30000)
    page.wait_for_timeout(random.randint(3000, 5000))  # Wait 3–5s

    # Simulate human behavior: scroll & hover
    page.mouse.move(200, 300)
    page.mouse.move(300, 400)
    page.mouse.wheel(0, 500)
    page.wait_for_timeout(random.randint(1000, 2000))

    html = page.content()
    browser.close()
    return extract_urls(html, query)

def save_urls(query, urls):
    filename = f"data/urls/{query.replace(' ', '_')}.json"
    with open(filename, "w") as f:
        json.dump(urls, f, indent=2)
    print(f"📝 Saved {len(urls)} URLs to {filename}\n")

def random_user_agent():
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0",
        "Mozilla/5.0 (Windows NT 10.0; rv:111.0) Gecko/20100101 Firefox/111.0",
        "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36"
    ]
    return random.choice(agents)

def main():
    with sync_playwright() as playwright:
        for query in CATEGORIES:
            try:
                urls = run_search(playwright, query)
                save_urls(query, urls)
                wait = random.randint(10, 25)
                print(f"⏳ Sleeping for {wait}s to avoid detection...\n")
                time.sleep(wait)
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Google Stealth Scraper Started")
    main()
    print("✅ All done!")
'''


'''
2captcha

import os
import json
import time
import random
from datetime import datetime
from bs4 import BeautifulSoup
from twocaptcha import TwoCaptcha
from playwright.sync_api import sync_playwright

# 2Captcha config (replace with your real API key)
solver = TwoCaptcha('YOUR_2CAPTCHA_API_KEY')

# Folder setup
os.makedirs("logs", exist_ok=True)
os.makedirs("data/urls", exist_ok=True)

# Categories (you can load from a JSON file if you prefer)
CATEGORIES = [
    "best food in ahmedabad",
    "vayu app"
]

def solve_captcha(page):
    print("⚠️ CAPTCHA detected. Attempting to solve...")
    site_key = page.query_selector('div.g-recaptcha').get_attribute('data-sitekey')
    url = page.url

    try:
        result = solver.recaptcha(sitekey=site_key, url=url)
        token = result['code']
        page.evaluate(f'document.getElementById("g-recaptcha-response").innerHTML="{token}";')
        page.click("#recaptcha-demo-submit")
        print("✅ CAPTCHA solved and submitted.")
        time.sleep(5)
    except Exception as e:
        print(f"❌ Failed to solve CAPTCHA: {e}")

def extract_urls(html, query):
    soup = BeautifulSoup(html, "html.parser")
    urls = []

    for a in soup.select('a[href^="/url?q="]'):
        href = a['href'].split("/url?q=")[1].split("&")[0]
        if "google.com" not in href and "youtube.com" not in href:
            urls.append(href)

    # Save raw HTML
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    with open(f"logs/{query.replace(' ', '_')}_{timestamp}.html", "w", encoding="utf-8") as f:
        f.write(html)

    return list(dict.fromkeys(urls))  # deduplicate

def run_search(playwright, query):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    page = context.new_page()

    print(f"➡️  Searching for: {query}")
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}&num=20"
    page.goto(url, timeout=30000)
    time.sleep(random.uniform(3, 5))

    # Detect and handle CAPTCHA
    if page.query_selector('div.g-recaptcha'):
        solve_captcha(page)
        time.sleep(5)

    html = page.content()
    urls = extract_urls(html, query)
    browser.close()
    return urls

def save_urls(query, urls):
    filename = f"data/urls/{query.replace(' ', '_')}.json"
    with open(filename, "w") as f:
        json.dump(urls, f, indent=2)
    print(f"📝 Saved {len(urls)} URLs to {filename}\n")

def main():
    with sync_playwright() as playwright:
        for query in CATEGORIES:
            try:
                urls = run_search(playwright, query)
                save_urls(query, urls)
                time.sleep(random.randint(8, 20))
            except Exception as e:
                print(f"❌ Error with query '{query}': {e}")

if __name__ == "__main__":
    print("🚀 Starting Google Search Scraper with Playwright + 2Captcha")
    main()
    print("✅ All done!")



'''