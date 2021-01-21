import pyMsql
import json

def get_price(cloth_pattern_number):
    try:
        int_cpn = int(cloth_pattern_number)
    except Exception as e:
        print("Error convert to int ->", e)
        return 0
    if int_cpn in range(1000, 1005) or int_cpn in range(1051, 1053):
        return 170
    elif int_cpn in range(1005,1007) or int_cpn in range(1008,1010):
        return 120
    elif int_cpn in range(1013, 1037) or int_cpn == 1053:
        return 45
    elif int_cpn == 1007 or int_cpn in range(1010,1013) or int_cpn in range(1037, 1048):
        return 65
    elif int_cpn in range(4000, 4042) or int_cpn in range(4022,4048):
        return 35
    elif int_cpn in range(4042, 4044):
        return 45
    elif int_cpn in range(5000,5022) or int_cpn in range(5042, 5046):
        return 55
    elif int_cpn in range(5022, 5026) or int_cpn in range(5031, 5042):
        return 64
    elif int_cpn in range(5027,5030) or int_cpn in range(5046, 5048):
        return 55
    elif int_cpn in range(6000,6010) or int_cpn == 6036:
        return 53
    elif int_cpn in range(6010,6020) or int_cpn in range(6038, 6056):
        return 55
    elif int_cpn in range(6020, 6030) or int_cpn in range(6033,6036) or int_cpn == 6037:
        return 60
    elif int_cpn in range(6030,6033):
        return 40
    elif int_cpn in range(16000, 16050):
        return 55
    elif int_cpn in range(25000,25035):
        return 48
    elif int_cpn in range(17000,17024):
        return 110
    elif int_cpn in range(17024,17031):
        return  165
    elif int_cpn in range(12050, 12060):
        return 130
    elif int_cpn in range(21000,21012):
        return 190
    elif int_cpn in range(21012,21021):
        return 260
    elif int_cpn in range(21021,21029):
        return 290
    elif int_cpn in range(27000,27067):
        return 45
    elif int_cpn in range(8000,8033):
        return 40
    elif int_cpn in range(19035,19085):
        return 44
    elif int_cpn in range(11000,11035):
        return 110
    elif int_cpn in range(15000,15042):
        return 60
    elif int_cpn in range(10000,10062):
        return 59
    elif int_cpn in range(22000,22075):
        return 55
    elif int_cpn in range(3000,3092):
        return 50
    elif int_cpn in range(7100,7142):
        return 225
    elif int_cpn in range(20000, 20046):
        return 115
    elif int_cpn in range(23000,23011):
        return 120
    elif int_cpn in range(23011,23026):
        return 99
    elif int_cpn in range(18000,18004):
        return 260
    elif int_cpn in range(18006,18024):
        return 110
    elif int_cpn in range(18024, 18028):
        return 80
    elif int_cpn in range(24001,24064):
        return 48
    elif int_cpn in range(12000,12050) or int_cpn ==12060 or int_cpn in range(12063, 12065) or int_cpn in range(14000,14052) or int_cpn in range(14061, 14063):
        return 130
    else:
        return 0

def Standeven_main():
    new_list = []
    with open("standeven_new.json", "r", encoding="latin1") as f:
        new_list = json.load(f)

    for item in new_list:
        print(item['cloth_pattern_number'])
        write_data = {
        'cloth_pattern_number': item['cloth_pattern_number'],
        'image_url': item['image_url'],
        'cloth_bunch': item['cloth_bunch'],
        'composition_1': item['composition1'] if 'composition1' in item else "",
        'supplier_name': 'Standeven',
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


if __name__ == '__main__':
    Standeven_main()