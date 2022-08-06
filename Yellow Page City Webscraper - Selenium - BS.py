# This webscraper was created as an example of how Selenium and Beautiful Soup can be used to create new datasets from YellowPageCity website. 
# I have not used this webscraper for any intention other than practicing coding abilities and have no intention of selling any information.
# The installation of Selenium and BeautifulSoup are needed to execute the script below. The script is a test example of how to scrape a few URLs.
# The same framework can modified for most websites. We can also use the same techniques to create bots or web testing purposes. 
# We can also scrape dynamic websites where we need to send words into a search bar just by programming and not physically typing them. (not included here)
# For a clear example on webscraping and how it works, watch the following Youtube videos from a channel called Tech With Tim. link: https://www.youtube.com/watch?v=Xjv1sY630Uc
# I've made notes about the process as well.

#Selenium is a powerful tool for controlling web browsers 
#through programs and performing browser automation. It is functional for all browsers, 
#works on all major OS and its scripts are written in various languages i.e Python, Java, C#, etc

#Beautiful Soup is a Python package for parsing HTML and XML documents. 
#It creates a parse tree for parsed pages that can be used to extract data 
#from HTML, which is useful for web scraping. 

# Selenium will get us to the webpage and BeautifulSoup will get the data from that page.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent # This changes the user agent frequently, helping to keep the IP being banned from various sites. 
import requests
from bs4 import BeautifulSoup
import time
from time import sleep
from random import randint
import numpy as np
import pandas as pd
import csv
import re
PATH = "C:\Program Files (x86)\chromedriver.exe"  # path your chromedriver is saved to.

options = Options()
ua = UserAgent()
userAgent = ua.random
options.add_argument(f'user-agent={userAgent}')

# Part 1: Scrape city urls to loop through. Each city URL displays multiple businesses. There is a URL associated with 
#         each business listing. Upon clicking onto that URL, we are taken to a businesses personal yellow page which displays their contact info. We want to scrape the URL's
#         by gathering the 'href' for the business links. For example, San+Antonio/Landscape+Contractors/Page+2/ URL seen below will diplay multiple businesses on that page. If there is a 
#         service called '123 Landscapers' we can retireve the URL (or href) associated with that business and store it into a list (which is 'test_lawn_service_contact_urls = []')


test_city_yellow_url = ['http://www.yellowpagecity.com/US/TX/San+Antonio/Landscape+Contractors/', 'http://www.yellowpagecity.com/US/TX/San+Antonio/Landscape+Contractors/Page+2/']

driver = webdriver.Chrome(chrome_options=options, executable_path=PATH)

test_lawn_service_contact_urls = []


for contact_urls in test_city_yellow_url:
    driver.get(contact_urls)

    soup_lawn_contacts = BeautifulSoup(driver.page_source, "html.parser")
    sleep(randint(2,3))# this function randomly decides how many seconds to wait in the range given, unitl switching to the next step in the loop. 
                            #Allows us to wait until the page is fully loaded before the scraper below activates, 
                                #and makes the banning of our IP address less likely because the time to scrape is random.
                                # It also puts less stress on the websties servers since we are not sending too many requests at once.

    for a in soup_lawn_contacts.findAll('a', {'class': 'listing-wrap'}, href=True):
        test_lawn_service_contact_urls.append('http://www.yellowpagecity.com'+a['href'])
        sleep(randint(5,9))


#Part 2: scrape yellowpagecity landscape contractor business details, by looping though the saved urls from 'test_lawn_service_contact_urls = []'. Store details in landscaper_data


landscaper_data = []

for urls_landscaper in test_lawn_service_contact_urls:
    
    
    driver.get(urls_landscaper)

    soup_landscaper = BeautifulSoup(driver.page_source, "html.parser")
    sleep(randint(2,3))

    
    for landscaper_item in soup_landscaper:  # below we scrape the desired contact info and business details by identifying unique html attributes per item.
        
        try:
            name_xx=landscaper_item.find('h3', {'class':'business-listing-businessName'}).text
        except:
            name_xx='NULL'
        pass
    
        try:
            address_xx=landscaper_item.find('span', {'class': 'listing-address'}).text
        except:
            address_xx='NULL'
        pass

        try:
            city_xx=landscaper_item.find('span', {'class': 'listing-city'}).text
        except:
            city_xx='NULL'
        pass

        try:
            state_xx=landscaper_item.find('span', {'class': 'listing-state'}).text
        except:
            state_xx='NULL'
        pass

        try:
            zip_xx=landscaper_item.find('span', {'class': 'listing-zip'}).text
        except:
            zip_xx='NULL'
        pass

        try:
            phone_xx=landscaper_item.find('a', {'class': 'btn btn-warning btn-sm pull-right call-btn-hide'}, href=True).get('href')
        except:
            phone_xx='NULL'
        pass
            
        try:
            business_listing_special_offer_xx=landscaper_item.find('span', {'class':'business-listing-specialOffer'}).text
        except:
            business_listing_special_offer_xx='NULL'
        pass

        try:
            alink_source = landscaper_item.find('li', {'class':'business-listing-email'})                                                              
            alinks = alink_source.find('a')
            if 'href' in alinks.attrs:
                    email_xx=alinks.get('href')
        except:
            email_xx='NULL'
        pass
            
        try:
            alink_source_2=landscaper_item.find('li', {'class':'business-listing-websiteUrl'})
            alinks_2=alink_source_2.find('a')
            if 'href' in alinks_2.attrs:
                additional_links_xx=alinks_2.get('href')
        except:
            additional_links_xx='NULL'
        pass
            
        # below we create the names of our saved variables and append them to create a new dataframe, which is then exported as a csv file. 
        landscaper_scraper = {
        'name': name_xx,   
        'address': address_xx,
        'city': city_xx,
        'state': state_xx,
        'zip': zip_xx,    
        'phone': phone_xx,
        'business_listing_special_offer': business_listing_special_offer_xx,
        'email': email_xx,
        'additional_links': additional_links_xx,  
        }
        landscaper_data.append(landscaper_scraper)
        sleep(randint(5,8))



df_biz_detail = pd.DataFrame(landscaper_data) 
df_biz_detail.to_csv(r'C:\Users\logan\Desktop\biz_detail_test.csv', index=False) # input your desired path to save the csv file and we have a new business dataset