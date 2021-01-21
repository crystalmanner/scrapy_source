import pyMsql
import gsheet
import json
import re

def get_price(cloth_pattern_number):
    try:
        if 'F1300' in str(cloth_pattern_number):
            return 56
        int_cpt = int(cloth_pattern_number)
        if int_cpt in range(9400,9474): return 40
        elif int_cpt in range(8700, 8713):return 40
        elif int_cpt in range(8713,8729):return 34
        elif int_cpt in range(8729,8734):return 46.5
        elif int_cpt in range(8734,8737):return 40
        elif int_cpt in range(8737,8741):return 46.5
        elif int_cpt in range(8741,8743):return 54
        elif int_cpt in range(8743,8745):return 46.5
        elif int_cpt in range(8745,8753):return 28
        elif int_cpt in range(8753,8755):return 56
        elif int_cpt in range(8760,8766):return 28.75
        elif int_cpt in range(8770,8774):return 40
        elif int_cpt in range(6300,6304): return 59
        elif int_cpt in range(6304,6311): return 76
        elif int_cpt in range(6311,6315): return 45
        elif int_cpt in range(8900,8977): return 34
        elif int_cpt in range(4100,4119): return 37.5
        elif int_cpt in range(4200,4212): return 37.5
        elif int_cpt in range(4212,4220): return 44.5
        elif int_cpt in range(4220, 4227): return 55
        elif int_cpt in range(6100,6141) or int_cpt in range(6800,6824): return 41.25
        elif int_cpt in range(8400,8433) or int_cpt ==8435 : return 62
        elif int_cpt in range(8433,8435): return 54
        elif int_cpt in range(7600,7636): return 62.5
        elif int_cpt in range(6400,6497): return 36
        elif int_cpt in range(6200,6236): return  41
        elif int_cpt in range(7800,7820): return 61
        elif int_cpt in range(7916,7939): return 17.5
        elif int_cpt in range(7300,7329): return 28
        elif int_cpt in range(3400,3491): return 37.5
        elif int_cpt in range(5000,5202): return 50
        elif int_cpt in range(7400,7465): return 39.5
        elif int_cpt in range(7200,7231): return 47.5
        elif int_cpt in range(4600,4616): return 53
        elif int_cpt in range(4700,4725): return 49
        elif int_cpt in range(5100,5125) or int_cpt in range(5900,5916) or int_cpt in range(1500,1521): return 45
    except Exception as e:
        print("Error =>",e)

    return 0


def dugdale_main():
    new_list = []
    with open("dugdale_new.json", "r") as f:
        new_list = json.load(f)

    for item in new_list:
        print(item['cloth_pattern_number'])
        write_data = {
            'cloth_pattern_number': item['cloth_pattern_number'],
            'image_url': item['image_url'],
            'cloth_bunch': item['cloth_bunch'],
            'composition_1': item['composition1'] if 'composition1' in item else "",
            'supplier_name': 'Dugdale',
            "weight_gms": item['weight'] if 'weight' in item else "",
            "design": item['design'] if 'design' in item else "",
            'colour': item['colour'] if 'colour' in item else "",
            "width": item['width'] if 'width' in item else "",
            "weight_ozs": "",
            "selvedge": "",
            "dye": "",
            "weave": item['weave'] if 'weave' in item else "",
            "price_per_meter": float(get_price(item['cloth_pattern_number']))}
        try:
            pyMsql.save_scabal(write_data)
        except Exception as e:
            print("save data error", e, item['cloth_pattern_number'])
    return

if __name__ == '__main__':
    dugdale_main()