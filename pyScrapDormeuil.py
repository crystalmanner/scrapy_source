import json
import time
from bs4 import BeautifulSoup
import cssutils

from selenium import  webdriver
prefs = {
  "translate_whitelists": {"fr":"en"},
  "translate":{"enabled":"true"}
}

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1980,1080')
chrome_options.add_experimental_option("prefs", prefs)

EXE_PATH = "chromedriver.exe"

URL = 'https://www.dormeuil.com{}'
COLLECTION_URL = 'https://www.dormeuil.com/en/fabrics/collection/'
BEST_SELLERS_URL = 'https://www.dormeuil.com/en/fabrics/ranges/best-sellers/'
INNOVATIVE_CLOTHS_URL = 'https://www.dormeuil.com/fr/tissus/gammes/innovative-cloths/'
ULTIMATE_LUXURY_URL ='https://www.dormeuil.com/fr/tissus/gammes/ultimate-luxury/'


def remove_duplicated_dict_from_dictlist(org_list):
    # return [dict(t) for t in {tuple(d.items()) for d in org_list}]
    out = []
    for v in org_list:
        if v not in out:
            out.append(v)
    return out

def get_collection_sub_urls(source):
    sub_urls = []
    soup = BeautifulSoup(source, "html.parser")
    try:
        article_tags = soup.find("div", {"id":"allContent"}).find("div", {"class":"content"}).findAll("article", {"class":"gabarit1 gammeshome"})
    except Exception as e:
        print("Error in Collection Sub Article_Tags->", e)

    for article in article_tags:
        try:
            bunch_url_div = article.find('div', {"class":"nomtissu"})
            href_val = bunch_url_div.find("a")['href']
            bunch_val = bunch_url_div.find('a').text
        except Exception as e:
            print("Error in get bunch div->", e)
        sub_urls.append({'url': href_val, 'bunch': bunch_val})
    return sub_urls


def get_range_sub_urls(source):
    sub_urls = []
    soup = BeautifulSoup(source, "html.parser")
    try:
        article_tags = soup.find("div", {"id": "allContent"}).find("div", {"class": "content"}).findAll("div", {
            "class": "gabarit3 gammesliste"})
    except Exception as e:
        print("Error in Range Sub Article_Tags->", e)

    for article in article_tags:
        try:
            div_columns = article.findAll("div", {"class":"column"})
            for div_column in div_columns:
                try:
                    bunch_url_div = div_column.find('div', {"class":"verticalCenter zonec"})
                    href_val = bunch_url_div.find("a")['href']
                    bunch_val = bunch_url_div.find('a').text
                except Exception as e:
                    print("Error bunch div", e)
                sub_urls.append({'url': href_val, 'bunch': bunch_val})
        except Exception as e:
            print("Error in get column div->", e)


    return sub_urls


def scrap_dormeuil():
    driver = webdriver.Chrome(executable_path=EXE_PATH, chrome_options=chrome_options)
    driver.get(COLLECTION_URL)
    time.sleep(5)
    collection_sub_urls = get_collection_sub_urls(driver.page_source)
    driver.get(BEST_SELLERS_URL)
    time.sleep(5)
    range_sub_urls = get_range_sub_urls(driver.page_source)
    driver.get(INNOVATIVE_CLOTHS_URL)
    time.sleep(5)
    range_sub_urls.extend(get_range_sub_urls(driver.page_source))
    driver.get(ULTIMATE_LUXURY_URL)
    time.sleep(5)
    range_sub_urls.extend(get_range_sub_urls(driver.page_source))

    collection_sub_urls.extend(range_sub_urls)
    print(len(collection_sub_urls))
    collection_sub_urls = remove_duplicated_dict_from_dictlist(collection_sub_urls)
    print(len(collection_sub_urls))
   # Dorsilk

    for collection_sub_url in collection_sub_urls:
        driver.get(URL.format(collection_sub_url['url']))
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        try:
            data_div_tags = soup.find("div", {"id": "allContent"}).find("div", {"class": "content"}).find("article").find("section").findAll("div", {"class":"gabarit5 listetissu marginTopSmall"})
        except Exception as e:
            print("Error in Collection Sub Article_Tags->", e)
        pass

        for data_div in data_div_tags:
            try:
                column2_tags = data_div.findAll('div', {"class":'column2'})
            except Exception as e:
                print("Error Column ", e)
            for column2_tag in column2_tags:
                write_data = {}
                cloth_pattern_number = ""
                image_url = ""
                composition = ""
                weight = ""
                try:
                    cloth_pattern_number = column2_tag['data-ref']
                    write_data.update({
                        'cloth_pattern_number': cloth_pattern_number
                    })
                    try:
                        image_url = column2_tag.find('a')['data-src']
                    except Exception as e:
                        print("image url error", e)
                    write_data.update({
                        'image_url': URL.format(image_url.replace('/HR/', '/LR/'))
                    })
                    try:
                        info_span = column2_tag.find('div', {"class": "info"}).findAll('span')
                        composition = info_span[2].text.replace(" ","")
                        weight = info_span[3].text.replace("g", "")
                    except Exception as e:
                        print("info span error")
                    write_data.update({
                        'composition_1': composition.strip(),
                        'weight': weight,
                        'bunch': collection_sub_url['bunch']
                    })
                    with open("dormeuil_data.json", "a", encoding='latin1') as f:
                        json.dump(write_data, f, indent=4)
                        f.write(",")
                    print("**********************",
                          str(write_data['bunch']) + "--" + str(write_data['cloth_pattern_number']))
                except Exception as e:
                    print ("cloth pattern number error ", e)
    return

if __name__ =='__main__':
    scrap_dormeuil()
