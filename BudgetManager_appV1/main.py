
from kivy.config import Config

Config.set("graphics", "width", "412")
Config.set("graphics", "height", "915")


from json_manager import odczytaj_json, zapis_json
from walidacja import waliduj_nazwe, waliduj_kwote, waliduj_rodzaj_paliwa, waliduj_miesiac, waliduj_rok, waliduj_dzien
from funkcje import utworz_wydatki,pobierz_dzien_tygodnia


from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
import uuid



class BudgetApp(App):

    def build(self):
        self.title = "BM"
        self.icon = "icons/logo.png"

        self.wydatki = odczytaj_json()
        self.suma_sesji = 0
        self.id_sesji = str(uuid.uuid4())
        self.usuniety = []
        self.rodzaj_paliwa = None
    
        self.layout = FloatLayout()

        with self.layout.canvas.before:
            Color(0.035, 0.035, 0.045, 1)
            self.rect = Rectangle(
                size=self.layout.size,
                pos=self.layout.pos
            )

        self.layout.bind(
            size=self.update_rect,
            pos=self.update_rect
        )

        # Ekran powitalny
        self.logo = Image(
            source="icons/logo.png",
            size_hint=(1.2, 1.2),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            opacity=0
        )

        self.nazwa = Label(
            text="Personal Finance Manager",
            font_size="25sp",
            color=(1, 1, 1, 1),
            opacity=0,
            pos_hint={"center_x": 0.5, "center_y": 0.43}
        )

        self.prawa = Label(
            text=(
                "Copyright © 2026 Michał Lissowski\n"
                "Wszystkie prawa zastrzeżone\n"
                "All Rights Reserved"
            ),
            font_size="13sp",
            color=(0.7, 0.7, 0.75, 1),
            opacity=0,
            pos_hint={"center_x": 0.5, "center_y": 0.23}
        )

        self.layout.add_widget(self.logo)
        self.layout.add_widget(self.nazwa)
        self.layout.add_widget(self.prawa)

        Animation(opacity=1, duration=2).start(self.logo)

        Animation(
            size_hint=(0.35, 0.35),
            pos_hint={"center_x": 0.5, "center_y": 0.7},
            duration=3
        ).start(self.logo)

        Clock.schedule_once(self.pokaz_nazwe, 1.5)
        Clock.schedule_once(self.pokaz_menu, 5)

        return self.layout

    def pokaz_nazwe(self, dt):
        Animation(opacity=1, duration=1.5).start(self.nazwa)
        Animation(opacity=1, duration=1.5).start(self.prawa)

    def stworz_przycisk(self, tekst):
        btn = Button(
            text=tekst,
            font_size="18sp",
            color=(0.95, 0.96, 1, 1),
            background_normal="",
            background_down="",
            background_color=(0.13, 0.15, 0.20, 1),
            size_hint_y=1
        )

        # Zaokrąglone tło
        with btn.canvas.before:
            btn.bg_color = Color(0.13, 0.15, 0.20, 1)
            btn.bg = RoundedRectangle(
                pos=btn.pos,
                size=btn.size,
                radius=[dp(12)]
            )

        def aktualizuj_tlo(widget, value):
            btn.bg.pos = widget.pos
            btn.bg.size = widget.size

        btn.bind(pos=aktualizuj_tlo, size=aktualizuj_tlo)

        # Efekt podświetlenia po kliknięciu
        def klikniecie(widget):
            Animation(
                background_color=(0.18, 0.28, 0.42, 1),
                duration=0.12
            ).start(widget)

        def puszczenie(widget):
            Animation(
                background_color=(0.13, 0.15, 0.20, 1),
                duration=0.18
            ).start(widget)

        btn.bind(on_press=klikniecie, on_release=puszczenie)

        return btn

    def pokaz_menu(self, dt):
        self.layout.clear_widgets()

 
        menu = BoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            height=dp(540),
            pos_hint={"center_x": 0.5, "top": 0.8},
            padding=[dp(15), dp(10), dp(15), dp(10)],
            spacing=dp(5)
        )

        naglowek = Label(
            text="Panel główny",
            font_size="28sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=dp(65)
        )

        menu.add_widget(naglowek)

        # PIERWSZY RZĄD: Dodaj wydatek i Cofnij wpis
        rzad1 = GridLayout(
            cols=2,
            spacing=dp(10),
            size_hint_y=None,
            height=dp(170)
        )

        dodaj_layout = FloatLayout()

        ikona_dodaj = Image(
            source="icons/dodajwydatek.png",
            fit_mode="contain",
            size_hint=(1.05,1.05),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        btn_dodaj = Button(
            text="",
                size_hint=(0.55, 0.9),
                pos_hint={
                    "center_x": 0.5,
                    "center_y": 0.5
                },
                background_normal="",
                background_down="",
                background_color=(0, 0, 0, 0)

        )

        napis_dodaj = Label(
            text="Dodaj wydatek",
            font_size="18sp",
            bold=True,
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.15}
        )


        dodaj_layout.add_widget(ikona_dodaj)
        dodaj_layout.add_widget(napis_dodaj)
        dodaj_layout.add_widget(btn_dodaj)

        def dodaj_press(instance):
            Animation(
                pos_hint={"center_x": 0.5, "center_y": 0.47},
                duration=0.05
            ).start(ikona_dodaj)

        def dodaj_release(instance):
            Animation(
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                duration=0.05
            ).start(ikona_dodaj)

        btn_dodaj.bind(on_press=dodaj_press)
        btn_dodaj.bind(on_release=dodaj_release)
        btn_dodaj.bind(on_press=self.pokaz_dodawanie)

        cofnij_layout = FloatLayout()

        btn_cofnij = Button(
            text="",
            size_hint=(0.55, 0.9),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.5
            },
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0)
        )

        napis_cofnij = Label(
            text="Cofnij wpis",
            font_size="18sp",
            bold=True,
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.15}
        )

        ikona_cofnij = Image(
            source="icons/back.jpg",
            fit_mode="contain",
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        
        cofnij_layout.add_widget(ikona_cofnij)
        cofnij_layout.add_widget(napis_cofnij)
        cofnij_layout.add_widget(btn_cofnij)
        btn_cofnij.bind(
                on_press=self.cofnij_wybor
            )
        

        def cofnij_press(instance):
            Animation(
                pos_hint={"center_x": 0.5, "center_y": 0.47},
                duration=0.05
            ).start(ikona_cofnij)

        def cofnij_release(instance):
            Animation(
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                duration=0.05
            ).start(ikona_cofnij)

        btn_cofnij.bind(on_press=cofnij_press)
        btn_cofnij.bind(on_release=cofnij_release)

        rzad1.add_widget(dodaj_layout)
        rzad1.add_widget(cofnij_layout)
        # DRUGI RZĄD: Historia i Statystyki
        rzad2 = GridLayout(
            cols=2,
            spacing=dp(10),
            size_hint_y=None,
            height=dp(170)
        )

        historia_layout = FloatLayout()

        btn_historia = Button(
             text="",
                size_hint=(0.55, 0.9),
                pos_hint={
                    "center_x": 0.5,
                    "center_y": 0.5
                },
                background_normal="",
                background_down="",
                background_color=(0, 0, 0, 0)
        )

        napis_historia = Label(
            text="Historia",
            font_size="18sp",
            bold=True,
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.15}
        )

        ikona_historia = Image(
            source="icons/historia.jpg",
            fit_mode="contain",
            size_hint=(0.96, 0.96),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )


        historia_layout.add_widget(ikona_historia)
        historia_layout.add_widget(napis_historia)
        historia_layout.add_widget(btn_historia)

        def historia_press(instance):
            Animation(
                pos_hint={"center_x": 0.5, "center_y": 0.47},
                duration=0.05
            ).start(ikona_historia)

        def historia_release(instance):
            Animation(
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                duration=0.05
            ).start(ikona_historia)

        btn_historia.bind(on_press=historia_press)
        btn_historia.bind(on_release=historia_release)
        btn_historia.bind(
            on_press=self.pokaz_historie
        )

        statystyki_layout = FloatLayout()


        btn_statystyki = Button(
             text="",
                size_hint=(0.55, 0.9),
                pos_hint={
                    "center_x": 0.5,
                    "center_y": 0.5
                },
                background_normal="",
                background_down="",
                background_color=(0, 0, 0, 0)
        )

        napis_statystyki = Label(
            text="Statystyki",
            font_size="18sp",
            bold=True,
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.15}
        )

        ikona_statystyki = Image(
            source="icons/statystyki.jpg",
            fit_mode="contain",
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )


        statystyki_layout.add_widget(ikona_statystyki)
        statystyki_layout.add_widget(napis_statystyki)
        statystyki_layout.add_widget(btn_statystyki)

        def statystyki_press(instance):
            Animation(
                pos_hint={"center_x": 0.5, "center_y": 0.47},
                duration=0.05
            ).start(ikona_statystyki)

        def statystyki_release(instance):
            Animation(
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                duration=0.05
            ).start(ikona_statystyki)

        btn_statystyki.bind(on_press=statystyki_press)
        btn_statystyki.bind(on_release=statystyki_release)

        btn_statystyki.bind(
            on_press=self.pokaz_statystyki
        )


        rzad2.add_widget(historia_layout)
        rzad2.add_widget(statystyki_layout)

        # TRZECI RZĄD: Wyjście na środku
        wyjscie_layout = FloatLayout(
            size_hint_y=None,
            height=dp(170)
        )

        btn_wyjdz = Button(
             text="",
                size_hint=(0.28, 0.9),
                pos_hint={
                    "center_x": 0.5,
                    "center_y": 0.5
                },
                background_normal="",
                background_down="",
                background_color=(0, 0, 0, 0)
        )

        napis_wyjdz = Label(
            text="Wyjście",
            font_size="18sp",
            bold=True,
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.15}
        )

        btn_wyjdz.bind(on_press=self.zamknij)

        ikona_wyjscie = Image(
            source="icons/Wyjscie.jpg",
            fit_mode="contain",
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        wyjscie_layout.add_widget(ikona_wyjscie)
        wyjscie_layout.add_widget(napis_wyjdz)
        wyjscie_layout.add_widget(btn_wyjdz)

        def wyjscie_press(instance):
            Animation(
                pos_hint={"center_x": 0.5, "center_y": 0.47},
                duration=0.05
            ).start(ikona_wyjscie)

        def wyjscie_release(instance):
            Animation(
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                duration=0.05
            ).start(ikona_wyjscie)

        btn_wyjdz.bind(on_press=wyjscie_press)
        btn_wyjdz.bind(on_release=wyjscie_release)

        # Dodawanie trzech rzędów do menuS
        menu.add_widget(rzad1)
        menu.add_widget(rzad2)
        menu.add_widget(wyjscie_layout)

        self.layout.add_widget(menu)

    def pokaz_dodawanie(self, instance):

        self.layout.clear_widgets()

        ekran = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10
        )

        tytul = Label(
            text="Dodaj wydatek",
            font_size="22sp",
            color=(1, 1, 1, 1)
        )

        zakupy_layout = FloatLayout()

        ikona_zakupy = Image(
            source="icons/zakupy.png",
            fit_mode="contain",
            size_hint=(0.85, 0.85),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        btn_zakupy = Button(
            text="",
            size_hint=(0.15, 1),
            pos_hint={
                "center_x": 0.5,
                "y": 0
            },
            background_normal="",
            background_down="",
            background_color=(0,0,0,0)
        )
        

        napis_zakupy = Label(
            text="Zakupy",
            font_size="18sp",
            bold=True,
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.15}
        )

        zakupy_layout.add_widget(ikona_zakupy)
        zakupy_layout.add_widget(napis_zakupy)
        zakupy_layout.add_widget(btn_zakupy)

        btn_zakupy.bind(on_press=self.pokaz_zakupy)
        

        paliwo_layout = FloatLayout()

        ikona_paliwo = Image(
            source="icons/paliwo.png",
            fit_mode="contain",
            size_hint=(0.85, 0.85),
            pos_hint={"center_x":0.5,"center_y":0.5}
        )

        napis_paliwo = Label(
            text="Paliwo",
            font_size="18sp",
            bold=True,
            color=(1,1,1,1),
            pos_hint={"center_x":0.5,"center_y":0.15}
        )

        btn_paliwo = Button(
            text="",
            size_hint=(0.15, 1),
            pos_hint={
                "center_x": 0.5,
                "y": 0
            },
            background_normal="",
            background_down="",
            background_color=(0,0,0,0)
        )

        paliwo_layout.add_widget(ikona_paliwo)
        paliwo_layout.add_widget(napis_paliwo)
        paliwo_layout.add_widget(btn_paliwo)

        btn_paliwo.bind(
            on_press=self.pokaz_paliwo
        )
        
        inne_layout = FloatLayout()

        ikona_inne = Image(
            source="icons/inne.png",
            fit_mode="contain",
            size_hint=(0.85, 0.85),
            pos_hint={"center_x":0.5,"center_y":0.5}
        )

        napis_inne = Label(
            text="Inne",
            font_size="18sp",
            bold=True,
            color=(1,1,1,1),
            pos_hint={"center_x":0.5,"center_y":0.15}
        )

        btn_inne = Button(
        text="",
                size_hint=(0.15, 1),
                pos_hint={
                    "center_x": 0.5,
                    "y": 0
                },
                background_normal="",
                background_down="",
                background_color=(0,0,0,0)
            )

        inne_layout.add_widget(ikona_inne)
        inne_layout.add_widget(napis_inne)
        inne_layout.add_widget(btn_inne)
        btn_inne.bind(on_press=self.pokaz_inne)       

        powrot_layout = FloatLayout()

        ikona_powrot = Image(
            source="icons/wroc.png",
            fit_mode="contain",
            size_hint=(0.85, 0.85),
            pos_hint={"center_x":0.5,"center_y":0.5}
        )

        napis_powrot = Label(
            text="Powrót",
            font_size="18sp",
            bold=True,
            color=(1,1,1,1),
            pos_hint={"center_x":0.5,"center_y":0.15}
        )

        btn_powrot = Button(
        text="",
                size_hint=(0.15, 1),
                pos_hint={
                    "center_x": 0.5,
                    "y": 0
                },
                background_normal="",
                background_down="",
                background_color=(0,0,0,0)
            )

        powrot_layout.add_widget(ikona_powrot)
        powrot_layout.add_widget(napis_powrot)
        powrot_layout.add_widget(btn_powrot)

        btn_powrot.bind(
            on_press=lambda x: self.pokaz_menu(None)
        )
        
        
        
        

        
        ekran.add_widget(tytul)
        ekran.add_widget(zakupy_layout)
        ekran.add_widget(paliwo_layout)
        ekran.add_widget(inne_layout)
        ekran.add_widget(powrot_layout)


        

        self.layout.add_widget(ekran)


   
    def cofnij_wybor(self, instance):

        self.layout.clear_widgets()

        if not hasattr(self, "wpisy_do_cofniecia"):
            self.wpisy_do_cofniecia = self.wydatki[-10:].copy()

        ekran = BoxLayout(
            orientation="vertical",
            padding=[dp(15), dp(10), dp(15), dp(10)],
            spacing=dp(8)
        )

        tytul = Label(
            text="Cofnij wpis (10 ostatnich)",
            font_size="24sp",
            bold=True,
            size_hint_y=None,
            height=dp(60),
            halign="center",
            valign="middle"
        )

        ekran.add_widget(tytul)

        if not self.wydatki:
            ekran.add_widget(
                Label(
                    text="Brak wpisów do cofnięcia",
                    font_size="21sp"
                )
            )

        else:
            scroll = ScrollView(
                size_hint=(1, 1),
                do_scroll_x=False,
                bar_width=dp(5)
            )

            lista = BoxLayout(
                orientation="vertical",
                size_hint=(1, None),
                spacing=dp(12),
                padding=[dp(5), dp(5)]
            )

            lista.bind(minimum_height=lista.setter("height"))

            ostatnie_wpisy = [
                wpis
                for wpis in self.wpisy_do_cofniecia
                if wpis in self.wydatki
            ]

            for i, wydatek in enumerate(
                reversed(ostatnie_wpisy),
                start=1
            ):

                btn_klik = Button(
                    text=(
                        f"[b][color=ff9900]{i}.[/color][/b] "
                        f"[color=00ff00]{wydatek['data_czas']}[/color]\n"
                        f"{wydatek['kategoria']} | "
                        f"{wydatek['nazwa']} | "
                        f"{wydatek['kwota']:.2f} zł"
                    ),
                    markup=True,
                    font_size="19sp",
                    background_normal="",
                    background_down="",
                    background_color=(0, 0, 0, 0),
                    color=(1, 1, 1, 1),
                    halign="left",
                    valign="middle",
                    size_hint=(1, None),
                    height=dp(60)
                )

                btn_klik.bind(
                    width=lambda inst, w: setattr(
                        inst, "text_size", (w - dp(20), None)
                    )
                )

                def klikniecie(instance, wydatek=wydatek):
                    animacja = Animation(opacity=0.4, duration=0.3)
                    animacja.bind(
                        on_complete=lambda *args: self.usun_wpis(wydatek)
                    )
                    animacja.start(instance)

                btn_klik.bind(on_press=klikniecie)

                lista.add_widget(btn_klik)

            scroll.add_widget(lista)
            ekran.add_widget(scroll)

        # Przycisk powrotu
        powrot_layout = FloatLayout(
            size_hint_y=None,
            height=dp(110)
        )

        ikona_powrot = Image(
            source="icons/wroc.png",
            fit_mode="contain",
            size_hint=(0.65, 0.85),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.65
            }
        )

        napis_powrot = Label(
            text="Powrót",
            font_size="28sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.30),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.12
            }
        )

        btn_powrot = Button(
            text="",
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0)
        )

        btn_powrot.bind(
            on_press=lambda x: self.pokaz_menu(None)
        )

        powrot_layout.add_widget(ikona_powrot)
        powrot_layout.add_widget(napis_powrot)
        powrot_layout.add_widget(btn_powrot)

        ekran.add_widget(powrot_layout)

        self.layout.add_widget(ekran)

    def usun_wpis(self, wydatek):
        if wydatek not in self.wydatki:
            return

        self.usuniety.append(wydatek)
        self.usuniety = self.usuniety[-10:]
        if wydatek.get("sesja") == self.id_sesji:
            self.suma_sesji -= float(wydatek["kwota"])
        self.wydatki.remove(wydatek)

        if hasattr(self, "wpisy_do_cofniecia"):
            if wydatek in self.wpisy_do_cofniecia:
                self.wpisy_do_cofniecia.remove(wydatek)

        zapis_json(self.wydatki)
        self.cofnij_wybor(None)
      
    def pokaz_zakupy(self, instance):
        

        self.layout.clear_widgets()
        if not hasattr(self, "wpisy_do_cofniecia"):
            self.wpisy_do_cofniecia = self.wydatki[-10:].copy()

        ekran = BoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(6)
        )

        tytul = Label(
            text="Dodaj Zakupy",
            font_size="24sp",
            size_hint_y=None,
            height=dp(45)
        )
        
       


        self.input_sklep = TextInput(
            hint_text="Podaj nazwę sklepu:",
            size_hint_y=None,
            height=dp(80),
            font_size="22sp",
            padding=[dp(15), dp(22)],
            multiline=False
        )

        self.input_kwota = TextInput(
            hint_text="Podaj kwotę:",
            size_hint_y=None,
            height=dp(80),
            font_size="22sp",
            padding=[dp(15), dp(22)],
            multiline=False
        )

        self.info_label = Label(
            text="",
            color=(1, 0, 0, 1),
            font_size="20sp",
            size_hint_y=None,
            height=dp(30)
        )

        zapisz_layout = FloatLayout(
            size_hint_y=None,
            height=dp(150)
        )

        ikona_zapisz = Image(
            source="icons/zapis.png",
            fit_mode="contain",
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        napis_zapisz = Label(
            text="Zapisz",
            font_size="28sp",
            bold=True,
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.15}
        )

        btn_zapisz = Button(
            text="",
            size_hint=(1, 1),
            pos_hint={
                "center_x": 0.5,
                "y": 0
            },
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0)  # zielony testowo
        )

        zapisz_layout.add_widget(ikona_zapisz)
        zapisz_layout.add_widget(napis_zapisz)
        zapisz_layout.add_widget(btn_zapisz)


        powrot_layout = FloatLayout(
            size_hint_y=None,
            height=dp(150)
        )

        ikona_powrot = Image(
            source="icons/wroc.png",
            fit_mode="contain",
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        napis_powrot = Label(
            text="Powrót",
            font_size="28sp",
            bold=True,
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.15}
        )

        btn_powrot = Button(
            text="",
            size_hint=(1, 1),
            pos_hint={
                "center_x": 0.5,
                "y": 0
            },
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0)   # czerwony testowo
        )

        powrot_layout.add_widget(ikona_powrot)
        powrot_layout.add_widget(napis_powrot)
        powrot_layout.add_widget(btn_powrot)

        
        ekran.add_widget(tytul)
        
        ekran.add_widget(self.input_sklep)
        ekran.add_widget(self.input_kwota)
        ekran.add_widget(self.info_label)
        ekran.add_widget(zapisz_layout )
        ekran.add_widget(powrot_layout)
        

        self.layout.add_widget(ekran)

        btn_powrot.bind(
            on_press=lambda x: self.pokaz_dodawanie(None)
        )

        btn_zapisz.bind(
            on_press=self.zapisz_zakupy

        )

   
    def pokaz_paliwo(self, instance):

        self.layout.clear_widgets()

        ekran = BoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(6)
        )

        tytul = Label(
            text="Dodaj Paliwo",
            font_size="24sp",
            size_hint_y=None,
            height=dp(45)
        )

      

        self.input_stacja = TextInput(
            hint_text="Podaj nazwę Stacji Paliw:",
            size_hint_y=None,
            height=dp(80),
            font_size="22sp",
            padding=[dp(15), dp(22)],
            multiline=False
        )

        self.input_kwota = TextInput(
            hint_text="Podaj kwotę:",
            size_hint_y=None,
            height=dp(80),
            font_size="22sp",
            padding=[dp(15), dp(22)],
            multiline=False
        )

        self.info_label = Label(
            text="",
            color=(1, 0, 0, 1),
            font_size="20sp",
            size_hint_y=None,
            height=dp(30)
        )

        self.btn_pb95 = Button(
            text="PB95",
            size_hint=(1, None),
            height=dp(55),
            font_size="20sp",
            background_normal="",
            background_down="",
            background_color=(0.95, 0.55, 0.05, 1)
        )

        self.btn_pb98 = Button(
            text="PB98",
            size_hint=(1, None),
            height=dp(55),
            font_size="20sp",
            background_normal="",
            background_down="",
            background_color=(0.95, 0.55, 0.05, 1)
        )

        self.btn_on = Button(
            text="ON",
            size_hint=(1, None),
            height=dp(55),
            font_size="20sp",
            background_normal="",
            background_down="",
            background_color=(0.95, 0.55, 0.05, 1)
        )

        self.btn_lpg = Button(
            text="LPG",
            size_hint=(1, None),
            height=dp(55),
            font_size="20sp",
            background_normal="",
            background_down="",
            background_color=(0.95, 0.55, 0.05, 1)
        )

        self.btn_elektryk = Button(
            text="Elektryk",
            size_hint=(0.95, None),
            height=dp(60),
            font_size="20sp",
            pos_hint={"center_x": 0.5},
            background_normal="",
            background_down="",
            background_color=(0.95, 0.55, 0.05, 1)
        )

        self.btn_pb95.bind(
            on_press=lambda x: self.ustaw_paliwo("PB95")
        )

        self.btn_pb98.bind(
            on_press=lambda x: self.ustaw_paliwo("PB98")
        )

        self.btn_on.bind(
            on_press=lambda x: self.ustaw_paliwo("ON")
        )

        self.btn_lpg.bind(
            on_press=lambda x: self.ustaw_paliwo("LPG")
        )

        self.btn_elektryk.bind(
            on_press=lambda x: self.ustaw_paliwo("Elektryk")
        )

        paliwa_layout = GridLayout(
            cols=2,
            spacing=dp(10),
            size_hint=(0.95, None),
            height=dp(120),
            pos_hint={"center_x": 0.5}
        )

        paliwa_layout.add_widget(self.btn_pb95)
        paliwa_layout.add_widget(self.btn_pb98)
        paliwa_layout.add_widget(self.btn_on)
        paliwa_layout.add_widget(self.btn_lpg)

        zapisz_layout = FloatLayout(
            size_hint_y=None,
            height=dp(150)
        )

        ikona_zapisz = Image(
            source="icons/zapis.png",
            fit_mode="contain",
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        napis_zapisz = Label(
            text="Zapisz",
            font_size="28sp",
            bold=True,
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.15}
        )

        btn_zapisz = Button(
            text="",
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "y": 0},
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0)
        )

        zapisz_layout.add_widget(ikona_zapisz)
        zapisz_layout.add_widget(napis_zapisz)
        zapisz_layout.add_widget(btn_zapisz)

        powrot_layout = FloatLayout(
            size_hint_y=None,
            height=dp(150)
        )

        ikona_powrot = Image(
            source="icons/wroc.png",
            fit_mode="contain",
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        napis_powrot = Label(
            text="Powrót",
            font_size="28sp",
            bold=True,
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.15}
        )

        btn_powrot = Button(
            text="",
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "y": 0},
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0)
        )

        powrot_layout.add_widget(ikona_powrot)
        powrot_layout.add_widget(napis_powrot)
        powrot_layout.add_widget(btn_powrot)

        
        ekran.add_widget(tytul)
        ekran.add_widget(self.input_stacja)
        ekran.add_widget(self.input_kwota)
        ekran.add_widget(self.info_label)
        ekran.add_widget(paliwa_layout)
        ekran.add_widget(self.btn_elektryk)
        ekran.add_widget(zapisz_layout)
        ekran.add_widget(powrot_layout)

        self.layout.add_widget(ekran)

        btn_powrot.bind(
            on_press=lambda x: self.pokaz_dodawanie(None)
        )

        btn_zapisz.bind(
            on_press=self.zapisz_paliwo
        )

    

    def pokaz_inne(self, instance):

        self.layout.clear_widgets()

        ekran = BoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(6)
        )

        tytul = Label(
            text="Dodaj Inne",
            font_size="24sp",
            size_hint_y=None,
            height=dp(45)
        )

       

        self.input_nazwa = TextInput(
            hint_text="Podaj nazwę wydatku:",
            size_hint_y=None,
            height=dp(80),
            font_size="22sp",
            padding=[dp(15), dp(22)],
            multiline=False
        )

        self.input_kwota = TextInput(
            hint_text="Podaj kwotę:",
            size_hint_y=None,
            height=dp(80),
            font_size="22sp",
            padding=[dp(15), dp(22)],
            multiline=False
        )

        self.info_label = Label(
            text="",
            color=(1, 0, 0, 1),
            font_size="20sp",
            size_hint_y=None,
            height=dp(30)
        )

        zapisz_layout = FloatLayout(
            size_hint_y=None,
            height=dp(150)
        )

        ikona_zapisz = Image(
            source="icons/zapis.png",
            fit_mode="contain",
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        napis_zapisz = Label(
            text="Zapisz",
            font_size="28sp",
            bold=True,
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.15}
        )

        btn_zapisz = Button(
            text="",
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "y": 0},
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0)
        )

        zapisz_layout.add_widget(ikona_zapisz)
        zapisz_layout.add_widget(napis_zapisz)
        zapisz_layout.add_widget(btn_zapisz)

        powrot_layout = FloatLayout(
            size_hint_y=None,
            height=dp(150)
        )

        ikona_powrot = Image(
            source="icons/wroc.png",
            fit_mode="contain",
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        napis_powrot = Label(
            text="Powrót",
            font_size="28sp",
            bold=True,
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.15}
        )

        btn_powrot = Button(
            text="",
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "y": 0},
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0)
        )

        powrot_layout.add_widget(ikona_powrot)
        powrot_layout.add_widget(napis_powrot)
        powrot_layout.add_widget(btn_powrot)

        
        ekran.add_widget(tytul)
        ekran.add_widget(self.input_nazwa)
        ekran.add_widget(self.input_kwota)
        ekran.add_widget(self.info_label)
        ekran.add_widget(zapisz_layout)
        ekran.add_widget(powrot_layout)

        self.layout.add_widget(ekran)

        btn_powrot.bind(
            on_press=lambda x: self.pokaz_dodawanie(None)
        )

        btn_zapisz.bind(
            on_press=self.zapisz_inne
        )


    
    
    def pokaz_historie(self, instance):

        self.layout.clear_widgets()

        ekran = BoxLayout(
            orientation="vertical",
            padding=[dp(15), dp(10), dp(15), dp(20)],
            spacing=dp(8)
        )

        tytul = Label(
            text="Historia wydatków",
            font_size="24sp",
            bold=True,
            size_hint_y=None,
            height=dp(55),
            halign="center",
            valign="middle"
        )

        ekran.add_widget(tytul)

        liczba_wpisow = Label(
            text=f"Liczba zapisanych wpisów: {len(self.wydatki)}",
            font_size="18sp",
            bold=True,
            size_hint_y=None,
            height=dp(40),
            halign="center",
            valign="middle"
        )

        ekran.add_widget(liczba_wpisow)

        # Przewijana lista wydatków
        scroll = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            bar_width=dp(5)
        )

        lista = BoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            spacing=dp(8),
            padding=[dp(5), dp(5)]
        )

        lista.bind(minimum_height=lista.setter("height"))

        if not self.wydatki:
            lista.add_widget(
                Label(
                    text="Brak zapisanych wydatków",
                    font_size="20sp",
                    size_hint_y=None,
                    height=dp(60)
                )
            )

        else:
            for wydatek in self.wydatki:
                tekst = (
                    f"[color=00ff00]{wydatek['data_czas']} | "
                    f"{wydatek['dzień']}[/color]\n"
                    f"{wydatek['kategoria']}  |  "
                    f"{wydatek['nazwa']}  |  "
                    f"{wydatek['kwota']:.2f} zł"
                )

                rekord = Label(
                    text=tekst,
                    markup=True,
                    font_size="19sp",
                    size_hint=(1, None),
                    height=dp(60),
                    halign="left",
                    valign="middle"
                )

                rekord.bind(
                    width=lambda inst, szerokosc: setattr(
                        inst, "text_size", (szerokosc - dp(10), None)
                    )
                )

                lista.add_widget(rekord)

        scroll.add_widget(lista)
        ekran.add_widget(scroll)

        # Przycisk powrotu
        powrot_layout = FloatLayout(
            size_hint_y=None,
            height=dp(90)
        )

        ikona_powrot = Image(
            source="icons/wroc.png",
            fit_mode="contain",
            size_hint=(1, 1),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.5
            }
        )

        napis_powrot = Label(
            text="Powrót",
            font_size="23sp",
            bold=True,
            color=(1, 1, 1, 1),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.15
            }
        )

        btn_powrot = Button(
            text="",
            size_hint=(1, 1),
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0)
        )

        btn_powrot.bind(
            on_press=lambda x: self.pokaz_menu(None)
        )

        powrot_layout.add_widget(ikona_powrot)
        powrot_layout.add_widget(napis_powrot)
        powrot_layout.add_widget(btn_powrot)

        ekran.add_widget(powrot_layout)

        self.layout.add_widget(ekran)



    
    def pokaz_statystyki(self, instance):
        self.layout.clear_widgets()

        ekran = BoxLayout(
            orientation="vertical",
            padding=[dp(15), dp(10), dp(15), dp(15)],
            spacing=dp(8)
        )

        tytul = Label(
            text="Statystyki",
            font_size="25sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(60)
        )

        ekran.add_widget(tytul)

        # Statystyki miesiąca
        miesiaca_layout = FloatLayout(
            size_hint_y=None,
            height=dp(190)
        )

        ikona_miesiaca = Image(
            source="icons/statystyki_miesiaca.png",
            fit_mode="contain",
            size_hint=(0.65, 0.75),
            pos_hint={"center_x": 0.5, "center_y": 0.65}
        )

        napis_miesiaca = Label(
            text="Statystyki miesiąca",
            font_size="22sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.25),
            pos_hint={"center_x": 0.5, "center_y": 0.10}
        )

        btn_miesiaca = Button(
            text="",
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0)
        )

        miesiaca_layout.add_widget(ikona_miesiaca)
        miesiaca_layout.add_widget(napis_miesiaca)
        miesiaca_layout.add_widget(btn_miesiaca)

        # Statystyki dnia
        dnia_layout = FloatLayout(
            size_hint_y=None,
            height=dp(190)
        )

        ikona_dnia = Image(
            source="icons/statystyki_dnia.png",
            fit_mode="contain",
            size_hint=(0.65, 0.75),
            pos_hint={"center_x": 0.5, "center_y": 0.65}
        )

        napis_dnia = Label(
            text="Statystyki dnia",
            font_size="22sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.25),
            pos_hint={"center_x": 0.5, "center_y": 0.10}
        )

        btn_dnia = Button(
            text="",
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0)
        )

        dnia_layout.add_widget(ikona_dnia)
        dnia_layout.add_widget(napis_dnia)
        dnia_layout.add_widget(btn_dnia)

        # Powrót
        wroc_layout = FloatLayout(
            size_hint_y=None,
            height=dp(110)
        )

        ikona_wroc = Image(
            source="icons/wroc.png",
            fit_mode="contain",
            size_hint=(0.65, 0.85),
            pos_hint={"center_x": 0.5, "center_y": 0.55}
        )

        napis_wroc = Label(
            text="Powrót",
            font_size="22sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.25),
            pos_hint={"center_x": 0.5, "center_y": 0.10}
        )

        btn_wroc = Button(
            text="",
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0)
        )

        wroc_layout.add_widget(ikona_wroc)
        wroc_layout.add_widget(napis_wroc)
        wroc_layout.add_widget(btn_wroc)

        ekran.add_widget(miesiaca_layout)
        ekran.add_widget(dnia_layout)
        ekran.add_widget(wroc_layout)

        btn_miesiaca.bind(
            on_press=self.pokaz_statystyki_miesiaca
        )

        btn_dnia.bind(
            on_press=self.pokaz_statystyki_dnia
        )

        btn_wroc.bind(
            on_press=lambda x: self.pokaz_menu(None)
        )

        self.layout.add_widget(ekran)


    

    
    def pokaz_statystyki_miesiaca(self, instance):
        self.layout.clear_widgets()

        ekran = BoxLayout(
            orientation="vertical",
            padding=[dp(15), dp(15), dp(15), dp(15)],
            spacing=dp(12)
        )

        tytul = Label(
            text="Statystyki miesiąca",
            font_size="28sp",
            bold=True,
            size_hint_y=None,
            height=dp(65)
        )

        self.input_rok = TextInput(
            hint_text="Podaj rok:",
            size_hint_y=None,
            height=dp(80),
            font_size="22sp",
            padding=[dp(15), dp(25)],
            multiline=False
        )

        self.input_miesiac = TextInput(
            hint_text="Podaj miesiąc (1-12):",
            size_hint_y=None,
            height=dp(80),
            font_size="22sp",
            padding=[dp(15), dp(25)],
            multiline=False
        )

        self.info_label = Label(
            text="",
            color=(1, 0, 0, 1),
            font_size="20sp",
            size_hint_y=None,
            height=dp(25)
        )

        # Sprawdź
        sprawdz_layout = FloatLayout(
            size_hint_y=None,
            height=dp(150)
        )

        ikona_sprawdz = Image(
            source="icons/zobacz.png",
            fit_mode="contain",
            size_hint=(0.65, 0.85),
            pos_hint={"center_x": 0.5, "center_y": 0.55}
        )

        napis_sprawdz = Label(
            text="Sprawdź",
            font_size="28sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.25),
            pos_hint={"center_x": 0.5, "center_y": 0.10}
        )

        btn_sprawdz = Button(
            text="",
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0)
        )

        sprawdz_layout.add_widget(ikona_sprawdz)
        sprawdz_layout.add_widget(napis_sprawdz)
        sprawdz_layout.add_widget(btn_sprawdz)

        # Powrót
        powrot_layout = FloatLayout(
            size_hint_y=None,
            height=dp(150)
        )

        ikona_powrot = Image(
            source="icons/wroc.png",
            fit_mode="contain",
            size_hint=(0.65, 0.85),
            pos_hint={"center_x": 0.5, "center_y": 0.55}
        )

        napis_powrot = Label(
            text="Powrót",
            font_size="28sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.25),
            pos_hint={"center_x": 0.5, "center_y": 0.10}
        )

        btn_powrot = Button(
            text="",
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0)
        )

        powrot_layout.add_widget(ikona_powrot)
        powrot_layout.add_widget(napis_powrot)
        powrot_layout.add_widget(btn_powrot)

        ekran.add_widget(tytul)
        ekran.add_widget(self.input_rok)
        ekran.add_widget(self.input_miesiac)
        ekran.add_widget(self.info_label)
        ekran.add_widget(sprawdz_layout)
        ekran.add_widget(powrot_layout)

        btn_powrot.bind(
            on_press=lambda x: self.pokaz_statystyki(None)
        )

        btn_sprawdz.bind(
            on_press=self.policz_statystyki_miesiaca
        )

        self.layout.add_widget(ekran)


    
    
    def policz_statystyki_miesiaca(self, instance):

        rok = waliduj_rok(self.input_rok.text)
        miesiac = waliduj_miesiac(self.input_miesiac.text)

        if rok is None:
            self.info_label.text = "Aplikacja działa od 2026"
            return

        if miesiac is None:
            self.info_label.text = "Nieprawidłowy miesiąc (1-12)"
            return

        szukam_miesiaca = f"{str(miesiac).zfill(2)}.{rok}"

        wydatki_miesiaca = [
            wydatek for wydatek in self.wydatki
            if szukam_miesiaca in wydatek["data_czas"]
        ]

        liczba_wydatkow = len(wydatki_miesiaca)

        suma_zakupy = sum(
            w["kwota"] for w in wydatki_miesiaca
            if w["kategoria"] == "Zakupy"
        )

        suma_paliwo = sum(
            w["kwota"] for w in wydatki_miesiaca
            if w["kategoria"] == "Paliwo"
        )

        suma_inne = sum(
            w["kwota"] for w in wydatki_miesiaca
            if w["kategoria"] == "Inne"
        )

        suma_razem = suma_zakupy + suma_paliwo + suma_inne

        self.layout.clear_widgets()

        ekran = BoxLayout(
            orientation="vertical",
            padding=[dp(15), dp(10), dp(15), dp(10)],
            spacing=dp(5)
        )

        tytul = Label(
            text=f"Statystyki miesiąca\n{szukam_miesiaca}",
            font_size="30sp",
            bold=True,
            size_hint_y=None,
            height=dp(100),
            halign="center",
            valign="middle"
        )

        liczba = Label(
            text=f"Liczba wydatków: {liczba_wydatkow}",
            font_size="25sp",
            bold=True,
            size_hint_y=None,
            height=dp(75)
        )

        zakupy = Label(
            text=f"[b]Zakupy: [color=00ff00]{suma_zakupy:.2f} zł[/color][/b]",
            markup=True,
            font_size="28sp",
            size_hint_y=None,
            height=dp(85)
        )

        paliwo = Label(
            text=f"[b]Paliwo: [color=00ff00]{suma_paliwo:.2f} zł[/color][/b]",
            markup=True,
            font_size="28sp",
            size_hint_y=None,
            height=dp(85)
        )

        inne = Label(
            text=f"[b]Inne: [color=00ff00]{suma_inne:.2f} zł[/color][/b]",
            markup=True,
            font_size="28sp",
            size_hint_y=None,
            height=dp(85)
        )

        razem = Label(
            text=f"[b][color=ffaa00]Łączne wydatki:\n{suma_razem:.2f} zł[/color][/b]",
            markup=True,
            font_size="30sp",
            size_hint_y=None,
            height=dp(120),
            halign="center",
            valign="middle"
        )

        powrot_layout = FloatLayout(
            size_hint_y=None,
            height=dp(130)
        )

        ikona_powrot = Image(
            source="icons/wroc.png",
            fit_mode="contain",
            size_hint=(0.65, 0.85),
            pos_hint={"center_x": 0.5, "center_y": 0.55}
        )

        napis_powrot = Label(
            text="Powrót",
            font_size="28sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.25),
            pos_hint={"center_x": 0.5, "center_y": 0.10}
        )

        btn_powrot = Button(
            text="",
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0)
        )

        powrot_layout.add_widget(ikona_powrot)
        powrot_layout.add_widget(napis_powrot)
        powrot_layout.add_widget(btn_powrot)

        btn_powrot.bind(
            on_press=self.pokaz_statystyki_miesiaca
        )

        ekran.add_widget(tytul)
        ekran.add_widget(liczba)
        ekran.add_widget(zakupy)
        ekran.add_widget(paliwo)
        ekran.add_widget(inne)
        ekran.add_widget(razem)
        ekran.add_widget(powrot_layout)

        self.layout.add_widget(ekran)



    

    
    def pokaz_statystyki_dnia(self, instance):
        self.layout.clear_widgets()

        ekran = BoxLayout(
            orientation="vertical",
            padding=[dp(15), dp(15), dp(15), dp(15)],
            spacing=dp(12)
        )

        tytul = Label(
            text="Statystyki dnia",
            font_size="28sp",
            bold=True,
            size_hint_y=None,
            height=dp(65)
        )

        self.input_rok = TextInput(
            hint_text="Podaj rok:",
            size_hint_y=None,
            height=dp(80),
            font_size="22sp",
            padding=[dp(15), dp(22)],
            multiline=False
        )

        self.input_miesiac = TextInput(
            hint_text="Podaj miesiąc (1-12):",
            size_hint_y=None,
            height=dp(80),
            font_size="22sp",
            padding=[dp(15), dp(22)],
            multiline=False
        )

        self.input_dzien = TextInput(
            hint_text="Podaj dzień:",
            size_hint_y=None,
            height=dp(80),
            font_size="22sp",
            padding=[dp(15), dp(22)],
            multiline=False
        )

        self.info_label = Label(
            text="",
            color=(1, 0, 0, 1),
            font_size="20sp",
            size_hint_y=None,
            height=dp(40)
        )

        # Przycisk Sprawdź
        sprawdz_layout = FloatLayout(
            size_hint_y=None,
            height=dp(150)
        )

        ikona_sprawdz = Image(
            source="icons/zobacz.png",
            fit_mode="contain",
            size_hint=(0.65, 0.85),
            pos_hint={"center_x": 0.5, "center_y": 0.55}
        )

        napis_sprawdz = Label(
            text="Sprawdź",
            font_size="28sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.25),
            pos_hint={"center_x": 0.5, "center_y": 0.10}
        )

        btn_sprawdz = Button(
            text="",
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0)
        )

        sprawdz_layout.add_widget(btn_sprawdz)
        sprawdz_layout.add_widget(ikona_sprawdz)
        sprawdz_layout.add_widget(napis_sprawdz)

        # Przycisk Powrót
        powrot_layout = FloatLayout(
            size_hint_y=None,
            height=dp(150)
        )

        ikona_powrot = Image(
            source="icons/wroc.png",
            fit_mode="contain",
            size_hint=(0.65, 0.85),
            pos_hint={"center_x": 0.5, "center_y": 0.55}
        )

        napis_powrot = Label(
            text="Powrót",
            font_size="28sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.25),
            pos_hint={"center_x": 0.5, "center_y": 0.10}
        )

        btn_powrot = Button(
            text="",
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0)
        )

        powrot_layout.add_widget(ikona_powrot)
        powrot_layout.add_widget(napis_powrot)
        powrot_layout.add_widget(btn_powrot)

        ekran.add_widget(tytul)
        ekran.add_widget(self.input_rok)
        ekran.add_widget(self.input_miesiac)
        ekran.add_widget(self.input_dzien)
        ekran.add_widget(self.info_label)
        ekran.add_widget(sprawdz_layout)
        ekran.add_widget(powrot_layout)

        btn_powrot.bind(
            on_press=lambda x: self.pokaz_statystyki(None)
        )

        btn_sprawdz.bind(
            on_press=self.policz_statystyki_dnia
        )

        self.layout.add_widget(ekran)

        
    
    def policz_statystyki_dnia(self, instance):

        rok = waliduj_rok(self.input_rok.text)
        miesiac = waliduj_miesiac(self.input_miesiac.text)
        dzien = waliduj_dzien(self.input_dzien.text)

        

        if rok is None:
            self.info_label.text = "Aplikacja działa od 2026 "
            return
        if miesiac is None:
            self.info_label.text = "Nieprawidłowy miesiąc (1-12)"
            return
        if dzien is None:
            self.info_label.text = "Nieprawidłowy dzień (1-31)"
            return
        szukam_dnia = f"{str(dzien).zfill(2)}.{str(miesiac).zfill(2)}.{rok}"
                
        wydatki_dzien = []

        for wydatek in self.wydatki:
            if szukam_dnia in wydatek["data_czas"]:
                wydatki_dzien.append(wydatek)

        liczba_wydatkow = len(wydatki_dzien)

        suma_zakupy=sum(
            wydatek["kwota"]
            for wydatek in wydatki_dzien
            if wydatek["kategoria"] == "Zakupy"

        )

        suma_paliwa=sum(
            wydatek["kwota"]
            for wydatek in wydatki_dzien
            if wydatek["kategoria"] == "Paliwo"
        )

        suma_inne=sum(
            wydatek["kwota"]
            for wydatek in wydatki_dzien
            if wydatek["kategoria"] == "Inne"
        )

        razem = (
            suma_zakupy +
            suma_paliwa +
            suma_inne
        )

        self.layout.clear_widgets()
        
        ekran = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10
        )

        tytul = Label(
            text=f"Statystyki dnia {szukam_dnia}:",
            font_size="22sp",
            bold=True,
            size_hint_y=None,
            height=dp(55)
        )

        liczba = Label(
            text=f"Liczba wydatków: [b]{liczba_wydatkow}[/b]",
            markup=True,
            font_size="20sp",
            size_hint_y=None,
            height=dp(40)
        )

       

        razem = Label(
            text=f"[b][color=ffaa00]Łączne wydatki: {razem:.2f} zł[/color][/b]",
            markup=True,
            font_size="24sp",
            size_hint_y=None,
            height=dp(45) 
        )

        powrot_layout = FloatLayout(
            size_hint_y=None,
            height=dp(150)
        )

        ikona_powrot = Image(
            source="icons/wroc.png",
            fit_mode="contain",
            size_hint=(1, 1.2),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.5
            }
        )

        napis_powrot = Label(
            text="Powrót",
            font_size="28sp",
            bold=True,
            color=(1, 1, 1, 1),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.15
            }
        )

        btn_powrot = Button(
            text="",
            size_hint=(1, 1),
            pos_hint={
                "center_x": 0.5,
                "y": 0
            },
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0)
        )

        btn_powrot.bind(
            on_press=self.pokaz_statystyki_dnia
        )

        powrot_layout.add_widget(ikona_powrot)
        powrot_layout.add_widget(napis_powrot)
        powrot_layout.add_widget(btn_powrot)

        ekran.add_widget(tytul)
        ekran.add_widget(liczba)

        ekran.add_widget(Widget(
            size_hint_y=None,
            height=15
        ))

      
        
      
       
        scroll = ScrollView(
            size_hint=(1, 2),
            do_scroll_x=False
        )

        lista = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=10
        )

        lista.bind(
            minimum_height=lista.setter("height")
        )
        
      

        ekran.add_widget(razem)
    
        if not wydatki_dzien:

            brak=Label(
                text="Brak zapisanych wydatków w tym dniu",
                font_size="16sp"
            )
            lista.add_widget(brak)

        else:

            for i,wydatek in enumerate(wydatki_dzien,start=1):
                wpis = Label(
                      text=(
                            f"[color=ffaa00]{i}.[/color] "
                            f"{wydatek['data_czas']} | "
                            f"{wydatek['kategoria']} | "
                            f"{wydatek['nazwa']} | "
                            f"[color=00ff00]{wydatek['kwota']:.2f} zł[/color]"
                        ),
                        markup=True,
                        font_size="19sp",
                        size_hint_y=None,
                        height=dp(60)
                    )
                lista.add_widget(wpis)
        scroll.add_widget(lista)

        
        ekran.add_widget(scroll)
        ekran.add_widget(powrot_layout)

        self.layout.add_widget(ekran)



    def dodaj_do_cofniecia(self, pozycje):
        
        if not hasattr(self, "wpisy_do_cofniecia"):
            self.wpisy_do_cofniecia = []

        self.wpisy_do_cofniecia.append(pozycje)
        self.wpisy_do_cofniecia = self.wpisy_do_cofniecia[-10:]  

   
      
    def zapisz_zakupy(self, instance):
        sklep = waliduj_nazwe(self.input_sklep.text)
        kwota = waliduj_kwote(self.input_kwota.text)

        if sklep is None:
            self.info_label.text=("Nieprawidłowa nazwa sklepu ")
            return

        if kwota is None:
            self.info_label.text=("Nieprawidłowa kwota")
            return
        self.info_label.text = (
                f"Dodano: {sklep} | {kwota:.2f} zł"
            )

        dzien = pobierz_dzien_tygodnia()

        kategoria = "Zakupy"
        pozycje = utworz_wydatki(
            kategoria,
            sklep,
            dzien,  
            kwota,
            
        )
        
        pozycje["sesja"] = self.id_sesji
        self.wydatki.append(pozycje)
        self.dodaj_do_cofniecia(pozycje)
        
        
        zapis_json(self.wydatki)
        self.suma_sesji += kwota
        
        self.layout.clear_widgets()

        ekran = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=20
        )
        ikona_ok = Image(
            source="icons/zapis.png",
            size_hint=(1, 1)
        )
        napis = Label(
            text=(
                "[b][color=ffaa00] Dodano wydatek: [/color][/b]\n\n"
                f"[color=ffffff]Kategoria:[/color] [b]{kategoria}[/b]\n"
                f"[color=ffffff]Sklep:[/color] [b]{sklep}[/b]\n"
                f"Kwota: [color=00ff88][b]{kwota:.2f} zł[/b][/color]\n\n"
                "[i]Powrót za 2 sekundy...[/i]"
            ),
            markup=True,
            font_size="24sp"
        )
        ekran.add_widget(ikona_ok)
        ekran.add_widget(napis)

       
        self.layout.add_widget(ekran)

        Clock.schedule_once(
            lambda dt: self.pokaz_dodawanie(None),
            2
        )

    def zapisz_paliwo(self, instance):
        stacja = waliduj_nazwe(self.input_stacja.text)
        kwota = waliduj_kwote(self.input_kwota.text)

        rodzaj = waliduj_rodzaj_paliwa(
            self.rodzaj_paliwa
        )
        if rodzaj is None:
            self.info_label.text ="Wybierz rodzaj paliwa"
            return
        
        if stacja is None:
            self.info_label.text=("Nieprawidłowa nazwa stacji ")
            return

        if kwota is None:
            self.info_label.text=("Nieprawidłowa kwota")
            return
        self.info_label.text = (
                f"Dodano: {stacja} | {kwota:.2f} zł"
            )

        dzien = pobierz_dzien_tygodnia()
        kategoria = "Paliwo"
        pozycje = utworz_wydatki(
            kategoria,
            stacja,
            dzien,
            kwota,
            rodzaj
        )
        
        pozycje["sesja"] = self.id_sesji
        self.wydatki.append(pozycje)
        self.dodaj_do_cofniecia(pozycje)

    

   
        
        
        zapis_json(self.wydatki)
        self.suma_sesji += kwota
        
        self.layout.clear_widgets()

        ekran = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=20
        )

        ikona_ok = Image(
            source="icons/zapis.png",
            size_hint=(1, 1)
        )
        napis = Label(
            text=(
                "[b][color=ffaa00] Dodano wydatek:[/color][/b]\n\n"
                f"[color=ffffff]Kategoria:[/color] [b]{kategoria}[/b]\n"
                f"[color=ffffff]Stacja:[/color] [b]{stacja}[/b]\n"
                f"[color=ffffff]Rodzaj:[/color] [b]{rodzaj}[/b]\n"
                f"Kwota: [color=00ff88][b]{kwota:.2f} zł[/b][/color]\n\n"
                "[i]Powrót za 2 sekundy...[/i]"
            ),
            markup=True,
            font_size="24sp"
        )
        ekran.add_widget(ikona_ok)
        ekran.add_widget(napis)
       
        self.layout.add_widget(ekran)

        Clock.schedule_once(
            lambda dt: self.pokaz_dodawanie(None),
            2
        )        

    def ustaw_paliwo(self, rodzaj):
        self.rodzaj_paliwa= rodzaj
        kolor_domyslny = (0.95, 0.55, 0.05, 1)

        self.btn_pb95.background_color = kolor_domyslny
        self.btn_pb98.background_color = kolor_domyslny
        self.btn_on.background_color = kolor_domyslny
        self.btn_lpg.background_color = kolor_domyslny
        self.btn_elektryk.background_color = kolor_domyslny
    
        if rodzaj =="PB95":
            self.btn_pb95.background_color = (0,1,0,1)
        if rodzaj =="PB98":
            self.btn_pb98.background_color = (0,1,0,1)
        if rodzaj =="ON":
            self.btn_on.background_color = (0,1,0,1)
        if rodzaj =="LPG":
            self.btn_lpg.background_color = (0,1,0,1)
        if rodzaj =="Elektryk":
            self.btn_elektryk.background_color = (0,1,0,1)
        
    def zapisz_inne(self, instance):

        nazwa = waliduj_nazwe(
            self.input_nazwa.text
        )

        kwota = waliduj_kwote(
            self.input_kwota.text
        )

        if nazwa is None:
            self.info_label.text = "Nieprawidłowa nazwa"
            return

        if kwota is None:
            self.info_label.text = "Nieprawidłowa kwota"
            return

        dzien = pobierz_dzien_tygodnia()
        kategoria = "Inne"
        pozycje = utworz_wydatki(
            kategoria,
            nazwa,
            dzien,
            kwota
        )
        pozycje["sesja"] = self.id_sesji
        self.wydatki.append(pozycje)
        self.dodaj_do_cofniecia(pozycje)

        zapis_json(self.wydatki)

        self.suma_sesji += kwota

        self.layout.clear_widgets()

        ekran = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=20
        )

        ikona_ok = Image(
            source="icons/zapis.png",
            size_hint=(1, 1)
        )
        napis = Label(
            text=(
                "[b][color=ffaa00] Dodano wydatek:[/color][/b]\n\n"
                f"[color=ffffff]Kategoria:[/color] [b]{kategoria}[/b]\n"
                f"[color=ffffff]Nazwa:[/color] [b]{nazwa}[/b]\n"
                f"Kwota: [color=00ff88][b]{kwota:.2f} zł[/b][/color]\n\n"
                "[i]Powrót za 2 sekundy...[/i]"
            ),
            markup=True,
            font_size="24sp"
        )
        ekran.add_widget(ikona_ok)
        ekran.add_widget(napis)
        self.layout.add_widget(ekran)

        Clock.schedule_once(
            lambda dt: self.pokaz_dodawanie(None),
            2
        )


    
    def zamknij(self, instance):
        self.layout.clear_widgets()

        if self.usuniety:
            tekst_usuniety = "Usunięte wydatki:\n\n"

            for i, wydatek in enumerate(self.usuniety[-10:], start=1):
                tekst_usuniety += (
                    f"{i}. {wydatek['data_czas']} | "
                    f"{wydatek['kategoria']} | "
                    f"{wydatek['nazwa']} | "
                    f"{wydatek['kwota']:.2f} zł\n"
                )
        else:
            tekst_usuniety = "Nie usunięto żadnych wydatków."

        ekran = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=0
        )

        # Dwie części tła: na początku obie czarne.
        with ekran.canvas.before:
            kolor_gora = Color(0, 0, 0, 1)
            tlo_gora = Rectangle()

            kolor_dol = Color(0, 0, 0, 1)
            tlo_dol = Rectangle()

        def aktualizuj_tlo(inst, val):
            polowa = ekran.height / 2

            tlo_gora.pos = (ekran.x, ekran.y + polowa)
            tlo_gora.size = (ekran.width, polowa)

            tlo_dol.pos = (ekran.x, ekran.y)
            tlo_dol.size = (ekran.width, polowa)

        ekran.bind(pos=aktualizuj_tlo, size=aktualizuj_tlo)
        aktualizuj_tlo(ekran, None)

        # Górna część: podsumowanie.
        gora = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        napis = Label(
            text=(
                "[size=30sp][b]Do zobaczenia![/b][/size]\n\n"
                
                "[size=16sp]Dodano wydatki na kwotę:[/size]\n"
                f"[color=73E6B5][size=34sp][b]{self.suma_sesji:.2f} zł[/b][/size][/color]\n"
                "[size=18sp]Dziękuję za korzystanie z aplikacji![/size]"
            ),
            markup=True,
            color=(1, 1, 1, 1),
            halign="center",
            valign="middle",
            opacity=0
        )

        logo = Image(
            source="icons/logo.png",
            size_hint=(1, 0.5),
            opacity=0
        )

        gora.add_widget(logo)
        gora.add_widget(napis)

        # Separator.
       
                # Separator na środku ekranu.
        with ekran.canvas.after:
            kolor_linii = Color(0.45, 0.9, 0.75, 0)
            linia = Rectangle()

        def aktualizuj_linie(inst, val):
            linia.pos = (
                ekran.x,
                ekran.y + ekran.height / 2 - 1
            )
            linia.size = (ekran.width, 2)

        ekran.bind(pos=aktualizuj_linie, size=aktualizuj_linie)
        aktualizuj_linie(ekran, None)

       

        # Dolna część: usunięte wydatki.
        dol = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        usuniety_label = Label(
            text=tekst_usuniety,
            font_size="16sp",
            color=(1, 1, 1, 1),
            halign="center",
            valign="middle",
            opacity=0
        )

        dol.add_widget(usuniety_label)

        ekran.add_widget(gora)
        
        ekran.add_widget(dol)
        self.layout.add_widget(ekran)

        # Zapis danych przed zakończeniem aplikacji.
        zapis_json(self.wydatki)

        # Etap 1: górne tło i napis.
        Animation(
            rgba=(0.09, 0.17, 0.16, 1),
            duration=1.5
        ).start(kolor_gora)

        Clock.schedule_once(
            lambda dt: Animation(opacity=1, duration=1.0).start(napis),
            0.5
        )
        Clock.schedule_once(
            lambda dt: Animation(opacity=1, duration=1.0).start(logo),
            0.5
        )

    #
    
        # Etap 2: separator.
        def pokaz_separator(dt):
            Animation(
                a=1,
                duration=0.5
            ).start(kolor_linii)

        Clock.schedule_once(pokaz_separator, 2.0)

        # Etap 3: dolne tło i lista.
        def pokaz_dol(dt):
            Animation(
                rgba=(0.09, 0.17, 0.16, 1),
                duration=1.5
            ).start(kolor_dol)

            Animation(
                opacity=1,
                duration=1.0
            ).start(usuniety_label)

        Clock.schedule_once(pokaz_dol, 2.5)

        # Zamknięcie po zakończeniu animacji.
        Clock.schedule_once(lambda dt: self.stop(), 8)

    


    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

if __name__ == "__main__":
    BudgetApp().run()
