# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 10:03:26 2020

@author: bruno
"""
import pandas
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import sys

import time

chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(".//chromedriver.exe", options=chrome_options)
# https://chromedriver.chromium.org/downloads
driver.get("https://www.google.com.br/maps/search/dealer+ford,+Adelanto,+CA,+EUA/@34.4381371,-118.5060137,8z")
time.sleep(2)
response = driver.page_source
driver.quit()


soup = BeautifulSoup(response, "html.parser")

containers = soup.findAll("div", class_="section-result-text-content")

result = []
for container in containers:
    website = soup.find("a", {"class": "section-result-action section-result-action-wide"})["data-href"]
    title = container.find("h3", class_="section-result-title").getText()
    print(title)
    phone = container.find("span", class_="section-result-info section-result-phone-number").getText()
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver2 = webdriver.Chrome(".//chromedriver.exe", options=chrome_options)
    # https://chromedriver.chromium.org/downloads
    driver2.get("https://www.google.com.br/maps/place/")
    time.sleep(2)
    
    inputElement = driver2.find_elements_by_xpath('//input[@id="searchboxinput"]')[0]
    inputElement.send_keys(title+",CA, USA")    
    inputElement.send_keys(Keys.ENTER)   
    time.sleep(2)
    inputElement.send_keys(Keys.DOWN)
    inputElement.send_keys(Keys.ENTER) 
    
    response2 = driver2.page_source
 
    soup2 = BeautifulSoup(response2, "html.parser")
    address = soup2.findAll("div", class_="ugiz4pqJLAG__primary-text gm2-body-2")[0].getText()
    
 
    driver2.quit()
    

    data = {
              "website": website,
              "title": title,
              "phone": phone,
              "address": address,

          }
    result.append(data)
import pandas as pd

result = pd.DataFrame.from_records(result)
result.to_excel("result.xlsx") 
