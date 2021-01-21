import requests
import pyMsql
import pyScrapLora
import json

loro_list = []
def Lora_main():

    with open("loro_piana.json", "r", encoding="latin1") as f:
        loro_list = json.load(f)
    for loro in loro_list:
        pyMsql.save_scabal(loro)
    print(len(loro_list))
    return

if __name__ == '__main__':
    Lora_main()