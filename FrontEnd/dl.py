import os, csv, json
from dicttoxml import dicttoxml

data = {"Elem1": "Val1", "Elem2": "Val2", "Elem3": "Val3"}
path = r"D:\Projects\-MISS1-Crack-Detection\FrontEnd"


def csv_dl(data, path):
    with open(os.path.join(path, 'csv_data.csv'), 'w') as f:
        w = csv.DictWriter(f, data.keys())
        w.writeheader()
        w.writerow(data)


def xml_dl(data, path):
    xml_data = dicttoxml(data).decode('utf8')
    with open(os.path.join(path, 'xml_data.xml'), 'w') as f:
        f.write(xml_data)


def json_dl(data, path):
    json_data = json.dumps(data)
    with open(os.path.join(path, 'json_data.json'), 'w') as f:
        f.write(json_data)


# csv_dl(data, path)
# xml_dl(data, path)
# json_dl(data, path)
