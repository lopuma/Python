import csv

datos= '/home/esy9d7l1/Alvaro/ISSUES/CIRAST/Extraccion/OS_AUTOMATIZACION/OS.csv'

with open(datos, newline='', encoding='utf-8') as f:
    os = csv.DictReader(f)

    for r in os:
        print(r['INSTRUCTIONS'])