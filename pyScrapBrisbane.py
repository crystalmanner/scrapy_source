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
URL = 'http://www.brisbanemoss.co.uk/'

def brisbane_main():
    driver = webdriver.Chrome(executable_path=EXE_PATH, chrome_options=chrome_options)
    driver.get(URL)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    try:
        sub_urls = soup.find("div", {"id":"maincontent"}).find("div", {"class":"clothtypes"}).findAll("a")
        for sub_url in sub_urls:
            sub_href = URL + sub_url['href']
            image_url = ""
            cloth_bunch= ""
            cloth_bunch = sub_url.find("div", {"class":"homeimage"}).find("div", {"class":"homeimagelabel"}).text
            driver.get(sub_href)
            time.sleep(5)
            detail_soup = BeautifulSoup(driver.page_source, "html.parser")
            try:
                detail_divs = detail_soup.find("div", {"id":"maincontent"}).findAll("a")
                for detail_div in detail_divs:
                    width = ""
                    weight = ""
                    composition1=""
                    cloth_pattern_number = ""
                    div_tag = detail_div.find("div", {"class":"colourblock"})
                    image_url = URL + div_tag.find("img", {"class":"colourimage"})['src']
                    cloth_pattern_number = div_tag.find("h4").text
                    descriptions = div_tag.find("span", {"class":"small"})
                    for br in descriptions.select('br'):
                        br.replace_with(', ')
                    for description in descriptions.text.split(","):
                        if "WIDTH:" in description:
                            width = description.replace("WIDTH:", "").replace("cms", "").strip()
                        elif "WEIGHT" in description:
                            weight = description.replace("WEIGHT:","").replace("gsm", "").strip()
                        elif "COMPOSITION" in description:
                            composition1 = description.replace("COMPOSITION:","").strip()
                    write_data = {}
                    write_data.update({
                        "image_url": image_url,
                        "cloth_bunch": cloth_bunch,
                        "cloth_pattern_number": cloth_pattern_number,
                        "width": width,
                        "weight": weight,
                        "compostion1": composition1,
                        "suppler":"Brisban Moss"
                    })
                    with open("brisbanMoss_new.json", "a") as f:
                        json.dump(write_data, f, indent=4)
                        f.write(",")
            except Exception as e:
                print("Error get detail urls =>", e)



    except Exception as e:
        print("Error to get sub url =>", e)

    return

if __name__ == '__main__':
    brisbane_main()