import json
import time
from bs4 import BeautifulSoup
import cssutils

from selenium import  webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1980,1080')

EXE_PATH = "chromedriver.exe"

URL = "https://www.harrisonsofedinburgh.com/search?criteria={}"
URL_NEW = "https://www.harrisonsofedinburgh.com"

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


def check_exist(list, item):
    for list_item in list:
        if item == list_item['pattern_number']:
            return True
    return False

def get_all_url(source):
    sub_urls = []
    soup = BeautifulSoup(source, "html.parser")
    try:
        brand_nav_divs = soup.find("header", {"id":"header"}).find("section", {"class":"nav-wrapper"}).find("nav", {"id":"secondary-nav"}).findAll("div", {"class":"brand-nav"})
    except Exception as e:
        print("Error in get nav divs->", e)

    for brand_div in brand_nav_divs:
        try:
            collections_div = brand_div.find("nav", {"class":"third-menu"}).find("div", {"class":"collections"}).findAll("div")
            for div_tag in collections_div:
                try:
                    sub_urls.append(div_tag.find("a", {"class":"wrap"})['href'])
                except Exception as e:
                    print("error to add sub url",e)
        except Exception as e:
            print("error to get url=>", e)

    return sub_urls

def scrap_harrison_new():
    driver = webdriver.Chrome(executable_path=EXE_PATH, chrome_options=chrome_options)
    driver.get(URL_NEW)
    time.sleep(10)
    all_urls = get_all_url(driver.page_source)
    print(all_urls)

    org_patterns = []
    with open("harrsion_datas_new.json", "r") as f:
        org_patterns = json.load(f)

    import re

    regex = re.compile('.*sample top.*')

    for url in all_urls:
        try:
            driver.get(url)
            scroll(driver, 5)
            write_data = {}
            soup = BeautifulSoup(driver.page_source, "html.parser")
            try:

                div_sample_tops = soup.find("div", {"class":"collection-grid"}).findAll("div", {"class":regex})
                for div_tag in div_sample_tops:
                    code = div_tag['id']
                    if check_exist(org_patterns, str(code)) == True:
                        continue
                    search_url = URL.format(code)
                    try:
                        driver.get(search_url)
                        time.sleep(5)
                        soup = BeautifulSoup(driver.page_source, "html.parser")
                        div_modal = soup.find("div", {"class": "modal show"})
                        if div_modal is not None:
                            div_detail = div_modal.find("div", {"class": "details"})
                            h2_value = div_detail.find("h2").text
                            if h2_value == 'Harrisons of Edinburgh':
                                bunch = 'Harrisons'  + "-" + div_detail.find("h3").text
                            elif h2_value == 'Porter & Harding':
                                bunch = 'P & H' + "-" + div_detail.find("h3").text
                            elif h2_value == 'Lear Browne & Dunsford':
                                bunch = 'LBD' + "-" + div_detail.find("h3").text
                            elif h2_value == 'W Bill':
                                bunch = 'WBILL' + "-" + div_detail.find("h3").text
                            elif h2_value == 'H Lesser & Sons':
                                bunch = 'HLESSER' + "-" + div_detail.find("h3").text
                            elif h2_value == 'Smith Woollens':
                                bunch = 'SMITHS' + "-" + div_detail.find("h3").text
                            else:
                                bunch = h2_value.replace(" ", "") + "-" + div_detail.find("h3").text
                            write_data.update({
                                "bunch": bunch.upper(),
                                "Supplier": "Harrisions"
                            })
                            # image Url
                            img_url_style = div_modal.find("div", {"class": "sample-thumbnail-modal"})['style']
                            if img_url_style is not None:
                                write_data.update({
                                    "pattern_number": code,
                                    "image_url": cssutils.parseStyle(img_url_style)['background-image'].replace('url(',
                                                                                                                '').replace(
                                        ')', '').replace('"', '').replace("c_fit,w_600,h_600,q_85/", '')

                                })
                            else:
                                write_data.update({
                                    "pattern_number": code,
                                    "image_url": ""
                                })
                            with open("harrsion_datas_new_omit.json", "a") as f:
                                json.dump(write_data, f, indent=4)
                                f.write(",")

                    except Exception as e:
                        print("error", e, code)
            except Exception as e:
                print("error to get div sample", e)
        except Exception as e:
            print("parsing data error in ", e, url)

    return

def scrap_harrison(article_id):

    harrison_patterns = []
    with open("harrison_pattern_number.txt", "r") as f:
        for line in f.readlines():
            harrison_patterns.append(line.rstrip())
    brestart = True
    org_patterns = []
    with open("harrsion_images.json","r") as f:
        org_patterns = json.load(f)

    for code in harrison_patterns:
        if check_exist(org_patterns, str(code)) == True:
            continue
        url = URL.format(code)
        if brestart == True:
            write_data = {}
            print("New Code =>", str(code))
            try:
                driver = webdriver.Chrome(executable_path=EXE_PATH, chrome_options=chrome_options)
                driver.get(url)
                time.sleep(10)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                div_modal = soup.find("div", {"class":"modal show"})
                ret_data = {}
                if div_modal is not None:
                    div_detail = div_modal.find("div", {"class":"details"})
                    bunch = div_detail.find("h2").text + " "+ div_detail.find("h3").text
                    write_data.update({
                        "bunch": bunch,
                        "Supplier": "Harrisions"
                    })
                    # image Url
                    img_url_style = div_modal.find("div", {"class": "sample-thumbnail-modal"})['style']
                    if img_url_style is not None:
                        write_data.update({
                            "pattern_number": code,
                            "image_url": cssutils.parseStyle(img_url_style)['background-image'].replace('url(', '').replace(')', '').replace('"','').replace("c_fit,w_600,h_600,q_85/",'')

                        })
                    else:
                        write_data.update({
                            "pattern_number": code,
                            "image_url": ""
                        })
                    with open("harrsion_images_new.json", "a") as f:
                        json.dump(write_data, f, indent=4)
                        f.write(",")

            except Exception as e:
                print("error", e, code)
                pass

    return



if __name__ == '__main__':
    scrap_harrison_new()