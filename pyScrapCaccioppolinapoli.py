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
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1980,1080')

EXE_PATH = "chromedriver.exe"

URL = 'http://www.caccioppolinapoli.it/shop/categoria-prodotto/spring-summer-2020/page/{}/'



def scrap_caccioppolinapoli():
    driver = webdriver.Chrome(executable_path=EXE_PATH, chrome_options=chrome_options)
    next_href = URL.format("1")
    while True:
        driver.get(next_href)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        try:
            main_div = soup.find("div", {"id": "infinite-page-wrapper"}).find("div",{"class":"infinite-content-area"}).find("div",{"class":"woocommerce gdlr-core-product-item gdlr-core-item-pdb clearfix gdlr-core-product-style-grid"})
            content_div = main_div.find("div", {"class":"gdlr-core-product-item-holder gdlr-core-js-2 clearfix"})
            pagination_div = main_div.find("div", {"class":"gdlr-core-pagination gdlr-core-style-round gdlr-core-right-align gdlr-core-item-pdlr"})
            try:
                regex = re.compile('.*gdlr-core-item-list.*')
                div_items = content_div.findAll("div", {"class": regex})
                for div_item in div_items:
                    image_url = ''
                    compostion1 = ""
                    weight = ""
                    height = ""
                    design = ""
                    cloth_pattern_number = ""
                    cloth_bunch = ""
                    use = ""
                    write_data = {}
                    try:
                        image_url = div_item.find("div", {"class":"gdlr-core-product-grid"}).find("div",{"class":"gdlr-core-product-thumbnail gdlr-core-media-image gdlr-core-zoom-on-hover"}).find('img')['src']
                    except Exception as e:
                        print("Error get image_url", e)
                    try:
                        sub_href = div_item.find("div", {"class":"gdlr-core-product-grid"}).find("div",{"class": "gdlr-core-product-grid-content-wrap"}).find("a")['href']
                        driver.get(sub_href)
                        time.sleep(5)
                        sub_soup = BeautifulSoup(driver.page_source, "html.parser")
                        try:
                            sub_main_div = sub_soup.find("div", {"id": "infinite-page-wrapper"}).find("div", {
                                "class": "infinite-content-container infinite-container"}).find("div", {
                                "class": "infinite-content-area infinite-item-pdlr infinite-sidebar-style-none clearfix"}).find(
                                "div", {"class": "summary entry-summary"})
                            description_tag = sub_main_div.find("div", {"class":"item-description"})
                            try:
                                cloth_pattern_number = description_tag.find("p").find("span").text.replace("Art.", "").strip()
                            except Exception as e:
                                print("Error cloth pattern number ", e)

                            for tr_tag in description_tag.find("table").find("tbody").findAll("tr"):
                                td_tags = tr_tag.findAll("td")
                                if 'Composition' in td_tags[0].text:
                                    compostion1 = td_tags[-1].text.strip()
                                elif 'Weight' in td_tags[0].text:
                                    weight = td_tags[-1].text.replace("gr.","").strip()
                                elif 'Height' in td_tags[0].text:
                                    height = td_tags[-1].text.replace("cm", "").strip()
                                elif 'Design' in td_tags[0].text:
                                    design = td_tags[-1].text.strip()
                                elif 'Use' in td_tags[0].text:
                                    use = td_tags[-1].text.strip()

                            category_tag = sub_main_div.find("div", {"class":"product_meta infinite-title-font"}).find("span", {"class":"posted_in"})
                            cloth_bunch = category_tag.find("a").text
                            write_data.update({
                                'image_url': image_url,
                                "composition1": compostion1,
                                "height": height,
                                "design": design,
                                "cloth_pattern_number": cloth_pattern_number,
                                "cloth_bunch": cloth_bunch + "-" + use.upper(),
                                "weight":weight
                            })
                            with open("caccioppolinapoli_new.json", "a") as f:
                                json.dump(write_data, f, indent=4)
                                f.write(",")
                        except Exception as e:
                            print("Error get sub main div", e)
                    except Exception as e:
                        print("Error get sub href", e)
            except Exception as e:
                print("Error in item dev->", e)

            next_page_tag =pagination_div.find("a",{"class":"next page-numbers"})
            if next_page_tag is None:
                break
            else:
                next_href = next_page_tag['href']
        except Exception as e:
            print("Error in main div->", e)
            break

    return

if __name__ == '__main__':
    scrap_caccioppolinapoli()

