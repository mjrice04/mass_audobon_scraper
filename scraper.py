"""
Requirements Take 1

Takes in list of mass audobon locations
Able to scrape the events coming up in the month
Able to tune parameters of search


Able to email this list to my email

"""

import requests
from lxml import html
from typing import List
import sys
import csv,os,json
from time import sleep
import datetime

class AudobonScraper:
    def __init__(self, site_list: List[str]):
        self.base_url = 'https://www.massaudubon.org/program-catalog/results/'
        self.site_list = site_list

    def clean_raw_xpath(self, result_list: List[str], url=False):
        clean_data = [' '.join(''.join(raw_item).split()) for raw_item in result_list]
        if url:
            clean_data = [f"{self.base_url}{url}" for url in clean_data]
        return clean_data


    def parser(self):
        for url in self.site_list:
            full_url = f"{self.base_url}{url}"
            page = requests.get(full_url)
            doc = html.fromstring(page.content)
            xpath_event_date = ('//div[@class="short-results-program-listings-divs"]'
                                '/div[@class="next-meeting-date-divs"]/text()')
            xpath_event_time = ('//div[@class="short-results-program-listings-divs"]'
                                '/div[@class="next-meeting-time-divs"]/text()')
            xpath_event_group = ('//div[@class="audience-search-form-divs"]'
                                 '/div[@class="audience-indicator-divs"]/text()')
            xpath_event_link = ('//div[@class="short-results-program-listings-divs"]'
                                '/div[@class="attribute-title program-title-and-location-divs"]//a/@href')
            xpath_event_name = ('//div[@class="short-results-program-listings-divs"]'
                                '/div[@class="attribute-title program-title-and-location-divs"]//a/text()')
            xpath_event_location = '//div[@class="location-official-name-divs"]/text()'
            raw_list = [xpath_event_date, xpath_event_time, xpath_event_group, xpath_event_name,
                        xpath_event_link, xpath_event_location]
            clean_events = []
            for item in raw_list:
                raw_xpath = doc.xpath(item)
                if item == xpath_event_link:
                    event = self.clean_raw_xpath(raw_xpath, url=True)
                else:
                    event = self.clean_raw_xpath(raw_xpath)
                clean_events.append(event)
            return clean_events

    def data_handler(self, clean_events):
        data_json = {}
        len_list = [len(x) for x in clean_events]
        all_events = all(x == len_list[0] for x in len_list)
        if not all_events:
            # If for whatever reason events are unequal (the scraper needs to be altered)
            sys.exit("Scraper failed. Please look into parser script")
        events = []
        event_count = len(clean_events[0])
        for i in range(event_count):
            event_item = []
            # 6 fields I care about
            event_item.append(clean_events[0][i])
            event_item.append(clean_events[1][i])
            event_item.append(clean_events[2][i])
            event_item.append(clean_events[3][i])
            event_item.append(clean_events[4][i])
            event_item.append(clean_events[5][i])
            events.append(event_item)
        return events

    def search_params(self):
        pass

    def run(self):
        clean_list = self.parser()
        events = self.data_handler(clean_list)
        return events

if __name__ == "__main__":
    site_list = ['greater-boston']
    scraper = AudobonScraper(site_list)
    events = scraper.run()
    print(events[1])





