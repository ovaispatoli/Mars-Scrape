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
    
    #-Mars Facts

    facts_url = "https://space-facts.com/mars/"
    time.sleep(3)
    facts_table = pd.read_html(facts_url)
    
    facts_df = pd.DataFrame(facts_table[0])
    facts_df.columns = ["Measurements", "Values"]
    facts_df = facts_df.reset_index(["Measurements"])

    facts_html = facts_df.to_html()
    facts_html = facts_html.replace("\n", "")
    
    mars_data["Mars Facts Table"] = facts_html

    #-Mars Hemipsheres
    
    hem_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hem_url)

    #Base URL
    hem_base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(hem_url))

    #soup object
    hem_html = browser.html
    soup = bs(hem_html, "html.parser")

    #find all divs containing class 'item'
    div_data = soup.find_all("div", class_="item")

    #Create empty list to append to
    hem_img_urls = []

    #Loop and find image urls
    for item in div_data:
        #Find and store title
        img_title = item.find("h3").text
        #Find and store link to image
        img_url = item.find("a", class_= "itemLink product-item")["href"]
        #Visit image web page
        browser.visit(hem_base_url + img_url)
        #Convert web page into html format and then soup object
        img_html = browser.html
        soup = bs(img_html, "html.parser")
        #Get full image source
        img_src = (hem_base_url + soup.find("img", class_= "wide-image")["src"])
        #Append to empty list: hem_img_urls
        hem_img_urls.append({"Image Title": img_title}, "Image URL": img_src})
        #Wait a second or two
        time.sleep(2)

    #-Add hem_img_urls to mars_data
    mars_data["Hemisphere Image URL's"] = hem_img_urls

    #-Return Mars DAta
    return mars_data


