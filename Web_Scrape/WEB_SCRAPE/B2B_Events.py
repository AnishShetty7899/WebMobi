import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class B2BEventScraper:
    def __init__(self):
        self.event_details = []

    def initialize_webdriver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    def get_page_source(self, url):
        driver = self.initialize_webdriver()
        driver.get(url)
        page_source = driver.page_source
        driver.quit()
        return page_source

    def scrape_event1(self):
        url='https://b2bmarketing.exchange/'
        page= self.get_page_source(url)

        soup = BeautifulSoup(page, "html.parser")
        title = "B2B Marketing Exchange"
        dates = soup.find_all("span", attrs={'class': 'elementor-icon-list-text'})[0].get_text().strip()
        location = soup.find_all("span", attrs={'class': 'elementor-icon-list-text'})[1].get_text().strip()
        description_elements = soup.find_all('span', class_='NormalTextRun SCXW200178519 BCX0')
        description = ' '.join([desc.get_text().strip() for desc in description_elements])
        speakers = "No Details"

        # Scrape agenda
        driver = self.initialize_webdriver()
        url1 = "https://b2bmarketing.exchange/east/agenda/"
        driver.get(url1)

        wait = WebDriverWait(driver, 10)
        try:
            iframe = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'iframe[src*="swapcard.com/widget/event/b2b-marketing-exchange-east-2024"]')))
            driver.switch_to.frame(iframe)
        except:
            pass

        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sc-dab8fe09-5')))
        page1 = driver.page_source
        driver.quit()

        soup3 = BeautifulSoup(page1, "html.parser")
        ag_h3 = soup3.find_all("h3", attrs={"class": "sc-dab8fe09-5 fwiXyw"})
        agenda = [h3.get_text() for h3 in ag_h3]
        agendas = ", ".join(agenda)

        # Scrape registration details
        driver = self.initialize_webdriver()
        url2 = "https://b2bmarketing.exchange/east/registration/"
        driver.get(url2)
        page2 = driver.page_source
        driver.quit()

        soup5 = BeautifulSoup(page2, "html.parser")
        soup6 = BeautifulSoup(soup5.prettify(), "html.parser")
        rg_details = f'Can register through this link. {url2}'

        # Scrape pricing
        price_elements = soup6.find_all("div", attrs={"class": "elementor-price-table__price"})
        prices = []
        for element in price_elements:
            p = element.find("span", attrs={"class": "elementor-price-table__integer-part"})
            pr = p.get_text().strip()
            prices.append(pr)
        final_price = ", ".join(prices)

        self.event_details.append({
            "Event Name": title,
            "Event Date(s)": dates,
            "Location": location,
            "Website URL": url,
            "Description": description,
            "Key Speakers": speakers,
            "Agenda": agendas,
            "Registration Details": rg_details,
            "Price": final_price,
            "Categories": "B2B Marketing Summit",
            "Audience type": "All"
        })

    def scrape_event2(self):
        try:
            url = "https://www.b2bmarketingexpo.us/"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "DNT": "1",
                "Connection": "close",
                "Upgrade-Insecure-Requests": "1"
            }

            # Connect to the website
            page = requests.get(url, headers=headers)
            soup = BeautifulSoup(page.content, "html.parser")

            # Initialize default values
            default = 'B2B Marketing Summit'
            event_details = {
                "Event Name": default,
                "Event Date(s)": "",
                "Location": "",
                "Website URL": url,
                "Description": "",
                "Key Speakers": "",
                "Agenda": "",
                "Registration Details": "",
                "Price": "",
                "Categories": default,
                "Audience type": "All"
            }

            # Extract event details
            # Title
            title_elem = soup.find("h1", class_='panel__header__title')
            if title_elem:
                event_details["Event Name"] = title_elem.get_text().strip()

            # Event Dates and Location
            date_loc = soup.find_all("h3", class_='ck-strapline--colour-white')

            date = []
            for dat in date_loc:
                dat_text = dat.get_text().strip()
                dates = dat_text.split(' - ')[1]
                date.append(dates)
            Dates = ', '.join(date)
            event_details["Event Date(s)"] = Dates

            loca = []
            for loc in date_loc:
                loc_text = loc.get_text().strip()
                location = loc_text.split(' - ')[0]
                loca.append(location)
            locations = ', '.join(loca)
            event_details["Location"] = locations

            # Description
            description_elem = soup.find("p", class_='ck-intro-text')
            if description_elem:
                event_details["Description"] = description_elem.get_text().strip()

            # Key Speakers
            speaker_names = []
            speakers_url = "https://www.b2bmarketingexpo.us/2022-speakers"
            speakers_page = requests.get(speakers_url, headers=headers)
            speakers_soup = BeautifulSoup(speakers_page.content, "html.parser")
            div_speakers = speakers_soup.find_all("div", class_='section section--one-column section--id-3')
            for div in div_speakers:
                key_speakers = div.find_all("a",
                                            class_='m-speakers-list__items__item__header__title__link js-librarylink-entry')
                for key in key_speakers:
                    speaker_names.append(key.get_text().strip())
            event_details["Key Speakers"] = ", ".join(speaker_names)

            # Agenda
            agenda_items = []
            agenda_url = "https://www.b2bmarketingexpo.us/seminar-agenda"
            agenda_page = requests.get(agenda_url, headers=headers)
            agenda_soup = BeautifulSoup(agenda_page.content, "html.parser")
            agenda_divs = agenda_soup.find_all("div", class_='m-seminar-list__list__items__item__title')
            for div in agenda_divs:
                agenda_links = div.find_all("a", class_='js-librarylink-entry')
                for link in agenda_links:
                    agenda_items.append(link.get_text().strip())
            event_details["Agenda"] = ", ".join(agenda_items)

            # Registration Details and Price
            reg_details = "Check the official website for registration details"
            rg_details = soup.find_all("div", attrs={'class': 'panel__body'})
            for div in rg_details:
                # Finding the first registration type
                rg_type1 = div.find('a', class_='ck-button-one')
                if rg_type1:
                    rg_type1_text = rg_type1.get_text().strip()

                # Finding the second registration type
                rg_type2 = div.find('a', class_='ck-button-two')
                if rg_type2:
                    rg_type2_text = rg_type2.get_text().strip()

                # Combine registration types
                if rg_type1 and rg_type2:
                    reg_details = f'It has two types of bookings: {rg_type1_text} and {rg_type2_text}.'
                    break
            price = "N/A"  # Update with actual price if available
            event_details["Registration Details"] = reg_details
            event_details["Price"] = price

            self.event_details.append(event_details)

        except Exception as e:
            print(f"Error occurred: {e}")

    def scrape_event3(self):
        driver = self.initialize_webdriver()
        url = "https://www.sales30conf.com/sales-conference-june2024/?sp_src=upcoming_event"
        driver.get(url)
        page_source = driver.page_source
        driver.quit()

        soup = BeautifulSoup(page_source, "html.parser")
        title = "Sales 3.0 Conference"
        date = soup.find_all("div", attrs={"class": "pricingDescription"})[0].find("span", attrs={
            "style": "color:#333333;"}).get_text().strip()
        dates = " ".join(date.split()[14:])
        audience_type = []
        audience_elements = soup.find_all("div", attrs={"class": "floatRight padding"}) + soup.find_all("div", attrs={
            "class": "floatLeft padding"})
        for elem in audience_elements:
            audience_type.extend(
                [audience.get_text().strip() for audience in elem.find_all("span", attrs={"style": "color:#333333;"})])
        audience_type = ", ".join(audience_type) if audience_type else "All"

        description = "N/A"

        speakers_url = "https://www.sales30conf.com/sales-conference-june2024/speakers.html?sp_src=june2024-header-txt-speakers"
        speakers_page = self.get_page_source(speakers_url)
        soup_speakers = BeautifulSoup(speakers_page, "html.parser")
        speaker_names = [speaker.get_text().strip() for speaker in soup_speakers.find_all("span", class_='red_speaker')]
        speakers = ", ".join(speaker_names) if speaker_names else "No Speakers Found"

        agenda_url = "https://www.sales30conf.com/sales-conference-june2024/agenda.html"
        agenda_page = self.get_page_source(agenda_url)
        soup_agenda = BeautifulSoup(agenda_page, "html.parser")
        agenda_items = [agenda.get_text().strip() for agenda in soup_agenda.find_all("div", class_='AgendaSession')]
        agenda = ", ".join(agenda_items) if agenda_items else "No Agenda Found"
        registration_details = "Can register through this link: https://sales30conference.swoogo.com/june2024/begin?ref=june2024-header-txt-register"
        price = soup.find("div",
                          attrs={"class": "pricingRate"}).get_text().strip()  # Update with actual price if available

        self.event_details.append({
            "Event Name": title,
            "Event Date(s)": dates,
            "Location": "Virtual Event",
            "Website URL": url,
            "Description": description,
            "Key Speakers": speakers,
            "Agenda": agenda,
            "Registration Details": registration_details,
            "Price": price,
            "Categories": "B2B Marketing Summit",
            "Audience type": audience_type
        })

    def scrape_event4(self):
        driver = self.initialize_webdriver()
        url = "https://www.leadscon.com/"
        driver.get(url)
        page_source = driver.page_source
        driver.quit()

        soup = BeautifulSoup(page_source, "html.parser")
        title = soup.find("div", attrs={'class': 'col-xs-12 col-sm-4 blue'}).find("div", attrs={
            'class': 'mb-2'}).get_text().strip()

        event_date = ""
        Event_Dates = soup.find_all("div", attrs={'class': 'small'})
        for date in Event_Dates:
            dat = date.find("div", attrs={'class': 'mb-1'})
            if dat:
                event_date = dat.get_text().strip()
                break  # Stop after finding the first valid date

        loca = ""
        locations = soup.find_all("div", attrs={'class': 'small'})
        for loc in locations:
            loc_text = loc.find("div", attrs={'class': ''})
            if loc_text:
                loca = " ".join(loc_text.get_text().split())
                break

        options1 = webdriver.ChromeOptions()
        options1.add_argument("--headless")
        service1 = Service(ChromeDriverManager().install())
        driver1 = webdriver.Chrome(service=service1, options=options1)

        # Connect to the event details page
        url1 = "https://www.leadscon.com/event/leadscon-connect-2024/"
        driver1.get(url1)
        page1 = driver1.page_source
        driver1.quit()

        Soup3 = BeautifulSoup(page1, "html.parser")
        Soup4 = BeautifulSoup(Soup3.prettify(), "html.parser")

        # Extract description
        description = Soup4.find("p", class_='intro').get_text().strip()
        final_description = description.split(".")[0]

        # Extract speakers
        div_speakers = Soup4.find_all("div", attrs={'class': 'evtx-container evtx-view-wrapper'})
        speaker_names = []
        for div in div_speakers:
            key_speakers = div.find_all("h4", attrs={'class': 'evtx-profile-title'})
            for key in key_speakers:
                key_speaker = key.get_text().strip()
                speaker_names.append(key_speaker)
        speakers = ", ".join(speaker_names)

        # Extract agenda
        ag_div = Soup4.find_all("div", attrs={'class': 'evtx-container evtx-view-wrapper'})
        agenda = []
        for ag in ag_div:
            agendas = ag.find_all("h3", attrs={'class': 'evtx-session-title'})
            for a in agendas:
                agend = a.get_text().strip()
                agenda.append(agend)
        agendas = ", ".join(agenda)

        # registration and pricing
        # Setup Selenium with Chrome using the webdriver-manager
        options2 = webdriver.ChromeOptions()
        options2.add_argument("--headless")  # Run in headless mode (optional)

        # Initialize the WebDriver using the ChromeDriverManager to automatically handle driver installation
        service2 = Service(ChromeDriverManager().install())
        driver2 = webdriver.Chrome(service=service2, options=options2)

        # connect to website
        url2 = "https://accessintel.swoogo.com/leadsconconnect2024/4623071"
        driver2.get(url2)

        page2 = driver2.page_source
        driver2.quit()

        Soup5 = BeautifulSoup(page2, "html.parser")
        Soup6 = BeautifulSoup(Soup5.prettify(), "html.parser")
        # registration details
        rg_details = f'Can register through this link. {url2}'

        # pricing
        price = Soup6.find_all("strong")
        price1 = price[3]
        prices = price1.get_text().strip()

        self.event_details.append({
            "Event Name": title,
            "Event Date(s)": event_date,
            "Location": loca,
            "Website URL": url,
            "Description": final_description,
            "Key Speakers": speakers,
            "Agenda": agendas,
            "Registration Details": rg_details,
            "Price": prices,
            "Categories": "B2B Marketing Summit",
            "Audience type": "All"
        })

    def scrape_event5(self):
        url = "https://b2bmarketing.wbresearch.com/"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}

        page = requests.get(url, headers=headers)

        Soup1 = BeautifulSoup(page.content, "html.parser")
        soup = BeautifulSoup(Soup1.prettify(), "html.parser")
        # title
        title = "B2b Online"
        # date
        Event_Dates = soup.find("p", attrs={'class': 'data'}).get_text().strip()
        # location
        locations = soup.find("p", attrs={'class': 'venue'}).get_text().strip()
        # Description
        discription = soup.find("h1", attrs={'class': 'text-white text-shadow text-bold fa-1x'}).get_text().strip()
        # speaker
        Speaker = "N/A"
        # agengda
        agenda = soup.find("p", attrs={'class': 'fa-lg'}).get_text().strip()

        # pricing
        url1 = "https://b2bmarketing.wbresearch.com/srspricing"
        page1 = requests.get(url1, headers=headers)

        Soup3 = BeautifulSoup(page1.content, "html.parser")
        Soup4 = BeautifulSoup(Soup3.prettify(), "html.parser")
        # price
        p = []
        price = Soup4.find_all("span", attrs={'class': 'srsprice_box_is'})
        for i in price:
            prices = i.get_text().strip()
            p.append(prices)
        Price = ", ".join(p)

        # registration details
        rg_details = f'Can register through this link. https://b2bmarketing.wbresearch.com/srspricing'

        self.event_details.append({
            "Event Name": title,
            "Event Date(s)": Event_Dates,
            "Location": locations,
            "Website URL": url,
            "Description": discription,
            "Key Speakers": Speaker,
            "Agenda": agenda,
            "Registration Details": rg_details,
            "Price": Price,
            "Categories": "B2B Marketing Summit",
            "Audience type": "All"
        })

    def combine_event_details(self):
        self.scrape_event1()
        self.scrape_event2()
        self.scrape_event3()
        self.scrape_event4()
        self.scrape_event5()

    def save_to_csv(self, filename='B2B_Summit_Events.csv'):
        df = pd.DataFrame(self.event_details)
        df.head()
        df.to_csv(filename, index=False)
        print(f"Event details saved to '{filename}' successfully.")
        return df




if __name__ == "__main__":
    scraper = B2BEventScraper()
    scraper.combine_event_details()
    df = scraper.save_to_csv()
    print(df)
