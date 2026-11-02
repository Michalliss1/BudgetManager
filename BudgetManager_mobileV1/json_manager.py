import json
def zapis_json(wydatki):

    with open("wydatki.json", "w", encoding="utf-8") as plik:

        json.dump(wydatki , plik, ensure_ascii=False, indent=4)

def odczytaj_json():
    try:
        with open("wydatki.json", "r", encoding="utf-8") as plik:
            return json.load(plik)
    except FileNotFoundError:
        return []