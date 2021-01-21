import pyMsql
import pyFabrics
import pyScrapScabal
import gsheet
import pyScrapHarrison
import json
import re

def get_cloth_pattern_number(fox_code_list, item):
    if len(item['qds']) == 0:
        return ""
    for fox_code in fox_code_list:
        if item['qds'].strip() == fox_code['qds'].strip():
            return fox_code['shortend_code'].strip()
    return ""

def fox_main():
    fox_code_list = gsheet.parse_from_google_for_fox()
    new_fox_list = []
    with open("fox_brother_new_update_last.json", "r", encoding="latin1") as f:
        new_fox_list = json.load(f)

    print(len(new_fox_list))
    cnt = 0
    empty_pattenr_count = 1
    for fox in new_fox_list:
        pattern_number = get_cloth_pattern_number(fox_code_list, fox)
        if len(str(pattern_number)) == 0:
            pattern_number = "None_Fox_" + str(empty_pattenr_count)
            empty_pattenr_count+=1
        try:
            write_data = {
                "cloth_pattern_number": pattern_number,
                "image_url": fox['image_url'],
                "cloth_bunch": fox['qds'],
                "supplier_name": fox['supplier_name'],
                "colour": "",
                "composition_1": fox['composition1'] if 'composition1' in fox else "",
                "composition_2": fox['cloth_bunch'],
                "price_per_meter": fox['price_per_meter'] if 'price_per_meter' in fox else "",
                "weight_gms": fox['weight'] if 'weight' in fox else "",
                "design": "",
                "width": fox['width'] if 'width' in fox else "",
                "weight_ozs": "",
                "selvedge": "",
                "dye": "",
                "weave": "",
            }
        except Exception as e:
            print("error =>", e)
        print("***", cnt)
        cnt = cnt + 1
        try:
            pyMsql.save_scabal(write_data)
            print("saved to wp database: article_id =>", write_data['cloth_pattern_number'])
        except Exception as e:
            print("error =>", e, pattern_number)

    return

if __name__ == '__main__':
    fox_main()
