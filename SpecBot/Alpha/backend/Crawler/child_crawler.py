import requests
import sys
import os
import signal

from urllib.parse import urlparse
from bs4 import BeautifulSoup
from time import sleep

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoAlertPresentException

from helpers import find_all_domain_links, find_all_forms_with_methods, \
                    write_to_json, path_based_on_os, signal_handler

is_cloud = 'CLOUD' in os.environ
signal.signal(signal.SIGINT, signal_handler)

sys.path.append(path_based_on_os(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/..")))
from aws_helper import upload_dict_to_s3, send_to_sqs, poll_from_sqs
from constants import CHILD_SQS, CHILD_SQS_RESULT, CHILD_BUCKET, CHILD_DATA_FILENAME

class ChildCrawler:
    def __init__(self, start_url):
        chrome_service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service = chrome_service)
        self.start_url = start_url
        self.pages_data = {}
        parsed_url = urlparse(self.start_url)
        self.base_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
        self.visited_links = set()
        self.links_to_visit = ["/"]

    def send_data(self):
        if is_cloud:
            bucket_path = f'{self.start_url}/{CHILD_DATA_FILENAME}'
            print(f'Uploading child data to {CHILD_BUCKET} S3')
            upload_dict_to_s3(CHILD_BUCKET, bucket_path, self.pages_data)
            print('Done')

            print(f'Posting child bucket path to {CHILD_SQS_RESULT} SQS')
            send_to_sqs(CHILD_SQS_RESULT, bucket_path)
            print('Done')
        else:
            write_to_json(CHILD_DATA_FILENAME, self.pages_data)

    def begin_scrapping(self) -> dict:
        while self.links_to_visit:
            link_to_visit = self.links_to_visit.pop(0)
            if link_to_visit in self.visited_links: continue

            url = self.start_url + link_to_visit
            print(f'Scrapping: {url}')
            domain_links = self.__extract_page_data(url)

            # remove visited url and add everything else
            self.visited_links.add(link_to_visit)
            self.links_to_visit += list(domain_links)
            self.links_to_visit = list(set(self.links_to_visit))

        self.driver.quit()
        self.pages_data['all_urls'] = [self.base_url + link for link in self.visited_links]
        return self

    def __extract_page_data(self, url) -> set:
        self.driver.get(url)
        # sleep(2) # make sure most of things load
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
        except NoAlertPresentException:
            pass

        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        links = find_all_domain_links(soup, url)
        forms = find_all_forms_with_methods(soup)
        domain_links = set(link for link in links if link and link.startswith('/') and not link == '/')

        self.pages_data[url] = {
            'headers': dict(page.headers),
            'status_code': page.status_code,
            'content': page.text,
            'links': list(domain_links),
            'forms': forms,
            'console_logs': self.driver.get_log('browser'),
            'source_code': self.driver.page_source
        }
        return domain_links

while True:
    if is_cloud:
        start_url = poll_from_sqs(CHILD_SQS)
    else:
        # start_url = sys.argv[1]
        # start_url = "http://testphp.vulnweb.com"
        start_url = "https://public-firing-range.appspot.com/reverseclickjacking/singlepage/ParameterInQuery/OtherParameter/?q=%26callback%3Durc_button.click%23"
        # start_url = "https://www.realpython.com"
    ChildCrawler(start_url).begin_scrapping().send_data()