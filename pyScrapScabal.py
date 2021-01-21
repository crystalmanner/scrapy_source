import json
import time
from bs4 import BeautifulSoup

from selenium import  webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1980,1080')

EXE_PATH = "chromedriver.exe"

URL = "https://fabrics.scabal.com/en/catalogue#/product-detail/"

def get_image_url(id):
    images = []
    with open("images.json", "r") as f:
        images = json.load(f)
    for image in images:
        if str(id) == image['pattern_number']:
            return image['img_url']
    try:
        url = URL + str(id)
        driver = webdriver.Chrome(executable_path=EXE_PATH, chrome_options=chrome_options)
        driver.get(url)
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        img_url = soup.find('div', {"class": "productDetailAllImg"}).find('img')
        driver.close()
        return img_url.get('src')
    except Exception as e:
        print("error", e)

    return ""

