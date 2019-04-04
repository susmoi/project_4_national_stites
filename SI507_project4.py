from bs4 import BeautifulSoup
import requests
import json
import csv

from advanced_expiry_caching import Cache

#scrapy scraping libray

#Code for scraping data from national websites
##NAME of site
##TYPE of site
##DESCRIPTION of site
##LOCATION (in any form Richmond; Richmond, VA; VA)
##CHALLENGE standarize state names

#Constants
FNAME = "national_sites_cache.json"
START_URL = "https://www.nps.gov"

PROGRAM_CACHE = Cache(FNAME)

def scrape_function(some_url):
    data = PROGRAM_CACHE.get_data(some_url)
    if not data:
        data = requests.get(some_url).text
        PROGRAM_CACHE.set(some_url, data)
    return data

main_page = scrape_function(START_URL)

main_soup = BeautifulSoup(main_page, features="html.parser")
ul_states = main_soup.find("ul",{"class":"dropdown-menu"})

# print (list_of_states)
ul_links = ul_states.find_all('a')

list_of_state_names = []
for href in ul_links:
     list_of_state_names.append(href.text)

crawl_links = []

for item in ul_links:
    link = "{}{}".format(START_URL, item.get("href"))
    crawl_links.append(link)
# print(crawl_links)

# Need to scrape each state link for national sites.
count = 0
state_csv = "state_csv_file.csv"
state_dict = {}

for state_link in crawl_links:
    count += 1
    print (state_link)
    page_data = scrape_function(state_link)
    state_page_soup = BeautifulSoup(page_data, features="html.parser")
    # print (state_page_soup)
    tags = state_page_soup.find_all('li',{'class':'clearfix'})
    print (tags)
    # site_name = tag.find("h3").text
    # site_type = tag.find("h2").text
    # site_discription = tag.find("p").text.strip( '\n' )
    # site_location = tag.find("h4").text
    #
    # state_list = [site_name, site_type, site_discription, site_location]
    # state_dict[site_location] = state_list


    if count >= 1:
        break
# print (state_dict)

##extracting urls found within pages
# for link in soup.find_all('a'):
#     print(link.get('href'))
# http://example.com/elsie
# http://example.com/lacie
# http://example.com/tillie

##1 row = 1 national site

#Code for caching data on json file
