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

def send_email(mail_body, subject):
    response = requests.post(MG_URL, auth=('api', MG_KEY), data={
        'from': '"SCC Scraper" <camper@westerncamper.photography>',
        'to': ','.join(config['emails']),
        'subject': subject,
        'text': mail_body
    })

def valid_campsite(description):
    lower_desc = description.lower()
    if lower_desc.find('horse') != -1:
        return False
    if lower_desc.find('ada') != -1:
        return False
    if lower_desc.find('tent') != -1:
        return True
    return False
    

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
            if valid_campsite(description.text):
                found.append(url)
                break
    return found

if __name__ == '__main__':
    while 1:
        try:
            found = scrape_info()
        except Exception as e:
            send_email(e.args, "Uh oh! Scraper Exception")
            break

        if len(found) > 0:
            logger.info('Found some campsites!')
            site_list = '\n'.join(found)
            logger.info(site_list)
            send_email(site_list, "Yay! Found campsites")
            break
        else:
            logger.info('No campsites found')
        time.sleep(300)
