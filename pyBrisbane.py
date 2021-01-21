import pyMsql
import gsheet
import json
import re

def get_price(cloth_pattern_number):
    ucpn = str(cloth_pattern_number).replace(" ","").upper()
    if 'Chiltern'.upper() in ucpn: return 6.95
    elif 'Cotswold'.upper() in ucpn:return 8.25
    elif '530' in ucpn: return 7.25
    elif '531' in ucpn: return 7.25
    elif 'Coniston'.upper() in ucpn or '568' in ucpn: return 7.95
    elif '3101X' in ucpn: return 11.25
    elif 'GS20' in ucpn: return 17.50
    elif '3124' in ucpn: return 10.95
    elif 'T1' in ucpn: return 9.75
    elif 'Yew'.upper() in ucpn: return 8.40
    elif "Sycamore".upper() in ucpn: return 8.95
    elif '3103' in ucpn: return 7.75
    elif 'Calder' in ucpn: return 8.75
    elif 'M1A' in ucpn: return 10.25
    elif 'M1B' in ucpn: return 9.75
    elif 'M25' in ucpn: return 7.95
    elif '52' in ucpn: return 7.45
    elif 'Haworth'.upper() in ucpn: return 6.95
    elif 'Madrid'.upper() in ucpn: return 7.95
    elif 'Napoli'.upper() in ucpn: return 8.95
    elif 'Shakespeare'.upper() in ucpn: return 6.50
    elif 'Turner'.upper() in ucpn: return 6.25
    elif 'Tennyson'.upper() in ucpn: return 7.45
    elif 'Keats'.upper() in ucpn or 'Wordsworth'.upper() in ucpn: return 5.95
    elif 'Blake'.upper() in ucpn: return 6.50
    elif 'Rye'.upper() in ucpn: return 4.95
    elif 'Byron'.upper() in ucpn: return 4.25
    elif 'Dreem'.upper() in ucpn: return 5.45
    elif 'Milton'.upper() in ucpn: return 4.50
    elif 'Bronte'.upper() in ucpn: return 7.45
    elif 'Montecarlo'.upper() in ucpn: return 6.85
    elif 'Aztec'.upper() in ucpn: return 5.50
    elif 'Pique'.upper() in ucpn: return  6.25
    elif 'Althorp'.upper() in ucpn: return 18.75
    elif 'Sherbourne'.upper() in ucpn: return 15.5
    elif 'Osborne'.upper() in ucpn: return 23.45
    elif 'Stowe'.upper() in ucpn: return 21
    else:
        print("non exist price list ",ucpn )
        return 0

    return

def brisbane_main():
    new_list = []
    with open("brisbanMoss_new.json", "r") as f:
        new_list = json.load(f)

    for item in new_list:
        print(item['cloth_pattern_number'])
        write_data = {
            'cloth_pattern_number': str(item['cloth_pattern_number']).upper(),
            'image_url': item['image_url'],
            'cloth_bunch': item['cloth_bunch'],
            'composition_1': item['compostion1'] if 'compostion1' in item else "",
            'supplier_name': 'Brisban Moss',
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
    brisbane_main()