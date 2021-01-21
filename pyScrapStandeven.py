import json
import time
from bs4 import BeautifulSoup
import random
from bs4 import BeautifulSoup
from selenium import webdriver
import cssutils

URL = "https://lovatmill.com/bunches/"


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1980,1080')

EXE_PATH = "chromedriver.exe"


URL = "https://standevenfabrics.co.uk/bunches/blackstorm/"

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

def get_bunch_urls(source):
    sub_urls = []
    soup = BeautifulSoup(source, "html.parser")
    header_bottom = soup.find("header",{"class":"header"}).find("div",{"class":"container"}).find("div",{"class":"header-bottom"})
    li_bunch_tag = header_bottom.find("nav",{"class":"header-menu"}).find("ul", {"id":"menu-main-menu"}).find("li", {"id":"menu-item-393"}).find("ul",{"class":"sub-menu"}).find("li",{"id":"menu-item-66"}).find("ul", {"class": "sub-menu"}).findAll("li", {"id": "menu-item-"})
    for li_tag in li_bunch_tag:
        try:
            sub_urls.append({
                "href": li_tag.find("a")['href'],
                "cloth_bunch": li_tag.find("a")['title']
            })
        except Exception as e:
            print("Error in get href and cloth bunch =>", e)

    return sub_urls

def scrap_standeven():
    driver = webdriver.Chrome(executable_path=EXE_PATH, chrome_options=chrome_options)
    driver.get(URL)
    time.sleep(5)
    sub_urls = get_bunch_urls(driver.page_source)

    for sub_url in sub_urls:
        driver.get(sub_url['href'])
        scroll(driver, 5)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        try:
            div_items = soup.find("section", {"class":"color"}).find("div",{"class":"container"}).find("div", {"class":"row"}).find("div", {"id":"items-container"}).findAll("div", {"class":"col-md-4 col-sm-6 active"})
            for div_item in div_items:
                image_url = ''
                cloth_pattern_number = ''
                composition1 = ''
                colour = ""
                weight = ""
                try:
                    image_url = div_item.find("div", {"class":"color_item"}).find("div", {"class":"open-product"}).find("img")['src']
                    sub_href = div_item.find("div", {"class":"color_item"}).find("div", {"class":"open-product"}).find("a")['href']
                    driver.get(sub_href)
                    time.sleep(5)
                    sub_soup = BeautifulSoup(driver.page_source, 'html.parser')
                    try:
                        detail_div = sub_soup.find("section", {"id": "product-content"}).find("div", {"class":"container"}).find("div", {"class":"content-area"}).find("main", {"id":"main"}).find("div", {"class":"summary entry-summary"})
                        cloth_pattern_number = detail_div.find("h1", {"class":"product_title entry-title"}).text.split(" ")[0].strip()
                        div_description = detail_div.find("div", {"class":"product-description"})
                        composition1 = div_description.find("p").text
                        colour = div_description.find("p", {"class":"fabric-colour"}).text.replace("Colour:","").strip()
                        weight = div_description.find("p", {"class":"fabric-weight"}).text.replace("Weight:","").strip().split("/")[0].replace("gms","").strip()
                    except Exception as e:
                        print("Error to get detail information ->", e)

                    write_data = {
                        "image_url":image_url,
                        "cloth_pattern_number": cloth_pattern_number,
                        "composition1": composition1,
                        "colour": colour,
                        "weight": weight,
                        "cloth_bunch":sub_url['cloth_bunch'],
                        "suppler":"Standeven"
                    }
                    with open("standeven_new.json", "a") as f:
                        json.dump(write_data, f, indent=4)
                        f.write(",")
                except Exception as e:
                    print("Error to get sub href => ", e)
        except Exception as e:
            print("Error get items =>", e)



    return

if __name__ == '__main__':
    scrap_standeven()