import pyMsql
import pyFabrics
import pyScrapScabal
import gsheet
import pyScrapHarrison
import json
import re

# 1. read items that have to be got from googlesheet
# 2. get information from api
# 3. get image scrapping
# 4: write data to wordpress db

# match = re.match(r"([a-z]+)([0-9]+)", 'foofo21', re.I)
# if match:
#     items = match.groups()
#     # items is ("foo", "21")

def get_image_url(img_list, code):
    for item in img_list:
        if str(code) == item['pattern_number']:
            return item['image_url']
    return ''



def get_digit_postion(pattern_number):
    m = re.search(r"\d", pattern_number)
    if m is not None:
        return m.start()
    return -1


def get_item_info(item_list, pattern_number):
    for item in item_list:
        m_pns_first_digit_pos = get_digit_postion(str(item['pattern_number_start']))
        m_pns_string = ''
        m_pns_number = 0
        if m_pns_first_digit_pos !=-1:
            m_pns_string = str(item['pattern_number_start'])[0: m_pns_first_digit_pos]
            m_pns_number = (str(item['pattern_number_start'])[m_pns_first_digit_pos:])
        else:
            m_pns_number = (str(item['pattern_number_start']))
        m_pne_string = ''
        m_pne_number = 0
        m_pne_first_digit_pos = get_digit_postion(str(item['pattern_number_end']))
        if m_pne_first_digit_pos !=-1:
            m_pne_string = str(item['pattern_number_end'])[0: m_pne_first_digit_pos]
            m_pne_number = (str(item['pattern_number_end'])[m_pne_first_digit_pos:])
        else:
            m_pne_number = ((item['pattern_number_end']))

        m_pn_first_digit_pos = get_digit_postion(str(pattern_number))
        m_pn_string = ''
        m_pn_number = 0
        if m_pn_first_digit_pos != -1:
            m_pn_string = str(pattern_number)[0: m_pn_first_digit_pos]
            m_pn_number = (str(pattern_number)[m_pn_first_digit_pos:])
        else:
            m_pn_number = (str(pattern_number))

        if m_pns_string == m_pn_string:
            if m_pn_number.isdigit():
                if int(m_pn_number) in range(int(m_pns_number), int(m_pne_number)+1):
                    return item
    return {}
def harrison_main():
    g_itemInfo = []
    img_list = []
    with open("harrsion_datas_new.json", "r", encoding="latin1") as f:
        img_list = json.load(f)
    with open("harrison_price.json", "r", encoding="latin1") as f:
        g_itemInfo = json.load(f)

    for image_item in img_list:
        item_info = get_item_info(g_itemInfo,str(image_item['pattern_number']))
        write_data= {}
        write_data.update({
            "cloth_pattern_number": image_item['pattern_number'],
            "image_url": image_item['image_url'],
            "cloth_bunch": image_item['bunch'],
            "supplier_name": image_item['Supplier'],
            "colour": "",
            "composition_1": "",
            "price_per_meter": "",
            "weight_gms": "",
            "design": "",
            "width": "",
            "weight_ozs": "",
            "selvedge": "",
            "dye": "",
            "weave": "",
        })
        if len(item_info) > 0:
            write_data.update({
                "composition_1": item_info['composition'] if 'composition' in item_info else '',
                "price_per_meter": item_info['price_per_meter'] if 'price_per_meter' in item_info else '',
                'width': item_info['width'] if 'width' in item_info else '',
                'weight_gms': item_info['weight gms'] if 'weight gms' in item_info else '',
                'weight_ozs': item_info['weight ozs'] if 'weight ozs' in item_info else ''
            })
        try:
            pyMsql.save_scabal(write_data)
            print("saved to wp database: article_id =>", write_data['cloth_pattern_number'])
        except Exception as e:
            print("error =>", e, image_item['pattern_number'])

if __name__ == '__main__':
    harrison_main()

