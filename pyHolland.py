import pyMsql
import gsheet
import json
import re

def check_exist_in_list(org_list, item):

    for org in org_list:
        if org['cloth_pattern_number'] == item['cloth_pattern_number']:
            return org
    return {}

def holland_main():
    new_holand_list = []
    with open("holland_sherry_new_update.json", "r") as f:
        new_holand_list = json.load(f)
    org_holland_list = gsheet.parse_from_google_for_holland()

    for new_holand in new_holand_list:
        write_data = {
            'cloth_pattern_number': new_holand['cloth_pattern_number'],
            'image_url': new_holand['image_url'],
            'cloth_bunch': new_holand['cloth_bunch'],
            'composition_1': new_holand['composition1'] if 'composition1' in new_holand else "",
            'supplier_name': 'Holland and Sherry',
            "weight_gms": new_holand['weight_gm'] if 'weight_gm' in new_holand else "",
            "design": new_holand['design'] if 'design' in new_holand else "",
            "width": "",
            "weight_ozs": "",
            "selvedge": "",
            "dye": "",
            "weave": ""
        }
        org_holland = check_exist_in_list(org_holland_list, new_holand)
        if len(org_holland) > 0:
                write_data.update({
                    'price_per_meter': org_holland['price_per_meter'],
                })
        try:
            pyMsql.save_scabal(write_data)
        except Exception as e:
            print("Error to save database")
    return


if __name__ == '__main__':
    holland_main()
