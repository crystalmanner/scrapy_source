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

URL_LOGIN = "https://www.loropiana.com/textile/login"

URL_SEARCH = "https://www.loropiana.com/textile/fabrics/c/00030-00001?sort=sku-asc&q=%3Aname-asc%3Abunch%3A{}&show=Page#"
URL_SEARCH_SOLBIATI = "https://www.loropiana.com/textile/fabrics/Solbiati/c/00035-00030-00001?sort=sku-asc&q=%3Acollection-order%3Abunch%3A{}&show=Page#"
URL_PREFIX = "https://www.loropiana.com"
user_name = 'tim.illsley@huntsmansavilerow.com'
password = '46hun1118'

bunch_lists= [ ['S04', 'S05', 'S07', 'S09', 'S10', 'S11', 'S12', 'S13', 'S14', 'S15', 'S16'],
               [368, 450,641,645,654,659,661,662,664,667,668,669,672,673,674,675,684,685,686,690,691,694,695,696,697,701,703,704,705,706,707,708,709,710]]

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

def scrap_lora():

    driver = webdriver.Chrome(executable_path=EXE_PATH, chrome_options=chrome_options)
    driver.get(URL_LOGIN)
    time.sleep(10)
    # Login
    username = driver.find_element_by_id("j_username")
    password = driver.find_element_by_id("j_password")

    username.send_keys("tim.illsley@huntsmansavilerow.com")
    password.send_keys("46hun1118")

    driver.find_element_by_id("loginButton").click()
    time.sleep(10)
    # Search
    bSolbiati = True
    for bunch_list in bunch_lists:
        for bunch_code in bunch_list:
            if bSolbiati == False:
                driver.get(URL_SEARCH.format(bunch_code))
            else:
                driver.get("https://www.loropiana.com/textile/fabrics/solbiati")
                time.sleep(3 + random.random())
                driver.get(URL_SEARCH_SOLBIATI.format(bunch_code))

            time.sleep(10 +random.random())
            scroll(driver, 5)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            product_result = soup.find("ul", {"class":"product-listing product-grid"})
            if product_result is not None:
                product_lis = product_result.find_all("li")
                # get all information
                product_li_list = []
                for product_li in product_lis:
                    try:
                        tag_figure = product_li.find("figure", {"class":"product-list-preview-item"})
                        href = tag_figure.find("a")['href']
                        image_url_style = tag_figure.find("a").find("div", {"class":"product-list-preview-item-placeholder-image"})['style']
                        image_url = ""
                        if image_url_style is not None:
                            image_url =cssutils.parseStyle(image_url_style)['background-image'].replace('url(', '').replace(')', '').replace('"','')
                            image_url = URL_PREFIX + image_url
                        tag_title_prod = tag_figure.find("div", {"class":"cf"}).find("div", {"class":"title-prod"})
                        cloth_patthern_number = tag_title_prod.find('span').text
                        compostion_1 = tag_title_prod.find('h3').text
                        product_li_list.append({
                            "cloth_pattern_number": cloth_patthern_number,
                            "composition_1": compostion_1,
                            "image_url": image_url,
                            "href_url": URL_PREFIX + href,
                            "cloth_bunch": bunch_code
                        })
                    except Exception as e:
                        print("Error ->", e)

                for product in product_li_list:
                    try:
                        if len(product['href_url']) > 0:
                            driver.get(product['href_url'])
                            time.sleep(5 + random.random())
                            # get detail information
                            detail_soup = BeautifulSoup(driver.page_source,"html.parser")
                            tag_product_detail_wrapper = detail_soup.find("div", {"class":"product-details-panel-wrapper"})
                            if tag_product_detail_wrapper is not None:
                                tag_product_detail= tag_product_detail_wrapper.find("div", {"class":"product-details-panel"})
                                price = ""
                                width = ""
                                weight = ""
                                try:
                                    price = driver.find_element_by_xpath("//div[@class='product-details-panel']/div[@class='ten_col']/div[@class='col span_10_of_10-mobile span_8_of_10-tablet']/div[@class='pdp-detail-cell']/div[@class='product-details']/div/span[@class='unitPrice right']").text.split("/")[0].replace("£","").strip()
                                except Exception as e:
                                    print("Error to get price value", e)
                                try:
                                    tag_product_info = tag_product_detail.find("div", {"class": "pdp-desktop"}).find("div",{"class":"ten_col noVerticalGap"}).find("div", {"class":"col span_4_of_10 productinfos"}).findAll("div", {"class":"sectionProductInfo"})[1]
                                except Exception as e:
                                    print("Error to get detail information", e)
                                try:
                                    tag_tables_infos = tag_product_info.find("div", {"class":"tabbody"}).find("div",{"class":"product-classifications"}).find("table", {"class":"table"}).find("tbody").findAll("tr")
                                except Exception as e:
                                    print("Error to get table tag", e)
                                try:
                                    width = tag_tables_infos[0].findAll("td")[1].text.split("&nbsp")[0].replace("\n","\t").replace("\t","").strip().split("\t")[0].strip()
                                    weight = tag_tables_infos[2].findAll("td")[1].text.split("&nbsp")[0].replace("\n","\t").replace("\t","").strip().split("\t")[0].strip()
                                except Exception as e:
                                    print("Error to get table information width & weight", e)

                                #write file
                                write_data = {
                                    "cloth_pattern_number": product['cloth_pattern_number'],
                                    "composition_1": product['composition_1'],
                                    "image_url": product["image_url"],
                                    "cloth_bunch": product["cloth_bunch"],
                                    "width": width,
                                    "weight_gms": weight,
                                    "supplier_name":"Loro Piana",
                                    "colour": "",
                                    "price_per_meter":float(price),
                                    "selvedge": "",
                                    "dye": "",
                                    "weave": "",
                                    "design":""
                                }
                                with open("loro_piana_solbiati.json", "a") as f:
                                    json.dump(write_data, f, indent=4)
                                    f.write(",")
                                print("**********************", str(bunch_code) + " -> " +  str(product['cloth_pattern_number']) )

                            # time.sleep(5 + random.random())
                    except Exception as e:
                        print("Error in get detail->", e)
        bSolbiati = False
    return


if __name__ == '__main__':
    scrap_lora()