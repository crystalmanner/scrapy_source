import json
import time
from bs4 import BeautifulSoup

from selenium import  webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1980,1080')

EXE_PATH = "chromedriver.exe"


URL = 'https://www.themerchantfox.co.uk/pages/fox-brothers-cloth'
URL_PREFIX = 'https://www.themerchantfox.co.uk{}'

def get_sub_urls(source):
    sub_urls = []
    soup = BeautifulSoup(source, "html.parser")
    try:
        collection_lists_tag = soup.find("div", {"class":"CollectionList CollectionList--grid CollectionList--spaced"}).findAll("div", {"class":"CollectionItem"})
    except Exception as e:
        print("Error get colletion lists ->", e)

    for collection in collection_lists_tag:
        try:
            href = collection.find("div", {"class":"SectionHeader__ButtonWrapper"}).find('a')['href']
        except Exception as e:
            print("Error get href ->", e)
        try:
            category = collection.find("h2", {"class":"SectionHeader__Heading SectionHeader__Heading--emphasize Heading u-h1"}).text
        except Exception as e:
            print("Error get category ->", e)

        sub_urls.append({
            "category": category,
            "url":URL_PREFIX.format(href)
        })
    return  sub_urls


def scrap_fox_brother():
    driver = webdriver.Chrome(executable_path=EXE_PATH, chrome_options=chrome_options)
    # driver.get(URL)
    # time.sleep(5)
    # sub_urls = get_sub_urls(driver.page_source)
    #
    # all_data_urls = []
    # for sub_url in sub_urls:
    #     driver.get(sub_url['url'])
    #     time.sleep(5)
    #     soup = BeautifulSoup(driver.page_source, 'html.parser')
    #     try:
    #         div_collection_inner_product = soup.find("div", {"class":"CollectionInner__Products"})
    #         div_product_pagination = div_collection_inner_product.find("div", {"class":"Pagination Text--subdued"})
    #         page_cnt = 1
    #         if div_product_pagination is not None:
    #             page_hrefs = div_product_pagination.findAll("a", {'class':'Pagination__NavItem Link Link--primary'})
    #             page_cnt = int(page_hrefs[-2].text)
    #         for page_index in range(1, page_cnt+1):
    #             page_url = sub_url['url'] + "?page={}".format(page_index)
    #             driver.get(page_url)
    #             time.sleep(5)
    #             sub_soup = BeautifulSoup(driver.page_source, 'html.parser')
    #             try:
    #                 div_collection_inner_product_sub = sub_soup.find("div", {"class": "CollectionInner__Products"})
    #                 div_proudct_lists = div_collection_inner_product_sub.findAll('div', {"class":"Grid__Cell 1/2--phone 1/3--tablet-and-up 1/4--desk"})
    #                 for product in div_proudct_lists:
    #                     all_data_urls.append({
    #                         "url": URL_PREFIX.format(product.find('a',{'class':'ProductItem__ImageWrapper'})['href']),
    #                         "category":sub_url['category']
    #                     })
    #             except Exception as e:
    #                 print("get div collection inner prouect error", e)
    #     except Exception as e:
    #         print("get div collection inner prouect error", e)
    #
    # with open("fox_brother_all_url_new.json", "w") as f:
    #     json.dump(all_data_urls,f, indent=4)
    #
    # all_data_urls = []
    #
    # return
    with open("fox_brother_all_url_new.json", "r") as f:
        all_data_urls = json.load(f)
    for data_url in all_data_urls:
        driver.get(data_url['url'])
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        try:
            write_data = {}
            div_product_wrapper = soup.find("div", {"class":"Product__Wrapper"})
            image_url = "https:{}".format(div_product_wrapper.find("div", {"class":"Product__Slideshow Product__Slideshow--zoomable Carousel"})\
            .find("div", {"class":"Product__SlideItem Product__SlideItem--image Carousel__Cell is-selected"}).find('img')['src'])
            div_product_info = div_product_wrapper.find("div", {"class":"Product__InfoWrapper"}).find("div", {"class":"Container"}).find("div", {"class":"ProductMeta"})
            write_data.update({
                "image_url":image_url.split("?")[0]
            })
            title = ''
            price_per_meter = ''
            try:
                title =div_product_info.find('h1', {"class":"ProductMeta__Title Heading u-h2"}).text
            except Exception as e:
                print("Get title error=>", e)
            try:
                price_per_meter =div_product_info.find('div', {"class":"ProductMeta__PriceList Heading"}).text.replace("£","")
            except Exception as e:
                print("Get price error=>", e)
            write_data.update({
                'price_per_meter': price_per_meter
            })
            description_div = div_product_info.find("div", {"class":"ProductMeta__Description Rte"})

            h5_divs = description_div.findAll("h5")
            # for h5_div in h5_divs:
            #     if 'CODE:' in h5_div.text:
            #         write_data.update({
            #             "qds": h5_div.text.replace("CODE:","").strip().replace(" ","-")
            #         })
            #     if 'WEIGHT:' in h5_div.text:
            #         write_data.update({
            #             'weight': h5_div.text.replace("WEIGHT:","").strip().split(" ")[0]
            #         })

            write_data.update({"qds": h5_divs[1].text.replace("CODE:","").strip().replace(" ","-")})
            write_data.update({'weight': h5_divs[2].text.replace("WEIGHT:","").strip().split(" ")[0]})

            ul_tag = description_div.find('ul')
            li_tags = ul_tag.findAll('li')
            write_data.update({
                "width":li_tags[0].text.replace("width", "").replace("cm","").strip(),
                "composition1":li_tags[2].text,
                "cloth_bunch":data_url['category'],
                'supplier_name':'Fox Brothers'
            })
            with open("fox_brother_new_update_last.json", "a" , encoding="latin1") as f:
                json.dump(write_data, f, indent=4)
                f.write(",")

        except Exception as e:
            print("get div collection inner prouect error", e, title)


    return


if __name__ =='__main__':
    scrap_fox_brother()
