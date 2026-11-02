from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
def stworz_przycisk_paliwa(tekst):
    btn = Button(
        text=tekst,
        size_hint=(0.2, None),
        height=40,
        background_normal="",
        background_down="",
        background_color=(0.18, 0.24, 0.40, 1),
        color=(1, 1, 1, 1)
    )

    with btn.canvas.before:
        btn.bg_color = Color(0.18, 0.24, 0.40, 1)
        btn.bg = RoundedRectangle(
            pos=btn.pos,
            size=btn.size,
            radius=[15]
        )

    def aktualizuj(widget, value):
        btn.bg.pos = widget.pos
        btn.bg.size = widget.size

    btn.bind(pos=aktualizuj, size=aktualizuj)

    btn.background_color = (0, 0, 0, 0)

    return btn
