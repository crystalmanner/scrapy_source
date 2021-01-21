import json
import time
from bs4 import BeautifulSoup
import cssutils

from selenium import  webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1980,1080')


EXE_PATH = "chromedriver.exe"
URL = "https://shop.hfwltd.com"
FIRST_URL = "https://shop.hfwltd.com/collection/76"

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

def get_all_sub_urls(source):
    sub_urls = []
    soup = BeautifulSoup(source, "html.parser")
    try:
        li_tags = soup.find("div", {"id": "Content"}).find("div", {"class": "category-section"}).find("ul").findAll("li")
    except Exception as e:
        print("Error in get nav divs->", e)

    for li_tag in li_tags:
        try:
            sub_urls.append({
                "href": URL + li_tag.find("a")['href'],
                "cloth_bunch": li_tag.find('a').text
            })
        except Exception as e:
            print("error to get url=>", e)

    return sub_urls

def scrap_huddersfield():
    driver = webdriver.Chrome(executable_path=EXE_PATH, chrome_options=chrome_options)
    driver.get(FIRST_URL)
    time.sleep(5)
    scroll(driver, 5)
    url_infos = get_all_sub_urls(driver.page_source)

    for url_info in url_infos:
        href = url_info['href']
        cloth_bunch = url_info['cloth_bunch']
        driver.get(href)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        try:

            div_product_lists = soup.find("div", {"id":"Content"}).find("div", {"class":"productList"}).findAll("div", {"class":"product"})
            for product in div_product_lists:
                write_data = {}
                try:
                    write_data.update({
                        "cloth_pattern_number": product.find("div", {"class":"product-title"}).text.replace("Product:", "").strip(),
                        "image_url": URL + product.find("div", {"class":"image"}).find("a")['href'],
                        "cloth_bunch": cloth_bunch
                    })
                    for li_tag in product.findAll('li'):
                        label = li_tag.find('span', {"class":"label"}).text
                        data = li_tag.find('span', {"class":'data'}).text
                        if label == 'Fabric':
                            write_data.update({"composition1": data})
                        elif label == 'Weight':
                            write_data.update({"weight": data})
                        elif label == 'Colour':
                            write_data.update({"colour": data})
                        elif label == 'Design':
                            write_data.update({"design": data})
                        elif label == 'Weave':
                            write_data.update({"weave": data})
                        elif label == 'Price':
                            write_data.update({"price": data.split("/")[0].replace("£","").strip() })
                    with open("huddersfield.json", "a", encoding="latin1") as f:
                        json.dump(write_data,f, indent=4)
                        f.write(",")
                except Exception as e:
                    print("Error to get Information->", e)

        except Exception as e:
            print("error get product list->", e)

    return

if __name__ == '__main__':
    scrap_huddersfield()