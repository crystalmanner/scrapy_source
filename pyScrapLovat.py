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
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1980,1080')

EXE_PATH = "chromedriver.exe"


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


def scrap_lovat():
    driver = webdriver.Chrome(executable_path=EXE_PATH, chrome_options=chrome_options)
    driver.get(URL)
    time.sleep(10)
    category_urls = []
    soup = BeautifulSoup(driver.page_source, "html.parser")

    try:
        li_tags = soup.find("div", {"class": "row three_column"}).find("div", {"class":"contents"}).find("ul", {"class":"list colx3_2"}).findAll("li")
        for li_tag in li_tags:
            h3_tag = li_tag.find("div", {'class':"list_text"}).find('h3',{"class":"large"})
            title = h3_tag.find('a').text
            href = h3_tag.find('a')['href']
            category_urls.append({
                "cloth_bunch": title,
                "href": href
            })
    except Exception as e:
        print("Error to get category lost = >", e)

    for cat_url in category_urls:
        driver.get(cat_url['href'])
        time.sleep(5)
        scroll(driver, 5)
        cat_soup = BeautifulSoup(driver.page_source, 'html.parser')
        sub_li_tags = cat_soup.find("ul", {"id":"swatches_list"}).findAll("li")

        cnt = 0
        for sub_li in sub_li_tags:
            try:
                sub_href = sub_li.find("div", {"class":"list_image"}).find("a")['href']
                driver.get(sub_href)
                time.sleep(5)
                detail_soup = BeautifulSoup(driver.page_source, 'html.parser')
                swatches_content_tag = detail_soup.find("div", {"id":"swatches_content"}).find("div", {"data-slick-index":str(cnt)})
                image_url = ""
                weight = ""
                composition1 = ""
                width = ""
                cloth_pattern_number = ""
                try:
                    image_div = swatches_content_tag.find("div", {"class":"swatch_image"})
                    image_url = image_div.find("a")['href']
                except Exception as e:
                    print("error getin image div", e)

                try:
                    text_div = swatches_content_tag.find("div", {"class":"swatch_text"})
                    for li_detail_tags in text_div.find("ul", {"class":"productdetails"}).findAll("li"):
                        span_value = li_detail_tags.find('span').text
                        if span_value == 'Weight:':
                            weight = li_detail_tags.text.replace("Weight:","").strip().split(" ")[0].replace("gm","")
                        elif span_value == 'Product Code:':
                            cloth_pattern_number = li_detail_tags.text.replace("Product Code:", "").strip()
                        elif span_value == 'Composition:':
                            composition1 = li_detail_tags.text.replace("Composition:", "").strip()
                        elif span_value == 'Width:':
                            width = li_detail_tags.text.replace("Width:", "").strip().replace("cm","")
                except Exception as e:
                    print("error get in text div", e)
                write_data = {
                    "image_url": image_url,
                    "cloth_pattern_number": cloth_pattern_number,
                    "weight": weight,
                    "width": width,
                    "composition1": composition1,
                    "cloth_bunch":cat_url['cloth_bunch'],
                    "suppler":"Lovat"
                }
                with open("Lovat_new.json", "a") as f:
                    json.dump(write_data, f,indent=4)
                    f.write(",")
            except Exception as e:
                print("Error in get sub href=>", e)
            cnt = cnt + 1



    return

if __name__ == '__main__':
    scrap_lovat()