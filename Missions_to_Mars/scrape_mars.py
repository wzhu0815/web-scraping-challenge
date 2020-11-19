# Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    listings = {}
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html,'html.parser')
    quotes = soup.find_all('li',class_='slide')
    news_title = quotes[0].find('div',class_='content_title').text
    news_p = quotes[0].find('div',class_='article_teaser_body').text
    listings['news_title'] = news_title
    listings['news_p'] = news_p
    # print(news_title)
    # print(news_p)
    browser.quit()
    
    browser = init_browser()
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html,'html.parser')
    quotes = soup.find_all('a',class_='fancybox')
    featured_image_url = 'https://www.jpl.nasa.gov/'+quotes[0]['data-fancybox-href']
    listings['featured_image_url'] = featured_image_url
    # print(featured_image_url)
    browser.quit()

    browser = init_browser()
    url ='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html,'html.parser')
    quotes = soup.find_all('div',class_='item')
    hemisphere_image_urls=[]
    for quote in quotes:
        t = quote.find('h3').text
        a = quote.a['href']
        a=a.replace('search/map','download')
        dic={}
        dic['title']=t
        dic['img_url']= "https://astropedia.astrogeology.usgs.gov"+a+'.tif/full.jpg'
        hemisphere_image_urls.append(dic)
    listings['hemisphere_image_urls'] = hemisphere_image_urls
    browser.quit()
    # print(hemisphere_image_urls) 
    print('------------------------------------------------------------------------------------------------')
    print(listings)
    return listings


