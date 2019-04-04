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
topics_pages = []

for state_link in crawl_links:

    # print (state_link)
    page_data = scrape_function(state_link)
    state_page_soup = BeautifulSoup(page_data, features="html.parser")
    topics_pages.append(state_page_soup)
    # print (type(state_page_soup))
STATES_DICT = {}

for state in topics_pages:
    # state = BeautifulSoup(state, features="html.parser")
    count += 1
    if count >= 70:
        break
    else:
        # print (type(state))
        # print (state.prettify())
        target_li = state.find_all('li',{'class':'clearfix'})
        for li in target_li:
            try:
                state_dict = {}
                site_name = li.find("h3").text
                site_type = li.find("h2").text
                site_discription = li.find("p").text.strip( '\n' )
                # print (site_discription)
                site_location = li.find("h4").text

                state_list = [site_name, site_type, site_discription, site_location]
                state_dict[site_location] = state_list
                STATES_DICT[site_location] = state_dict
            except:
                ("NONE TYPE")

        # find('li',{'class':'clearfix'})

# print (STATES_DICT)

with open ("some_file.json", "w") as fh:
    json_object = json.dumps(STATES_DICT)
    fh.write(json_object)
# print (topics_pages[0].prettify())
# for soup in topics_pages[0]:
#     soup = soup.prettify()
#     for park_list in soup.find("ul"):
#
#         print(type(park_list))

    # print (soup.prettify().find(id="list_parks"))

# tags = state_page_soup.find_all('li',{'class':'clearfix'})
# for tag in tags:
#     # print (type(tag))
#
#     if count >= 1:
#         break
#

##extracting urls found within pages
# for link in soup.find_all('a'):
#     print(link.get('href'))
# http://example.com/elsie
# http://example.com/lacie
# http://example.com/tillie

##1 row = 1 national site

#Code for caching data on json file
