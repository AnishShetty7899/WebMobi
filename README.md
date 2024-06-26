# B2B Event Scraper

## Overview
This Python script is designed to scrape data from multiple B2B event websites. It collects information such as event dates, location, description, key speakers, agenda, registration details, pricing, categories, and audience type. The scraped data is then stored in a CSV file named `B2B_Summit_Events.csv` for further analysis and reference.

## Prerequisites
Before running the script, ensure you have the following installed:

- Python (latest version)
- Required Python libraries (install using `pip install -r requirements.txt`):
  - requests
  - beautifulsoup4
  - pandas

## Usage
1. Modify the `events_info` list in `B2B_Events.py` to include the events you want to scrape. Each event should have a dictionary with at least the name and homepage URL. For events with registration or agenda URLs, provide those as well.

2. Run the script:
   ```python
   !python scrape_events.py

Data for each event will be printed to the console as it's scraped.

View the Data:

After the script finishes running, you will find a file named B2B_Summit_Events.csv in the same directory. This CSV file contains all the collected data structured in a tabular format.

Data Collected

The script collects the following information for each event:
  - Event Name
  - Event Date(s)
  - Location
  - Website URL
  - Description
  - Key Speakers
  - Agenda
  - Registration Details
  - Pricing
  - Categories
  - Audience type

Note: The output CSV file may contain incomplete or minimal details depending on the availability and structure of data on the event websites. Some fields may appear as "N/A" if the information couldn't be retrieved.


