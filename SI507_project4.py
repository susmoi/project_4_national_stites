from bs4 import BeautifulSoup
import requests
import json
import csv

from advanced_expiry_caching import Cache

#Constants
FNAME = "national_sites_cache.json"
START_URL = "https://www.nps.gov"

PROGRAM_CACHE = Cache(FNAME)

# Function which either gets data from cache or creates new get request, then returns data
def scrape_function(some_url):
    data = PROGRAM_CACHE.get_data(some_url)
    if not data:
        data = requests.get(some_url).text
        PROGRAM_CACHE.set(some_url, data)
    return data

main_page = scrape_function(START_URL)

# create a BeautifulSoup object from returned data
main_soup = BeautifulSoup(main_page, features="html.parser")
#  find state list
ul_states = main_soup.find("ul",{"class":"dropdown-menu"})
# extract "a" tags from list
anchor_tags = ul_states.find_all('a')

# creates a list of "a" tag links for crawling
crawl_list = []
for a in anchor_tags:
    link = "{}{}".format(START_URL, a.get("href"))
    crawl_list.append(link)

# web crawling Function
def web_crawler(some_list):
    count = 0
    list_of_BS_objects = []

    # Loops thorugh list scraping each link and creating a BeautifulSoup object and appending the object to a list
    for link in some_list:
        page_data = scrape_function(link)
        page_soup = BeautifulSoup(page_data, features="html.parser")
        list_of_BS_objects.append(page_soup)

    STATES_DICT = {}
    SITE_LIST = []

    # for each soup object, finds div with site info
    for soup in list_of_BS_objects:
        national_sites_divs = soup.find_all('div',{'class':'col-md-9 col-sm-9 col-xs-12 table-cell list_left'})

        # Loops through the target div elements and grab site name, type, discription, and location
        for div in national_sites_divs:
            local_list = []
            site_name = div.find("h3").text
            site_type = div.find("h2").text
            site_discription = div.find("p").text.strip('\n')
            site_location = div.find("h4").text

            # creates a local_list containing the above site info
            local_list = [site_name,site_location, site_type, site_discription]
            SITE_LIST.append(local_list)
    return SITE_LIST

# run function
state_site_info_list = web_crawler(crawl_list)

# writes a new csv file using site info list
with open ("National_Site_CSV.csv", "w", newline="") as fh:
    writer = csv.writer(fh)
    header = ["Site Name","Site Location","Site Type", "Site discription"]
    writer.writerow(header)
    count = 0
    for site in state_site_info_list:
        s_name = site[0].upper()
        s_location = site[1]
        s_type = site[2]
        s_discription = site[3]
        row = [s_name,s_location, s_type, s_discription]
        writer.writerow(row)
