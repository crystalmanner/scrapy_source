import pyMsql
import pyFabrics
import pyScrapScabal
import gsheet
import json

# 1. read items that have to be got from googlesheet
# 2. get information from api
# 3. get image scrapping
# 4: write data to wordpress db

def scabal_main():
    scabal_list = gsheet.parse_from_google()
    for scabal_item in scabal_list:
        for article_id in range(scabal_item['articles_from'], scabal_item['articles_to'] + 1):
            try:
                fabric_api_data = pyFabrics.get_fabric_info_by_id(article_id)
                if len(fabric_api_data['FABRICS']) > 0:
                    fabric_data_detail = pyFabrics.get_fabric_data_detail(fabric_api_data['FABRICS'][0])
                    fabric_data_detail.update({
                        "price_per_meter": float(scabal_item['price_per_meter_gbp']),
                        "supplier_name": "Scabal",
                        'image_url': pyScrapScabal.get_image_url(fabric_data_detail['cloth_pattern_number'])
                    })
                    pyMsql.save_scabal(fabric_data_detail)
                    print("saved to wp database: article_id =>", article_id)
            except Exception as e:
                print("Error in Scabal Main =>", e)


patch_list_one = [
    {'id': '402743', 'ppm': '27.65'},
    {'id': '402745', 'ppm': '27.65'},
    {'id': '402746', 'ppm': '27.65'},
    {'id': '402747', 'ppm': '27.65'},
    {'id': '402748', 'ppm': '27.65'},
    {'id': '402750', 'ppm': '27.65'},
    {'id': '402751', 'ppm': '27.65'},
    {'id': '402752', 'ppm': '27.65'},
    {'id': '402754', 'ppm': '22.4'},
    {'id': '402755', 'ppm': '22.4'},
    {'id': '402756', 'ppm': '22.4'},
    {'id': '402758', 'ppm': '22.4'},
]
def scabal_patch_one():
    for item in patch_list_one:
        article_id = item['id']
        try:
            fabric_api_data = pyFabrics.get_fabric_info_by_id(article_id)
            if len(fabric_api_data['FABRICS']) > 0:
                fabric_data_detail = pyFabrics.get_fabric_data_detail(fabric_api_data['FABRICS'][0])
                fabric_data_detail.update({
                    "price_per_meter": float(item['ppm']),
                    "supplier_name": "Scabal",
                    'image_url': pyScrapScabal.get_image_url(fabric_data_detail['cloth_pattern_number'])
                })
                pyMsql.save_scabal(fabric_data_detail)
                print(fabric_data_detail)
                print("saved to wp database: article_id =>", article_id)
        except Exception as e:
            print("Error in Scabal Main =>", e)

pathch_two_list = []
def scabal_patch_two():

    with open("scabal_missed_pattern_number.txt", "r") as f:
        for line in f.readlines():
            pathch_two_list.append(line.rstrip())

    scabal_list = gsheet.parse_from_google_patch()
    for scabal_item in scabal_list:
        try:
            if str(scabal_item['cloth_pattern_number']) in pathch_two_list:
                scabal_item.update({
                        "supplier_name": "Scabal",
                    'image_url': pyScrapScabal.get_image_url(scabal_item['cloth_pattern_number'])
                })
                pyMsql.save_scabal(scabal_item)
                print("saved to wp database: article_id =>", scabal_item['cloth_pattern_number'])
        except Exception as e:
            print("Error in Scabal Main =>", e)


patch_list_three = [
    {'id': '28154', 'ppm': '1675.00'},
    {'id': '28155', 'ppm': '1675.00'},
    {'id': '28156', 'ppm': '1675.00'},
    {'id': '28160', 'ppm': '2565.00'},
    {'id': '28163', 'ppm': '2565.00'},
    {'id': '28164', 'ppm': '2565.00'}
]
def scabal_patch_three():
    for item in patch_list_three:
        article_id = item['id']
        try:
            fabric_api_data = pyFabrics.get_fabric_info_by_id(article_id)
            if len(fabric_api_data['FABRICS']) > 0:
                fabric_data_detail = pyFabrics.get_fabric_data_detail(fabric_api_data['FABRICS'][0])
                fabric_data_detail.update({
                    "price_per_meter": float(item['ppm']),
                    "supplier_name": "Scabal",
                    'image_url': pyScrapScabal.get_image_url(fabric_data_detail['cloth_pattern_number'])
                })
                pyMsql.save_scabal(fabric_data_detail)
                print(fabric_data_detail)
                print("saved to wp database: article_id =>", article_id)
        except Exception as e:
            print("Error in Scabal Main =>", e)
if __name__ == '__main__':
    # scabal_patch_two()
    # scabal_patch_one()
    scabal_patch_three()
    # scabal_main()
