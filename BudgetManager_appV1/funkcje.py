from datetime import datetime
from narzedzia import formatuj_date

def pobierz_miesiac():

    while True:
        try:
            miesiac = int(input("Podaj numer miesiąca (1-12): "))
# Obecnie sprawdzany jest tylko zakres 1-31.
# Poprawna walidacja powinna uwzględniać wybrany miesiąc
# oraz rok (w tym lata przestępne).
            if 1 <= miesiac <= 12:
                return miesiac

            print("Miesiąc musi być od 1 do 12.")

        except ValueError:
            print("Nieprawidłowy numer miesiąca. Wprowadź liczbę od 1 do 12.")


def pobierz_rok():

    while True:
        try:
            rok = int(input("Podaj rok(0 = powrót): "))

            if rok == 0:
                return None

            return rok

            

        except ValueError:
            print("Rok musi być liczbą całkowitą.")


def pobierz_dzien():

    while True:
        try:
            dzien = int(input("Podaj dzień (1-31): "))

            if 1 <= dzien <= 31:
                return dzien

            print("Dzień musi być od 1 do 31.")

        except ValueError:
            print("Nieprawidłowy dzień. Wprowadź liczbę od 1 do 31.")

def pobierz_rodzaj_paliwa():

    while True:
        print("1. PB95")
        print("2. PB98")
        print("3. ON")
        print("4. LPG")

        wybor = input("Wybierz rodzaj paliwa (1-4): ")

        if wybor == "1":
            return "PB95"
        elif wybor == "2":
            return "PB98"
        elif wybor == "3":
            return "ON"
        elif wybor == "4":
            return "LPG"

        print("Nieprawidłowy wybór. Wybierz liczbę od 1 do 4.")

def pobierz_nazwe(komunikat):

    while True:
        sklep = input(komunikat).strip().capitalize()

        sklep = " ".join(sklep.split())
    
        if len(sklep) > 25:
            print("Nazwa sklepu nie może być dłuższa niż 25 znaków.")
            continue
    
        if sklep == "":
            print("Nazwa sklepu nie może być pusta.")
            continue




        return sklep



def pobierz_kwote():

    while True:
        try:
            kwota = input("Podaj kwotę: ")
            kwota = kwota.replace(",", ".")
            kwota = float(kwota)

            if kwota <= 0:
                print("Kwota musi być większa od zera.")
                continue

            return kwota
        except ValueError:
            print("Nieprawidłowa kwota. Wprowadź liczbę.")


def licznik_wydatkow(wydatki):
    licznik = 0
    for wydatek in wydatki:
        licznik +=1
    return licznik

def utworz_wydatki(kategoria, nazwa, dzien, kwota, rodzaj_paliwa=None):
    return{
        "data_czas": formatuj_date(datetime.now()),
        "dzień": dzien,
        "kategoria": kategoria,
        "nazwa": nazwa,
        "kwota": kwota,
        "rodzaj_paliwa": rodzaj_paliwa
    }


from datetime import datetime

def pobierz_dzien_tygodnia():

    dni_tygodnia = {
        "Monday": "Poniedziałek",
        "Tuesday": "Wtorek",
        "Wednesday": "Środa",
        "Thursday": "Czwartek",
        "Friday": "Piątek",
        "Saturday": "Sobota",
        "Sunday": "Niedziela"
    }

    dzien = datetime.now().strftime("%A")

    return dni_tygodnia[dzien]
