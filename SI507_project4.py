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

ul_links = ul_states.find_all('a')

list_of_state_names = []
for href in ul_links:
     list_of_state_names.append(href.text)

sorted_list_of_state_names = sorted(list_of_state_names)
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
state_dict = {}
state_list = []

for state in topics_pages:
    # state = BeautifulSoup(state, features="html.parser")

    if count >= 3:
        break
    else:
        # print (type(state))
        # print (state.prettify())
        target_li = state.find_all('div',{'class':'col-md-9 col-sm-9 col-xs-12 table-cell list_left'})
        for li in target_li:
            # print ("*********\n")
            # print (li)
            # print ("*********\n")

            # print("getting tag text")
            # print ("*********\n")

            site_name = li.find("h3").text
            site_type = li.find("h2").text
            site_discription = li.find("p").text.strip( '\n' )
            # print (site_discription)
            site_location = li.find("h4").text

            # create a list of site info and add list to overall state list.
            # print("creating list with site info")
            list = [site_name, site_type, site_discription, site_location]

            # print ("adding list to mega list")
            state_list.append(list)

            # add state to state dict, where key is state and value is list of all site info
        current_state = sorted_list_of_state_names[count]
        STATES_DICT[current_state] = state_list

        count += 1



print (STATES_DICT)



with open ("some_file.json", "w") as fh:
    json_object = json.dumps(STATES_DICT)
    fh.write(json_object)
#

##extracting urls found within pages
# for link in soup.find_all('a'):
#     print(link.get('href'))
# http://example.com/elsie
# http://example.com/lacie
# http://example.com/tillie

##1 row = 1 national site

#Code for caching data on json file
