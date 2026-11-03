
from datetime import datetime
from funkcje import utworz_wydatki


from funkcje import (
    pobierz_dzien,
    pobierz_miesiac,
    pobierz_rok,
    pobierz_rodzaj_paliwa,
    pobierz_nazwe,
    pobierz_kwote,
    licznik_wydatkow,
    pobierz_dzien_tygodnia
)

from json_manager import (
    zapis_json,
    odczytaj_json
)

from narzedzia import formatuj_date

from statystyki import policz_sume_wydatkow_kategori

usuniety = None
suma_sesji = 0
suma_usunieta = 0
usuniete_wpisy = []





nazwa_aplikacji = "Budget Manager"

teraz = datetime.now()

print("Aplikacja uruchomiona:", formatuj_date(teraz))

wydatki = odczytaj_json()

while True:

    teraz = datetime.now()

  

    
    data = teraz.strftime("%Y-%m-%d")
    godzina = teraz.strftime("%H:%M:%S")

    dzisiaj = pobierz_dzien_tygodnia()

    print(f"Data: {data}")
    print(f"Godzina: {godzina}")
    print(f"Dzień: {dzisiaj}")

    print("\n=== " + nazwa_aplikacji + " ===")
    print("1. Dodaj wydatek")
    print("2. Pokaż historię wydatków")
    print("3. Statystyki wydatków")
    print("4. Cofnij ostatnie wpisy")
    print("5. Wyjdź")

    wybor = input("Wybierz opcję: ")

    if wybor == "1":
        
        print("\nJakie wydatki?")
        print("1. Zakupy")
        print("2. Paliwo")
        print("3. Inne")
        print("4. Powrót")

        typ_wydatku = input("Wybierz liczbę od 1 do 3: ")

        if typ_wydatku == "1":
            
            

            
            print("\nWybrano zakupy")
            sklep = pobierz_nazwe("Podaj nazwę sklepu: ")

            kwota_zakupow = pobierz_kwote()

            
            
            suma_sesji += kwota_zakupow
           
                
           

            pozycja = utworz_wydatki(
                "Zakupy",
                sklep,
                dzisiaj,
                kwota_zakupow
                )

            wydatki.append(pozycja)
            zapis_json(wydatki)

            print("\nPodsumowanie:")
            print(f"Sklep: {sklep}")
            print(f"Kwota: {kwota_zakupow:.2f} zł")

        elif typ_wydatku == "2":
            print("\nWybrano paliwo")

            stacja = pobierz_nazwe("Podaj nazwę stacji paliw: ")
            rodzaj_paliwa = pobierz_rodzaj_paliwa()
            kwota_paliwa = pobierz_kwote()

            
            suma_sesji += kwota_paliwa

            pozycja = utworz_wydatki(
                "Paliwo",
                stacja,
                dzisiaj,
                kwota_paliwa,
                rodzaj_paliwa
            )

            wydatki.append(pozycja)
            zapis_json(wydatki)
            
         

            print("\nPodsumowanie:")
            print(f"Stacja: {stacja}")
            print(f"Kwota paliwa: {kwota_paliwa:.2f} zł")
            print(f"Rodzaj paliwa: {rodzaj_paliwa}")

        elif typ_wydatku == "3":
            print("\nWybrano Inne")
            inne = pobierz_nazwe("Podaj nazwę innego wydatku: ")
            kwota_inne = pobierz_kwote()

            suma_sesji += kwota_inne

            pozycja = utworz_wydatki(
                "Inne",
                inne,
                dzisiaj,
                kwota_inne
            )
            wydatki.append(pozycja)
            zapis_json(wydatki)

            print("\nPodsumowanie:")
            print(f"Inne: {inne}")
            print(f"Kwota: {kwota_inne:.2f} zł")

        elif typ_wydatku == "4":
            print("\nPowrót do głównego menu")
            continue

        else:
            print("Nieprawidłowy wybór kategorii.")

    elif wybor == "2":
        
        
        for wydatek in wydatki:
            print(f"\nData i czas: {wydatek['data_czas']}")
            print(f"Dzień: {wydatek['dzień']}")
            print(f"Kategoria: {wydatek['kategoria']}")
            print(f"Nazwa: {wydatek['nazwa']}")
            print(f"Kwota: {wydatek['kwota']:.2f} zł")

            if wydatek["kategoria"] == "Paliwo":

                print(
                    f"Rodzaj paliwa: " 
                    f"{wydatek.get('rodzaj_paliwa', 'Brak danych')}"
                )




        suma_wydatkow = policz_sume_wydatkow_kategori(wydatki)
        liczba_wydatkow = licznik_wydatkow(wydatki)
        print(f"\nŁączna kwota wydatków: {suma_wydatkow:.2f} zł")
        print(f"Liczba wydatków: {liczba_wydatkow}")


    elif wybor == "3":


        

        print("\n=== Statystyki ===")
        print("1. Wszystkie statystyki")
        print("2. Statystyki miesiąca")
        print("3. Statystyki dnia")
        print("4. Powrót")

        wybor_statystyki = input("Wybierz opcję od 1 do 4 : ")

        if wybor_statystyki == "1":
            print("\nStatystyki wszystkich wydatków:")

            suma_zakupy = policz_sume_wydatkow_kategori(wydatki, "Zakupy")
            suma_paliwo = policz_sume_wydatkow_kategori(wydatki, "Paliwo")
            suma_inne = policz_sume_wydatkow_kategori(wydatki, "Inne")
            suma_razem = policz_sume_wydatkow_kategori(wydatki) 
            liczba_wydatkow = licznik_wydatkow(wydatki)
            print(f"Liczba wydatków: {liczba_wydatkow}")
            


        elif wybor_statystyki == "2":
            print("\nStatystyki wydatków w tym miesiącu:")

            podaj_rok = pobierz_rok()
            if podaj_rok is None:
                continue
            miesiac = pobierz_miesiac()
            szukamy_miesiaca = f"{podaj_rok}-{str(miesiac).zfill(2)}"
            
         
            print(f"Statystki z : {szukamy_miesiaca}")


            wydatki_miesiaca = []

            for wydatek in wydatki:
                if wydatek["data_czas"].startswith(szukamy_miesiaca):
                    wydatki_miesiaca.append(wydatek)


                    print(
                        f"{wydatek['data_czas']} | "
                        f"{wydatek['kategoria']} | "
                        f"{wydatek['nazwa']} | "
                        f"{wydatek['kwota']:.2f} zł"
                        
                    ) 
                    
          
            suma_zakupy = policz_sume_wydatkow_kategori(wydatki_miesiaca, "Zakupy")
            suma_paliwo = policz_sume_wydatkow_kategori(wydatki_miesiaca, "Paliwo")
            suma_inne = policz_sume_wydatkow_kategori(wydatki_miesiaca, "Inne")
            suma_razem = policz_sume_wydatkow_kategori(wydatki_miesiaca)
            liczba_wydatkow = licznik_wydatkow(wydatki_miesiaca)
            print(f"Liczba wydatków w miesiącu: {liczba_wydatkow}")
        
        elif wybor_statystyki == "3":
            print("\nStatystyki wydatków w tym dniu:")

            podaj_rok = pobierz_rok()
            if podaj_rok is None:
                continue
            podaj_miesiac = pobierz_miesiac()
            podaj_dzien = pobierz_dzien()
            dzien_szukany = f"{podaj_rok}-{str(podaj_miesiac).zfill(2)}-{str(podaj_dzien).zfill(2)}"



            wydatki_dnia = []


            for wydatek in wydatki:
                if wydatek["data_czas"].startswith(dzien_szukany):
                    wydatki_dnia.append(wydatek)

                    print(
                        f"{wydatek['data_czas']} | "
                        f"{wydatek['kategoria']} | "
                        f"{wydatek['nazwa']} | "
                        f"{wydatek['kwota']:.2f} zł"
                    )
                    
            suma_zakupy = policz_sume_wydatkow_kategori(wydatki_dnia, "Zakupy")
            suma_paliwo = policz_sume_wydatkow_kategori(wydatki_dnia, "Paliwo")
            suma_inne = policz_sume_wydatkow_kategori(wydatki_dnia, "Inne")
            suma_razem = policz_sume_wydatkow_kategori(wydatki_dnia)
            liczba_wydatkow = licznik_wydatkow(wydatki_dnia)
            print(f"Liczba wydatków w dniu: {liczba_wydatkow}")
               
        elif wybor_statystyki == "4":
            continue
            

       
        
       
      
        print(
            f"Zakupy: {suma_zakupy:.2f} zł, "
            f"Paliwo: {suma_paliwo:.2f} zł, "
            f"Inne: {suma_inne:.2f} zł" 

            f"\nŁączna kwota wydatków: {suma_razem:.2f} zł"
        )
       


    elif wybor == "4":
    
        print("0. Powrót")
        if not wydatki:
            print("Nie masz żadnych wpisów")
            continue

        print("10 ostatnich wpisów:") 

        ostatnie_wpisy = wydatki[-10:]

        for i, wydatek in enumerate(ostatnie_wpisy, start=1):
            print(
                f"{i}. "
                f"{wydatek['data_czas']} | "
                f"{wydatek['nazwa']} | "
                f"{wydatek['kwota']:.2f} zł"


            )
        try:
            numer = int(input("Który wpis cofnąć? "))

            if numer == 0:
                continue
            if 1<= numer <= len(ostatnie_wpisy):
                print(f"Wybrano numer: {numer}")
            else:
                print("Nieprawidłowy numer.")
                continue
        except ValueError:
            print("Podaj liczbę.")
            continue


        indeks = len(wydatki) - len(ostatnie_wpisy) + numer - 1

        usuniety = wydatki.pop(indeks)
        usuniete_wpisy.append(usuniety)
        suma_usunieta += usuniety["kwota"]
        suma_sesji -= usuniety['kwota']
        zapis_json(wydatki)

        print(
            f"Cofnięto wpis: "
            f"{usuniety['nazwa']} | "
            f"{usuniety['kwota']:.2f} zł"
        )
       
        zapis_json(wydatki)

    

    elif wybor == "5":
        print("\nZamykam aplikację...")
        if usuniete_wpisy:
            print("\nUsunięte wpisy:")

            for wpis in usuniete_wpisy:
                print(
                    f"{wpis['kategoria']} | "
                    f"{wpis['nazwa']} | "
                    f"{wpis['kwota']:.2f} zł"
                )
      
        if suma_sesji > 0:
             print(
                f"\nW tej sesji dodano wydatki na kwotę: "
                f"{suma_sesji:.2f} zł"
            )

        if suma_usunieta > 0:
            print(
                f"W tej sesji usunięto wydatki na kwotę: "
                
                f"{suma_usunieta:.2f} zł"
            )
        
        
        
        
            

        

        zapis_json(wydatki)

        print("Do zobaczenia!")


        break
    
    
    
    else:

        print("Nieprawidłowy wybór.")



