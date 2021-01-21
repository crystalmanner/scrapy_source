import pyMsql
import json

lovat_list = []
def get_price(bunch_code):
    if bunch_code == 'The Kirkton':
        return 23.50
    elif bunch_code == 'The Teviot':
        return 27.30
    elif bunch_code == 'The Ettrick':
        return 32.90

def lovat_main():

    with open("Lovat_new.json", "r", encoding="latin1") as f:
        lovat_list = json.load(f)
    for lovat in lovat_list:
        write_data = {
            'cloth_pattern_number': lovat['cloth_pattern_number'],
            'image_url': lovat['image_url'],
            'cloth_bunch': lovat['cloth_bunch'],
            'composition_1': lovat['composition1'] if 'composition1' in lovat else "",
            'supplier_name': 'Lovat',
            "weight_gms": lovat['weight'] if 'weight' in lovat else "",
            "design": lovat['design'] if 'design' in lovat else "",
            'colour': lovat['colour'] if 'colour' in lovat else "",
            "width": lovat['width'] if 'width' in lovat else "",
            "weight_ozs": "",
            "selvedge": "",
            "dye": "",
            "weave": lovat['weave'] if 'weave' in lovat else "",
            "price_per_meter": float(get_price(lovat['cloth_bunch']))
        }

        pyMsql.save_scabal(write_data)

    return

if __name__ == '__main__':
    lovat_main()