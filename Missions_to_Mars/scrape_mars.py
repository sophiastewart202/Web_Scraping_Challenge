import pandas as pd
import numpy as np

from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def scrape_data():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    
    
    # NASA Mars News
    # Get splinter to open browser at url
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    # Get article titles and teasers
    news_titles = soup.find_all(class_='content_title')
    news_teasers = soup.find_all(class_='article_teaser_body')
    titles = []
    teasers = []
    for news_title in news_titles:
        for news_teaser in news_teasers:
            titles.append(news_title.text)
            teasers.append(news_teaser.text)
            
    # Create data frame (cause why not?)
    nasa_news = {"Title": titles, "Teaser": teasers}
    df = pd.DataFrame(nasa_news)
    
    # Save first row into variables
    nasa_news_title = df['Title'].iloc[0]
    nasa_news_teaser = df['Teaser'].iloc[0]
    
    
    
    # JPL Mars Space Images - Featured Image
    # Get splinter to open browser at url
    url2 = 'https://spaceimages-mars.com/'
    browser.visit(url2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find featured image data
    featured_img = soup.find_all(class_='headerimage')

    # Grab the image source and create the complete url, storing in a new variable
    for item in featured_img:
        featured_img_url = url2 + item['src']
    
    

    # Mars Facts
    url3 = 'https://galaxyfacts-mars.com/'
    # Get splinter to open browser at url
    tables = pd.read_html(url3)

    # Save tables separately
    mars_earth_comparison = tables[0].copy()
    mars_profile = tables[1].copy()

    # Add column headers
    mars_earth_comparison.columns =['', 'Mars', 'Earth']
    # Remove non-header row with duplicate column names
    mars_earth_comparison = mars_earth_comparison.drop(mars_earth_comparison.index[[0]])
    # Set index
    mars_earth_comparison = mars_earth_comparison.set_index('')

    # Add column headers
    mars_profile.columns =['Mars Planet Profile', '']
    # Set index
    mars_profile = mars_profile.set_index('Mars Planet Profile')
    # Convert to html
    mars_profile = mars_profile.to_html(classes="table table-striped")
    
    
    # Mars Hemispheres
    url4 = 'https://marshemispheres.com/'
    # Get splinter to open browser at url
    browser.visit(url4)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Create empty list to hold dictionaries of each hemisphere image with the title & image url
    hemisphere_image_urls = []

    # find the links (to help with navigation from page to page)
    html_info = soup.find_all('h3')
    links = [html_info[0].text, html_info[1].text, html_info[2].text, html_info[3].text]
    back = html_info[4].text

    for link in links:
        mars_dict = {}
        browser.find_by_text(link).click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        images = soup.find_all(class_='wide-image')
        titles = soup.find_all(class_ = 'title')
    
        for title in titles:
            for image in images:
                mars_dict["title"] = title.text
                mars_dict["img_url"] = url4 + image['src']
                hemisphere_image_urls.append(mars_dict)
        
        browser.find_by_text(back).click()
        
        
    
    # Store data in a dictionary
    mars_data = { 
    'mars_news': [nasa_news_title, nasa_news_teaser],
    'mars_featured_image': featured_img_url,
    'mars_facts': mars_profile,
    'mars_hemispheres': hemisphere_image_urls
    }
    
    # Close the browser
    browser.quit()
    
    return mars_data
    
        
        
    
    