import pyMsql
import gsheet
import json
import re


def get_bunch_number_price(cloth_pattern_number):
    cpn = int(cloth_pattern_number)
    if cpn in range(207001, 207034):
        return float(700)
    if cpn in range(140005, 143622):
        return float(128)
    if cpn in range(146005, 146109):
        return float(71.20)
    if cpn in range(191002, 191005):
        return float(156.00)
    if cpn in range(197217, 197362) or cpn in range(209201, 209243) or cpn in range(518201, 518204) or cpn in range(518401,518405) or cpn in range(518605, 518607) \
        or cpn in range(204004, 204009) or cpn in range(992001,992005) or cpn in range(993101,993104) or cpn in range(993201, 993202) or \
        cpn in range(841001, 841069):
        return float(96.00)
    if cpn in range(518901, 518913):
        return float(112.00)
    if cpn in range(313001,313079 ) or cpn in range(321001, 321033):
        return float(52.80)
    if cpn in range(175002,175014 ):
        return float(668.80)
    if cpn in range(833003, 833107) or cpn in range(836018, 836125) or cpn in range(417501, 417541) or cpn in range(835012, 835100) or cpn in range(836006, 836013):
        return float(88.00)
    if cpn in range(417100, 417108) or cpn in range(417301, 417321):
        return float(92.00)
    if cpn in range(862601, 862606):
        return float(76.00)
    if cpn in range(881001, 881023):
        return float(97.00)
    if cpn in range(885101, 885106) or cpn in range(885401,885413 ) or cpn in range(462224,462228 ):
        return float(69.60)
    if cpn in range(307103, 307185) or cpn in range(407017,407097 ) or cpn in range(460001,460023 ) or cpn in range(758301,758304 ) or cpn in range(837301,837308 ) or cpn in range(981300,981399) or \
        cpn in range(441001, 441050) or cpn in range(417401, 417426) or cpn in range(417435, 417466) :
        return float(84.00)
    if cpn in range(409001, 409009) or cpn in range(409101, 409116) or cpn in range(419204, 419207):
        return float(104.00)
    if cpn in range(470201, 470203) or cpn in range(771501, 771508):
        return float(188.00)
    if cpn in range(475001, 475003) or cpn in range(994120, 994126):
        return float(140.00)
    if cpn in range(796001, 796006):
        return float(368)
    if cpn in range(994501, 994504) or cpn in range(994801, 994805) or cpn in range(995069, 995071):
        return float(300.00)
    if cpn in range(779301, 779350) or cpn in range(879889, 880105):
        return float(100.00)
    if cpn in range(300001, 300788) or cpn in range(301219, 301643):
        return float(72.00)
    if cpn in range(993019, 993068):
        return float(68.00)
    if cpn in range(518529, 518553) or cpn in range(896701, 896706):
        return float(116.00)
    if cpn in range(895200, 895208):
        return float(176.00)
    if cpn in range(843001, 843412) or cpn in range(844001, 844008):
        return float(124.00)
    if cpn in range(897030,897031):
        return float(120.00)
    if cpn in range(418001,418002):
        return float(316.00)
    if cpn in range(418251, 418253) or cpn in range(995600, 995602):
        return float(296.00)
    if cpn in range(793001, 793003) or cpn in range(798008, 798017):
        return float(254.00)
    if cpn in range(793101, 793102) or cpn in range(795001, 795017) or cpn in range(795020, 795042) or cpn in range(795114, 795212):
        return float(276.00)
    if cpn in range(200101,200116):
        return float(400.00)
    if cpn in range(841001,841069):
        return float(96.00)
    if cpn in range(791001,791027) or cpn in range(180001,180508) or cpn in range(180520,180522) or cpn in range(180527,180577):
        return float(260.00)
    if cpn in range(303044,303451):
        return float(78.40)
    if cpn in range(899343, 899362) or cpn in range(899470, 899483):
        return float(24.00)
    return float(0.0)
def check_exist_in_list(org_list, item):

    for org in org_list:
        if org['cloth_pattern_number'] == item['cloth_pattern_number']:
            return org
    return {}

def dormeuil_main():
    org_dormeuil_list = gsheet.parse_from_google_for_dormeuil()
    new_list =  []
    with open("dormeuil_data.json", "r", encoding="latin1") as f:
        new_list = json.load(f)

    # for org in org_dormeuil_list:
    #     try:
    #         pyMsql.save_scabal(org)
    #     except Exception as e:
    #         print("error in =>", org['cloth_pattern_number'])

    for new_item in new_list:
        if len(check_exist_in_list(org_dormeuil_list, new_item)) == 0:
            write_data = {
                'cloth_pattern_number': new_item['cloth_pattern_number'],
                'image_url': new_item['image_url'],
                'composition_1': str(new_item['composition_1']).upper(),
                'weight_ozs': new_item['weight'],
                'cloth_bunch': new_item['bunch'],
                'supplier_name':'Dormeuil',
                'price_per_meter': get_bunch_number_price(new_item['cloth_pattern_number']),
                'design':'',
                'width':''
            }
            try:
                pyMsql.save_scabal(write_data)
            except Exception as e:
                print("error in =>", new_item['cloth_pattern_number'])

if __name__ == '__main__':
    dormeuil_main()

