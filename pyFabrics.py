import requests

URL = "https://fabrics.scabal.com/en/api/external/extractfabrics.json"
"""
(price range)
Potential returned values:

"""
zprice_range = {
    "x": "cheapest",
    "xx": "cheap",
    "xxx": "normal",
    "xxxx": "expensive",
    "xxxxx": "most expensive",
}

"""
(weight category per meter)
    Potential returned values:

    wc1=light // <260gr
    wc2=medium // 260gr - 320gr
    wc3=heavy // >320gr
"""
zweight_cat = {
    "wc1": "light",
    "wc2": "medium",
    "wc3": " heavy"
}

"""
	(color group)
Potential returned values:

cg1 // black
cg2 // black & white
cg3 // blue
cg4 // brown
cg5 // grey
cg6 // white
cg9 // other

"""
zcolor_group = {
    "cg1": "black",
    "cg2": "black & white",
    "cg3": "blue",
    "cg4": "brown",
    "cg5": "grey",
    "cg6": "white",
    "cg9": "other"
}

"""
(weaving method)
Potential returned values:

we1 // barathea
we2 // birdseye
we3 // cavalry twill
we4 // corduroy
we5 // gabardine
we6 // herringbone
we7 // hopsack
we8 // jacquard
we9 // plain weave
we10 // prunella
we11 // semi-plain
we12 // sharkskin
we13 // 2/2 twill
we14 // velvet
we15 // whipcord
we16 // faille
we17 // venetian 
we18 // chenille
we19 // satin
we20 // bell hopsack
we21 // rib weave
we22 // 3/1 twill

"""

zweave = {
    "we1": "barathea",
    "we2": "birdseye",
    "we3": "cavalry twill",
    "we4": "corduroy",
    "we5": "gabardine",
    "we6": "herringbone",
    "we7": "hopsack",
    "we8": "jacquard",
    "we9": "plain weave",
    "we10": "prunella",
    "we11": "semi-plain",
    "we12": "sharkskin",
    "we13": "2/2 twill",
    "we14": "velvet",
    "we15": "whipcord",
    "we16": "faille",
    "we17": "venetian",
    "we18": "chenille",
    "we19": "satin",
    "we20": "bell hopsack",
    "we21": "rib weave",
    "we22": "3/1 twill"
}

"""
(design)
Potential returned values:
de1 // check
de2 // glencheck
de3 // houndstooth
de4 // motif
de5 // pick & pick
de6 // pinhead
de7 // prince of wales
de8 // stripe
de9 // plain design
de10 // hairlline
"""

zdesign = {
    "de1": "check",
    "de2": "glencheck",
    "de3": "houndstooth",
    "de4": "motif",
    "de5": "pick & pick",
    "de6": "pinhead",
    "de7": "prince of wales",
    "de8": "stripe",
    "de9": "plain design",
    "de10": "hairlline"
}

"""
(exact color group)
Potential returned values:

ec1 // dark
ec2 // medium
ec3 // light
ec4 // green
ec5 // lilac
ec6 // orange
ec7 // red
ec8 // tartan
ec9 // yellow
ec10 // purple
ec11 // pink
"""

zexact_col = {
    "ec1": "dark",
    "ec2": "medium",
    "ec3": "light",
    "ec4": "green",
    "ec5": "lilac",
    "ec6": "orange",
    "ec7": "red",
    "ec8": "tartan",
    "ec9": "yellow",
    "ec10": "purple",
    "ec11": "pink",
}


def get_all_fabric_info():
    querystring = {
        "fabric": "all"
    }
    try:
        r = requests.request("GET", URL, params=querystring)
        r.raise_for_status()
        if (r.status_code != requests.codes.ok):
            return "{0}: {1}".format(r.status_code, r.text)
        else:
            return r.json()
    except Exception as e:
        return {}
    return


def get_fabric_info_by_id(id):
    querystring = {
        "fabric": id
    }
    try:
        r = requests.request("GET", URL, params=querystring)
        r.raise_for_status()
        if (r.status_code != requests.codes.ok):
            return "{0}: {1}".format(r.status_code, r.text)
        else:
            return r.json()
    except Exception as e:
        return {}


def get_fabric_data_detail(fabric_api_data):
    return {
        "cloth_pattern_number": int(fabric_api_data['matnr']),
        "cloth_bunch": fabric_api_data['maktx'],
        "colour": fabric_api_data['zcolor_txt'].upper() + " " + fabric_api_data['zexact_col_txt'].upper(),
        "composition_1": str(fabric_api_data['zcomp_1_perc']) + " " +  fabric_api_data['zcomponent_1'] if fabric_api_data['zcomp_1_perc'] != 0 else "",
        "composition_2": str(fabric_api_data['zcomp_2_perc']) + " " +  fabric_api_data['zcomponent_2'] if fabric_api_data['zcomp_2_perc'] !=0 else "",
        "design": fabric_api_data['zdesign_txt'].upper(),
        "width": fabric_api_data['zwidth'],
        "weight_ozs": fabric_api_data['ntgew'],
        "weight_gms": fabric_api_data['ntgew'],
        "weave": fabric_api_data['zweave_txt'].upper(),
        "dye": fabric_api_data['zdye'],
        "selvedge": fabric_api_data['zlisiere_txt']
    }
