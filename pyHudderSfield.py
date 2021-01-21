import pyMsql
import gsheet
import json
import re


def huddersfield_main():
    new_lists = []
    with open("huddersfield.json", "r", encoding="latin1") as f:
        new_lists = json.load(f)
    for item in new_lists:
        try:
            write_data = {}
            write_data.update({
                'cloth_pattern_number': item['cloth_pattern_number'],
                'image_url': item['image_url'],
                'cloth_bunch': item['cloth_bunch'],
                'composition_1': item['composition1'] if 'composition1' in item else "",
                'supplier_name': 'Huddersfield Fine Worsteds',
                "weight_gms": item['weight'] if 'weight_gm' in item else "",
                "design": item['design'] if 'design' in item else "",
                'colour': item['colour'] if 'colour' in item else "",
                "width": "",
                "weight_ozs": "",
                "selvedge": "",
                "dye": "",
                "weave": item['weave'] if 'weave' in item else "",
                "price_per_meter":item['price'] if 'price' in item else ""
            })
        except Exception as e:
            print("error in scrapped data")
        try:
            pyMsql.save_scabal(write_data)
        except Exception as e:
            print("Error to save database")

    return

if __name__ == '__main__':
    huddersfield_main()
