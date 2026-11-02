def pokaz_historie(self, instance):
        scroll = ScrollView(
            size_hint=(1, 3)
        )

        lista = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=2
        )

        lista.bind(
            minimum_height=lista.setter("height")
        )

        self.layout.clear_widgets()

        ekran = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=5
        )

        

        tytul = Label(
            text="Historia wydatków: ",
            font_size="20sp",
            bold=True,
            size_hint_y=None,
            height=50
)
        
        ekran.add_widget(tytul)

        for wydatek in self.wydatki:

            tekst= (
                f"[color=00ff00]{wydatek['data_czas']} | {wydatek['dzień']}[/color]\n" 
                f"{wydatek['kategoria']}  |  "
                f"{wydatek['nazwa']}  |  "
                f"{wydatek['kwota']:.2f} zł"
            )

            lista.add_widget(
                Label(
                    text=tekst,
                    markup=True,
                    font_size="16sp",
                    size_hint_y=None,
                    height=40
                )
            )
      
        
        scroll.add_widget(lista)

        powrot_layout = FloatLayout(
            size_hint_y=None,
            height=60
        )
        ikona_powrot = Image(
            source="icons/wroc.png",
            fit_mode="contain",
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
       

        napis_powrot = Label(
            text="Powrót",
            font_size="18sp",
            bold=True,
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.15}
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
        ekran.add_widget(scroll)

        powrot_layout.add_widget(ikona_powrot)
        powrot_layout.add_widget(napis_powrot)
        powrot_layout.add_widget(btn_powrot)
        
        ekran.add_widget(powrot_layout)
        
                
        
        
        self.layout.add_widget(ekran)
        