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
STATE_SITE_LIST = []

for state_page in topics_pages:
    if count >= 56:
        break
    # state = BeautifulSoup(state, features="html.parser")

    else:
        print ("****************new state\n")
        # print(state_page)
        national_sites_divs = state_page.find_all('div',{'class':'col-md-9 col-sm-9 col-xs-12 table-cell list_left'})

        # Loop through the target div elements and grab site name, type, discription, and location

        for div in national_sites_divs:
            local_list = []
            site_name = div.find("h3").text
            site_type = div.find("h2").text
            site_discription = div.find("p").text.strip('\n')
            site_location = div.find("h4").text

            # create a local_list containing the above site info
            local_list = [site_name,site_location, site_type, site_discription]
            STATE_SITE_LIST.append(local_list)
    current_state = sorted_list_of_state_names[count]
    # STATES_DICT[current_state] = state_list
    count += 1



# print (STATE_LIST)


with open ("some_file.csv", "w") as fh:
    writer = csv.writer(fh)
    header = ["Site Name","Site Location","Site Type", "Site discription"]
    writer.writerow(header)
    count = 0
    for site in STATE_SITE_LIST:
        # print (len(STATE_SITE_LIST))
        # print (type(STATE_SITE_LIST))
        # print (len(site))
        # print (site[0])
        s_name = site[0]
        s_location = site[1]
        print (type(s_location))
        s_type = site[2]
        s_discription = site[3]
        row = [s_name,s_location, s_type, s_discription]
        writer.writerow(row)

        # if count >=1:
        #     break
        # else:
        #     count +=1
        #     print (STATE_SITE_LIST[0])
        #     for site in state:
        #         print (site)
        #         print (len(state))
        #         print (type(site))
        #
        #         print ("***********")


#

##extracting urls found within pages
# for link in soup.find_all('a'):
#     print(link.get('href'))
# http://example.com/elsie
# http://example.com/lacie
# http://example.com/tillie

##1 row = 1 national site

#Code for caching data on json file
