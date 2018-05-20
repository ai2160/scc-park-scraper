#!/usr/bin/python
import json
import logging
import urllib
import requests
import time

from robobrowser import RoboBrowser

from secrets import MG_KEY, MG_DOMAIN

found_sites = []
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)

BASE_URL = 'https://gooutsideandplay.org'
REQUEST_PATH = '/Index.asp?actiontype=camping&park_idno={park_id}&arrive_date={start}&res_length={length}'
MG_URL = 'https://api.mailgun.net/v3/{}/messages'.format(MG_DOMAIN)

config = None
with open('config.json') as config_file:
    config = json.loads(config_file.read())

def send_email(mail_body):
    response = requests.post(MG_URL, auth=('api', MG_KEY), data={
        'from': '"SCC Scraper" <camper@westerncamper.photography>',
        'to': ','.join(config['emails']),
        'subject': 'Found SCC camp sites!',
        'text': mail_body
    })

def scrape_info():
    found = []
    for reservation_request in config['reservation_requests']:
        start_date = urllib.parse.quote(reservation_request['start_date'])
        park_id = 0
        if 'park_id' in reservation_request:
            park_id = reservation_request['park_id']
        length = 1
        if 'length' in reservation_request:
            length = reservation_request['length']
        query_path = REQUEST_PATH.format(start=start_date, park_id=park_id, length=length)
        url = BASE_URL + query_path
        browser = RoboBrowser(user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko')
        browser.open(url)
        sites = browser.find('div', {'id': 'list_camping'}).find_all('tr')
        
        for site in sites:
            data = site.find_all('td')
            description = data[1]
            if description.text().lower().find('tent') != -1:
                found.append(url)
                break
        return found

if __name__ == '__main__':
    while 1:
       found = scrape_info()

       if found:
          logger.info('Found some campsites!')
          send_email('\n'.join(found))
       else:
          logger.info('No campsites found')
       time.sleep(300)
