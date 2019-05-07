#--Dependencies

from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import pandas as pd
import numpy as np
import time
from urllib.parse import urlsplit
import pymongo


#--browser function

def browser():
    driver_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **driver_path, headless=False)

#--scrape function

def scrape ():
    browser = browser()
    mars_data = {}

    #-Nasa Website
    nasa = "https://mars.nasa.gov/news/"
    browser.visit(nasa)
    time.sleep(2)

    html = browser.html
    soup = bs(html, "html.parser")

    #-Scrape latest mars data from NASA
    new_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_= "article_teaser_body").text

    #-JPL Mars Featured Image
    nasa_img = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    img_base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(nasa_img))

    browser.visit(nasa_img)



