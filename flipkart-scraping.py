# Importing necessary Libraries
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.keys import Keys
import os
import time
import csv
import re
from bs4 import BeautifulSoup


def get_url(search_item):
    '''
    This function fetches the URL of the item that you want to search
    '''
    PATH = (r'C:\Users\Rutvikpatil\OneDrive\Desktop\SELENIUM\chromedriver.exe')
    driver = webdriver.Chrome(PATH)

    template = 'https://www.flipkart.com/mobiles/mi~brand/pr?sid=tyy%2C4io&page=1'
    search_item = search_item.replace(" ","+")
    # Add term query to URL
    url = template.format(search_item)
    # Add term query placeholder
    url += '&page{}'
    return url

def extract_phone_model_info(item):
    """
    This function extracts model, price, ram, storage, stars , number of ratings, number of reviews,
    storage expandable option, display option, camera quality, battery , processor, warranty of a phone model at flipkart
    """
    # Extracting the model of the phone from the 1st card
    model = item.find('div',{'class':"_4rR01T"}).text
    # Extracting Stars from 1st card
    star = item.find('div',{'class':"_3LWZlK"}).text
    # Extracting Number of Ratings from 1st card
    num_ratings = item.find('span', {'class': "_13vcmD"}).text.replace('\xa0&\xa0', " ; ")[
                  0:item.find('span', {'class': "_13vcmD"}).text.replace('\xa0&\xa0', " ; ").find(';')].strip()
    # Extracting Number of Reviews from 1st card
    reviews = item.find('span', {'class': "_2_R_DZ"}).text.replace('\xa0&\xa0', " ; ")[
              item.find('span', {'class': "_2_R_DZ"}).text.replace('\xa0&\xa0', " ; ").find(';') + 1:].strip()
    # Extracting RAM from the 1st card
    ram = item.find('li', {'class': "rgWa7D"}).text[0:item.find('li', {'class': "rgWa7D"}).text.find('|')]
    # Extracting Storage/ROM from 1st card
    storage = item.find('li', {'class': "rgWa7D"}).text[item.find('li', {'class': "rgWa7D"}).text.find('|') + 1:][
              0:10].strip()
    # Extracting whether there is an option of expanding the storage or not
    expandable = item.find('li', {'class': "rgWa7D"}).text[item.find('li', {'class': "rgWa7D"}).text.find('|') + 1:][
                 13:]
    # Extracting the display option from the 1st card
    display = item.find_all('li')[1].text.strip()
    # Extracting camera options from the 1st card
    camera = item.find_all('li')[2].text.strip()
    # Extracting the battery option from the 1st card
    battery = item.find_all('li')[3].text
    # Extracting the processir option from the 1st card
    processor = item.find_all('li')[4].text.strip()
    # Extracting Warranty from the 1st card
    warranty = item.find_all('li')[-1].text.strip()
    # Extracting price of the model from the 1st card
    price = item.find('div', {'class': '_30jeq3 _1_WHN1'}).text
    result = (
    model, star, num_ratings, reviews, ram, storage, expandable, display, camera, battery, processor, warranty, price)
    return result
def main(search_item):
    '''
    This function will create a dataframe for all the details that we are fetching from all the multiple pages
    '''
    driver = webdriver.Chrome()
    records = []
    url = get_url(search_item)
    for page in range(1,464):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source,'html.parser')
        results = soup.find_all('a',{'class':"_1fQZEK"})
        for item in results:
            records.append(extract_phone_model_info(item))
    driver.close()
    # Saving the data into a csv file
    with open('Flipkart_results.csv','w',newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Model','Stars','Num_of_Ratings','Reviews','Ram','Storage','Expandable',
                        'Display','Camera','Battery','Processor','Warranty','Price'])
        writer.writerows(records)