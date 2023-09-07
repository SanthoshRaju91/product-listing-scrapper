import time

import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)


def get_item_page_html_soup(url):
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    return soup


def get_product_title(soup):
    product_title = soup.find('span', class_="normal_reserve_item_name").text.strip()
    return product_title


def get_product_description(soup):
    product_description = soup.find('meta', attrs={'name': 'description'})['content'].strip()
    return product_description


def get_product_price(soup):
    product_price = soup.find('meta', itemprop='price')['content'].strip()
    return product_price


def get_product_images(soup):
    product_images = []
    image_tags = soup.find_all('meta', itemprop='image')

    for image_tag in image_tags:
        product_images.append(image_tag['content'])

    return product_images


def get_product_reviews(soup):
    rating_aggregate = soup.find('div', attrs={'itemprop': 'aggregateRating'})
    rating_value = 0
    rating_count = 0

    if rating_aggregate:
        rating_value = rating_aggregate.find('meta', attrs={'itemprop': 'ratingValue'})['content'].strip()
        rating_count = rating_aggregate.find('meta',  attrs={'itemprop': 'reviewCount'})['content'].strip()
    
    return rating_value, rating_count


def get_product_shipping_options(soup):
    shipping = soup.find('span', attrs={'irc': 'ShippingFee'})
    shipping_options = 'NA'

    if shipping.find('div'):
        shipping_options = shipping.find('div').text.strip()
    
    return shipping_options


def get_product_genre(soup):
    genre_tree = soup.find('div', class_='rGenreTreeDiv')
    genres = []
    if genre_tree:
        genre_tags = genre_tree.find_all('a', href=True)
        for genre_tag in genre_tags:
            genre_text = genre_tag.text.strip()
            genre_url = genre_tag['href']
            genres.append({
                "text": genre_text,
                "url": genre_url
            })
    return genres


def scrape_item_page(url):
    print("::: Scrapping web page")
    item_page_html_soup = get_item_page_html_soup(url)
    product_title = get_product_title(item_page_html_soup)
    product_description = get_product_description(item_page_html_soup)
    product_price = get_product_price(item_page_html_soup)
    product_images = get_product_images(item_page_html_soup)
    rating_value, rating_count = get_product_reviews(item_page_html_soup)
    shipping_options = get_product_shipping_options(item_page_html_soup)
    genres = get_product_genre(item_page_html_soup)
    print("::: Scrapping done")

    return {
        "title": product_title,
        "description": product_description,
        "price": product_price,
        "images": product_images,
        "rating": rating_value,
        "rating_count": rating_count,
        "shipping_options": shipping_options,
        "genres": genres
    }



    

