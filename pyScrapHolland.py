import json
import time
from bs4 import BeautifulSoup
import random
from bs4 import BeautifulSoup
from selenium import webdriver
import cssutils
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys




chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1980,1080')

EXE_PATH = "chromedriver.exe"


URL= "https://apparel.hollandandsherry.com/en/fabric/bunch/all-bunch-books/{}"
URL_PREFIX = "https://apparel.hollandandsherry.com"
def scroll(driver, timeout):
    scroll_pause_time = timeout
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
        # If heights are the same it will exit the function
            break
        last_height = new_height

    return

def gen_url(bunch):
    sublink = ''
    if bunch == 'HS1920':
        sublink = 'hs-1920'
    elif bunch == 'HS1845A/B':
        sublink = 'hs1845ab'
    elif bunch == 'HS1831A':
        sublink = 'hs1831a-royal-mile-1976'
    elif bunch == 'HS1698B':
        sublink = 'hs1698b-trenchcoat-collection'
    elif bunch == 'HS1698A':
        sublink = 'hs1698a-classic-overcoats--topcoats'
    elif bunch == 'HS1697':
        sublink = 'hs1697-black-tie'
    elif bunch == 'HS1692':
        sublink = 'hs1692-cashmere-doeskin-blazers'
    elif bunch == 'HS1682':
        sublink = 'hs1682-peacock'
    elif bunch == 'HS1669':
        sublink = 'hs1669-sloane-square'
    elif bunch == 'HS1663':
        sublink = 'hs1663-city-suits'
    elif bunch == 'HS1643':
        sublink = 'hs1643-the-anniversary-collection'
    elif bunch == 'HS1642':
        sublink = 'hs1642-imperial-gold'
    elif bunch == 'HS1627':
        sublink = 'hs1627-so-cotton'
    elif bunch == 'HS1622':
        sublink = 'hs1622-linings-collection'
    elif bunch == 'HS1564':
        sublink = 'hs1564-perennial-classics'
    elif bunch == 'HS1529':
        sublink = 'hs1529-target-gaberdines'
    elif bunch == 'HS1528B':
        sublink = 'hs1528b-classic-mohairs'
    elif bunch == 'HS1470':
        sublink = 'hs1470-koh-i-noor'
    else:
        sublink = bunch

    return URL.format(sublink)

def scrap_holland():
    driver = webdriver.Chrome(executable_path=EXE_PATH, chrome_options=chrome_options)
    bunch_list = []
    with open('Holland_bunch.txt', "r") as f:
        for line in f.readlines():
            bunch_list.append(line.rstrip())
    brestart = False
    for bunch in bunch_list:
        if bunch == 'HS1840':
            brestart = True
        if brestart == True:
            url = gen_url(str(bunch))
            driver.get(url)
            time.sleep(2)
            scroll(driver,5)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            title_container_tag = soup.find("div" , {"class":"relpos"})
            if title_container_tag is not None:
                titles = title_container_tag.findAll("div", {"class":"tile"})
                for tile in titles:
                    try:
                        href = tile.find("a")['href']
                    except Exception as e:
                        print ("Get href error ->", e)
                    try:
                        image_url = tile.find("div", {"class":"productImage"}).find("img")['src']
                    except Exception as e:
                        print("Get Error In Image URL ->",e)
                    try:
                        cloth_pattern_number = tile.find("div", {"class":"tileDescription"}).find("p", {"class":"productCode"}).text
                    except Exception as e:
                        print("Get Error Cloth Pattern Number ->",e)

                    write_data = {
                        "cloth_pattern_number": cloth_pattern_number,
                        "image_url": image_url,
                        "cloth_bunch": bunch
                    }

                    driver.get(URL_PREFIX + href)
                    time.sleep(2)
                    sub_soup = BeautifulSoup(driver.page_source,"html.parser")
                    try:
                        div_product = sub_soup.find("section", {"class": "productSection"}).find("div", {"class": "productDescriptionContent"}).find("div", {"class":"productDetails"})
                        colour = div_product.find("div", {"class":"productColor"}).text
                        div_product_desc = div_product.find("div", {"class":"productDesc"}).find("pre", {"class":"prestyled_block"}).text

                        desc_datas = div_product_desc.split("\n")
                        composition1 = ""
                        weight_gm = ""
                        design = ""
                        for desc_data in desc_datas:
                            if "Composition" in desc_data:
                                composition1 = desc_data.replace("Composition:","").strip()
                            if "Weight" in desc_data:
                                weight_gm = desc_data.replace("Weight:","").strip().split(" ")[0].replace("gm", "")
                            if "Design" in desc_data:
                                design = desc_data.replace("Design:", "").strip()
                        write_data.update({
                            "colour": colour,
                            "composition1": composition1,
                            "weight_gm": weight_gm,
                            "design": design
                        })
                    except Exception as e:
                        print("Error on product description tag", e)
                    try:
                        with open("holland_sherry_new_update.json", "a", encoding="latin1") as f:
                            json.dump(write_data, f, indent=4)
                            f.write(",")
                        print("*********************************", str(cloth_pattern_number) + " " + str(bunch))
                    except Exception as e:
                        print("Write File Error ->", e)
    return


if __name__ == '__main__':
    scrap_holland()