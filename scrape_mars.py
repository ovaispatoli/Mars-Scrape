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
    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_= "article_teaser_body").text

    mars_data["Latest News Title"] = news_title
    mars_data ["Latest News Paragraph"] = news_p

    #-JPL Mars Featured Image
    nasa_img = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(nasa_img)
    time.sleep(2)
    img_html = browser.html
    soup = bs(img_html, "html.parser")

    img_base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(nasa_img))
    img_url = soup.find("div", class_="carousel_items").find("article")["style"]
    img_url = img_url[23:(len(img_url)-3)]

    feat_img_url = img_base_url + img_url

    mars_data["Featured Image"] = feat_img_url

    #-Mars Weather
    tweet_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(tweet_url)

    html_tweet = browser.html
    soup = bs(html_tweet, "html.parser")

    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_weather = mars_weather.replace("\n", " ")
    mars_weather = mars_weather[0:-26]

    mars_data["Mars Weather"] = mars_weather
    





