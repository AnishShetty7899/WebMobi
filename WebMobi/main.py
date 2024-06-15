import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

# List of event URLs and their respective homepage
events_info = [
    {"name": "B2B Marketing Exchange", "registration_url": "https://b2bmarketing.exchange/east/registration/",
     "agenda_url": "https://b2bmarketing.exchange/east/agenda/", "homepage": "https://b2bmarketing.exchange/"},
    {"name": "B2B Marketing Expo", "url": "https://www.b2bmarketingexpo.us/",
     "homepage": "https://www.b2bmarketingexpo.us/"},
    {"name": "LeadsCon", "url": "https://www.leadscon.com/", "homepage": "https://www.leadscon.com/"},
    {"name": "B2B Online", "url": "https://b2bonlineusa.wbresearch.com/",
     "homepage": "https://b2bonlineusa.wbresearch.com/"},
    {"name": "MARTECH", "url": "https://martech.org/conference/spring/",
     "homepage": "https://martech.org/conference/spring/"}
]


# Function to scrape data from an event website
def scrape_event(event_info):
    registration_url = event_info.get("registration_url")
    agenda_url = event_info.get("agenda_url")
    homepage = event_info["homepage"]

    # Set up retry strategy with exponential backoff
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Initialize a dictionary to store the event details
    event_details = {
        "Event Name": event_info["name"],
        "Event Date(s)": "N/A",
        "Location": "N/A",
        "Website URL": homepage,
        "Description": "N/A",
        "Key Speakers": "N/A",
        "Agenda": "N/A",
        "Registration Details": "N/A",
        "Pricing": "N/A",
        "Categories": "N/A",
        "Audience type": "N/A"
    }

    # Helper function to safely get text
    def safe_get_text(soup, selectors, attr=None, default="N/A"):
        for selector in selectors:
            try:
                if attr:
                    element = soup.select_one(selector)[attr]
                else:
                    element = soup.select_one(selector).get_text(strip=True)
                if element:
                    return element.strip()
            except (AttributeError, TypeError):
                continue
        return default

    # Function to scrape registration page
    def scrape_registration_page():
        try:
            response = http.get(registration_url, headers=headers, timeout=20)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException:
            return None

        # Update with specific selectors for registration details and pricing
        registration_selector = [".elementor-element.elementor-element-d8b9d36 .elementor-text-editor"]
        pricing_selector = [".elementor-element.elementor-element-8f0f9d3 .elementor-text-editor"]

        event_details["Registration Details"] = safe_get_text(soup, registration_selector)
        event_details["Pricing"] = safe_get_text(soup, pricing_selector)

    # Function to scrape agenda page
    def scrape_agenda_page():
        try:
            response = http.get(agenda_url, headers=headers, timeout=20)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException:
            return None

        # Fetching event date(s), location, description, and key speakers
        event_details["Event Date(s)"] = safe_get_text(soup, [".article__body"])
        event_details["Location"] = safe_get_text(soup, [".article__body"])
        event_details["Description"] = safe_get_text(soup, ["meta[name='description']"], "content")
        event_details["Key Speakers"] = ', '.join(
            [speaker.get_text(strip=True) for speaker in soup.select('.speaker-name')])

        # Fetching all agenda items
        agenda_items = soup.select('.elementor-size-default')
        agenda_texts = [agenda.get_text(strip=True) for agenda in agenda_items]
        event_details["Agenda"] = ', '.join(agenda_texts)

    if registration_url:
        scrape_registration_page()
    if agenda_url:
        scrape_agenda_page()

    return event_details


# List to store all event details
events_data = []

# Scrape each event website
for event_info in events_info:
    event_data = scrape_event(event_info)
    if event_data:
        print(f"Data for {event_info['name']}:")
        for key, value in event_data.items():
            print(f"{key}: {value}")
        print("\n")
        events_data.append(event_data)
    time.sleep(1)  # Adding a short delay between requests

# Create a DataFrame and save it to a CSV file
df = pd.DataFrame(events_data)
df.to_csv('b2b_events_2024.csv', index=False)
