#!/usr/bin/env python
# coding: utf-8

# ## Mission To Mars Notebook
# 

# ### Dependencies

# In[98]:


#--Dependencies

from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import pandas as pd
import numpy as np
import time
from urllib.parse import urlsplit
import pymongo


# ### Web Scrape Code

# In[99]:


#Chromedriver and Browser set-up

driver_path = {"executable_path":"chromedriver.exe"}
browser =  Browser('chrome', **driver_path, headless=False)


# #### NASA Mars News

# In[100]:


#URL set-up

url = "https:/mars.nasa.gov/news/"
browser.visit(url)


# In[101]:


# Beautiful Soup Html parser set-up

html = browser.html
soup = bs(html, "html.parser")


# In[102]:


# Fetch latest news title and paragraph text

news_title = soup.find("div", class_= "content_title").text
news_p = soup.find("div", class_= "article_teaser_body").text


print(f"Latest Title: {news_title}")
print("----------------------------")
print(f"Title Paragraph: {news_p}")


# #### JPL Mars Space Images - Featured Image

# In[103]:


image_url = "https://www.jpl.nasa.gov/spaceimages/images/wallpaper/PIA09320-1920x1200.jpg"
browser.visit(image_url)


# #### Mars Weather

# In[104]:


#Get the latest tweet from mar's weather twitter account

tweet_url = "https://twitter.com/marswxreport?lang=en"
browser.visit(tweet_url)


# In[105]:


#Turn into soup object for text
html_tweet = browser.html
soup = bs(html_tweet, "html.parser")

mars_weather = soup.find("p", class_= "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

mars_weather = mars_weather.replace("\n", " ")
mars_weather = mars_weather[0:-26]
mars_weather


# #### Mars Facts

# In[106]:


facts_url = "https://space-facts.com/mars/"

facts_table = pd.read_html(facts_url)
facts_table[0]


# In[75]:


#--Turn into DataFrame

facts_df = pd.DataFrame(facts_table[0])

facts_df.columns = ["Measurements", "Values"]
facts_df.reset_index(["Measurements"], inplace=True)

facts_df


# In[76]:


#turn into HTML table

facts_table = facts_df.to_html()
facts_table = facts_table.replace("\n", "")
facts_table


# #### Mars Hemispheres (Images)

# In[77]:


#set-url and launch browser

hem_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(hem_url)


# In[90]:


#get base url

hem_base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(hem_url))
print(hem_base_url)


#Soup object
hem_html = browser.html

soup = bs(hem_html, "html.parser")

#Find all divs containing class 'item'

div_data = soup.find_all("div", class_="item")


# In[79]:


# create image list to append url to

hem_img_urls = []
hem_img_urls


# In[96]:


#--loop and find images
for item in div_data:

    #Find and store title
    img_title = item.find("h3").text
    #print(title)
    
    #Find and store link to image 
    img_url = item.find("a", class_= "itemLink product-item")["href"]
    
    #Visit image web page
    browser.visit(hem_base_url + img_url)
    
    #Convert image web page to html and then soup object
    img_html = browser.html

    soup = bs(img_html, "html.parser")
    
    #Get full image source
    img_src = hem_base_url + soup.find("img", class_="wide-image")["src"]
    
    #Append to hem_img_urls list
    hem_img_urls.append({"Image Title": img_title, "Image URL": img_src})
    


# In[97]:


#--Pring hem_img_urls

hem_img_urls


# In[ ]:




