#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Setup Dependencies 
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from webdriver_manager.chrome import ChromeDriverManager


# In[2]

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # In[3]:


    # Begin scraping
    url = 'https://mars.nasa.gov/news/'

    # Reach out to site
    browser.visit(url)

    html = browser.html

    news_data = BeautifulSoup(html, 'html.parser')


    # In[4]:


    #Find title
    news_title = news_data.find_all('div', class_ = 'content_title')[1].text

    news_paragraph = news_data.find_all('div', class_ = 'article_teaser_body')[0].text


    # In[5]:


    print(news_title)
    print(news_paragraph)


    # In[6]:


    #Head to the other site to get the space images 
    nasa_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'

    next_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'

    browser.visit(next_url)

    html = browser.html

    image = BeautifulSoup(html, 'html.parser')


    # In[7]:


    image_url = image.find_all('img')[2]["src"]

    print(image_url)

    featured_image_url = nasa_url + image_url

    print(featured_image_url)


    # In[11]:


    #Visit Mars Facts page 
    mars_url = 'https://space-facts.com/mars/'

    facts = pd.read_html(mars_url)

    facts


    # In[12]:


    #convert data to HTML table string -- first put it into a table then put to html 
    facts_df = facts[2]

    facts_df.columns = ["Description", "Value"]

    html_table = facts_df.to_html()


    # In[13]:


    print(html_table)


    # In[21]:


    #Find information on Mars Atmosphere 
    a_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    b_url = 'https://astrogeology.usgs.gov/'
    browser.visit(a_url)

    html = browser.html

    atmosphere = BeautifulSoup(html, 'html.parser')


    # In[16]:


    all_atmospheres = atmosphere.find('div', class_ = 'result-list')

    atmosphere_item = all_atmospheres.find_all('div', class_= 'item')


    # In[25]:


    atmosphere_urls = []

    for i in atmosphere_item:
        atmosphere = i.find('div', class_= 'description')
        title = atmosphere.h3.text

        atmosphere_link = atmosphere.a["href"]
        browser.visit(b_url + atmosphere_link)

        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')

        image_link = image_soup.find('div', class_ = 'downloads')

        image_url = image_link.find('li').a['href']

        image_dict = {}
        image_dict['title'] = title
        image_dict['imgage_url'] = image_url

        atmosphere_urls.append(image_dict)

    print(atmosphere_urls)

    mars_data = {
        "news_title" : news_title,
        "news_paragraph" : news_paragraph,
        "featured_image" : featured_image,
        "atmosphere" : atmosphere,
    }

    browser.quit()

    return mars_data
# In[ ]:



