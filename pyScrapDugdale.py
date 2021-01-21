import json
import time
from bs4 import BeautifulSoup
import random
from selenium import webdriver
import cssutils
import re

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1980,1080')

EXE_PATH = "chromedriver.exe"

URL = 'https://www.dugdalebros.com/collections/'

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
# /rows/80/sort/rel/
def get_sub_urls(source):
    sub_urls = []
    soup = BeautifulSoup(source, "html.parser")
    category_divs = soup.find("div",{"id":"page"}).find("div", {"class":"site-content-contain"}).find("div", {"class":"site-content"}).find("div",{"class":"main-content"}).find("div", {"class":"content-area"}).find("div",{"id":"content"}).findAll("div",{"class":"vc_row wpb_row vc_row-fluid"})
    r_category_divs = category_divs[-1]
    regex = re.compile('.*c-lister__item js-fade-in.*')
    try:
        divs = r_category_divs.find("div", {"class":"wpb_column vc_column_container vc_col-sm-12"}).find("div", {"class":"vc_column-inner"}).find("div", {"class":"container"}).find("div",{"class":"c-lister no-pad"}).find("div",{"class":"row text-center c-lister__header"}).find("div",{"class":"col-12 p-0"}).find("div",{"class":"row c-lister__container"}).findAll("div",{"class":regex})
        for div in divs:
            href = div.find("div", {"class":"c-lister__item--banner"}).find("a")['href']
            bunch_code = div.find("div", {"class":"c-lister__item--pre"}).text.replace("BUNCH", "").strip()
            sub_urls.append({
               "href": href,
                "cloth_bunch": bunch_code
            })
    except Exception as e:
        print("Error -> ", e)
    return sub_urls

def get_detail_urls(source):
    soup = BeautifulSoup(source, "html.parser")
    category_divs = soup.find("div", {"id": "page"}).find("div", {"class": "site-content-contain"}).find("div", {
        "class": "site-content"}).find("div", {"class": "main-content"}).find("div", {"class": "content-area"}).find(
        "div", {"id": "content"}).findAll("div", {"class": "vc_row wpb_row vc_row-fluid"})
    r_category_divs = category_divs[0]
    href = r_category_divs.find("a",{"class":"c-button c-button--center"})['href']
    return  href

def scrap_dugdale():
    driver = webdriver.Chrome(executable_path=EXE_PATH, chrome_options=chrome_options)
    # driver.get(URL)
    # scroll(driver, 5)
    # sub_urls = get_sub_urls(driver.page_source)
    # detail_urls = []
    # for sub_url in sub_urls:
    #     driver.get(sub_url['href'])
    #     time.sleep(5)
    #     detail_url =get_detail_urls(driver.page_source)
    #     detail_urls.append({
    #         "href": detail_url + "/rows/200/sort/rel/",
    #         "cloth_bunch": sub_url['cloth_bunch']
    #     })
    #
    # with open("dugdale_url.json","w") as f:
    #     json.dump(detail_urls, f, indent=4)
    #
    # return
    detail_urls = []
    with open("dugdale_url.json", "r") as f:
        detail_urls = json.load(f)

    for detail_url in detail_urls:
        driver.get(detail_url['href'])
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        regex = re.compile('.*products.*')
        try:
            product_divs = soup.find("div", {"id":"outercontainer"}).find("span", {"id":"main-content"}).find("div",{"class":"outerrow"}).find("div",{"id":"lister"})\
        .find("div", {"id":"product-holder"}).find("div", {"class":"product-holder-inner"}).find("div",{"class": regex}).findAll("div", {"class":"product-card"})
            for product in product_divs:
                image_url = ''
                tag_a = product.find("a", {"class":"content"})
                try:
                    image_url = tag_a.find('div', {"class":"thumb"}).find('div', {"class":"productThumbnail"}).find('img')['src']
                except Exception as e:
                    print("error get image url", e)
                driver.get("https://shop.dugdalebros.com" + tag_a['href'])
                time.sleep(5)
                detail_soup = BeautifulSoup(driver.page_source, 'html.parser')
                try:
                    divs_active = detail_soup.find("div", {"id":"outercontainer"}).find("span", {"id":"main-content"}).find("div", {"class":"product-page"}).find("div", {"id":"product"}).find("div",{"class":"container"}).find("div", {"class":"row"}).findAll("div", {"class":"col-12 col-lg-6"})
                    active_tag = divs_active[-1]
                    div_tab = active_tag.find("div", {"class":"more-info-tabs"}).find("div", {"class":"product-spec"}).find("div", {"id":"product-spec-row"}).find("div", {"data-tab-content-id":"1"}).find("div",{"class":"info-attributes"})
                    regex = re.compile('.*info-attribute.*')
                    composition1 = ""
                    weight = ""
                    width = ""
                    cloth_pattern_number = ""
                    div_infos = div_tab.findAll("div", {"class":regex})
                    for div in div_infos:
                        if 'Width:' in div.text:
                            width = div.text.replace("Width:","").replace("\n", " ").replace("cm", "").strip()
                        elif "Weight:" in div.text:
                            weight = div.text.replace("Weight:","").split("/")[-1].replace("grams","").strip()
                        elif "Product SKU:" in div.text:
                            cloth_pattern_number = div.text.replace("Product SKU:","").strip()
                        elif "Bunch Name:" in div.text:
                            continue
                        elif "Bunch Number:" in div.text:
                            continue
                        else:
                            composition1 = div.text.replace("\n","\t").replace("\t"," ").strip()

                    write_data = {
                         "image_url": image_url,
                         "cloth_pattern_number": cloth_pattern_number,
                         "weight": weight,
                         "width": width,
                         "composition1": composition1,
                         "cloth_bunch": detail_url['cloth_bunch']
                     }

                    with open("dugdale_new.json", "a") as f:
                        json.dump(write_data, f, indent=4)
                        f.write(",")

                except Exception as e:
                    print("error active tab", e)

        except Exception as e:
            print("Error to get product ", e)


    return


if __name__ == '__main__':
    scrap_dugdale()