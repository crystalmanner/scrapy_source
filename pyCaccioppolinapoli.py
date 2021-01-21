import pyMsql
import gsheet
import json
import re

def get_bunch_number_price(cloth_pattern_number):
    cpn = int(cloth_pattern_number)
    if cpn in range(300101, 300160):
        return float(84.00)
    elif cpn in range(300160, 300170):
        return float(45)
    elif cpn in range(300201, 300227):
        return float(84.00)
    elif cpn in range(300227, 300236):
        return float(76)
    elif cpn in range(300236, 300251):
        return float(51)
    elif cpn in range(300301, 300376):
        return float(54)
    elif cpn in range(300401, 300413):
        return float(68)
    elif cpn in range(300413, 300420):
        return float(59)
    elif cpn in range(300420, 300433):
        return float(47)
    elif cpn in range(300441, 300451):
        return float(51)
    elif cpn in range(300451, 300462):
        return float(45)
    elif cpn in range(300462, 300470):
        return float(53)
    elif cpn in range(300470, 300483):
        return float(47)
    else:
        return 0


def caccioppolinapoli_main():
    new_list = []
    with open("caccioppolinapoli_new.json", "r", encoding="latin1") as f:
        new_list = json.load(f)

    for item in new_list:
        print(item['cloth_pattern_number'])
        write_data = {
            'cloth_pattern_number': item['cloth_pattern_number'],
            'image_url': item['image_url'],
            'cloth_bunch': item['cloth_bunch'],
            'composition_1': item['composition1'] if 'composition1' in item else "",
            'supplier_name': 'Caccioppolinapoli',
            "weight_gms": item['weight'] if 'weight' in item else "",
            "design": item['design'] if 'design' in item else "",
            'colour': item['colour'] if 'colour' in item else "",
            "width": item['width'] if 'width' in item else "",
            "weight_ozs": "",
            "selvedge": "",
            "dye": "",
            "weave": item['weave'] if 'weave' in item else "",
            "price_per_meter": float(get_bunch_number_price(item['cloth_pattern_number']))}
        try:
            pyMsql.save_scabal(write_data)
        except Exception as e:
            print("save data error", e, item['cloth_pattern_number'])

    return

if __name__ == '__main__':
    caccioppolinapoli_main()
