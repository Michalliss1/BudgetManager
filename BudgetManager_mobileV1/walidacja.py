def waliduj_nazwe(nazwa):

    nazwa = nazwa.strip().capitalize()
    nazwa = " ".join(nazwa.split())

    if len(nazwa) > 25:
        return None

    if nazwa == "":
        return None

    return nazwa


def waliduj_kwote(kwota):

    try:
        kwota = kwota.replace(",", ".")
        kwota = float(kwota)

        if kwota <= 0:
            return None

        return kwota

    except ValueError:
        return None

def waliduj_rodzaj_paliwa(rodzaj):
    dozwolone = ["PB95", "PB98", "ON", "LPG","EV"]

    if rodzaj in dozwolone:
        return rodzaj

    return None


def waliduj_miesiac(tekst):

    
    try:
        miesiac = int(tekst)

        if 1 <= miesiac <= 12:
            return miesiac

        return None

    except ValueError:
        return None


def waliduj_rok(tekst):

   
    try:
        rok = int(tekst)

        if rok < 2026:
            return None

        return rok

        

    except ValueError:
        return None

def waliduj_dzien(tekst):

   
    try:
        dzien = int(tekst)

        if dzien < 1 or dzien > 31:
            return None

        return dzien

        

    except ValueError:
        return None



