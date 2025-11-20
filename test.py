import unittest
from functies import kaart_is_speelbaar, pas_kaart_effect_toe, get_kaart_rect
from pygame import Rect

class TestKaartIsSpeelbaar(unittest.TestCase):

    def test_zelfde_kleur(self):
        self.assertTrue(
            kaart_is_speelbaar(("rood", "5"), ("blauw", "7"), "rood")
        )

    def test_zelfde_waarde(self):
        self.assertTrue(
            kaart_is_speelbaar(("groen", "7"), ("blauw", "7"), "rood")
        )

    def test_wild_kaart_altijd_speelbaar(self):
        self.assertTrue(
            kaart_is_speelbaar(("zwart", "wild"), ("geel", "8"), "blauw")
        )

    def test_wild_plus_4_altijd_speelbaar(self):
        self.assertTrue(
            kaart_is_speelbaar(("zwart", "wild+4"), ("geel", "2"), "groen")
        )

    def test_niet_speelbaar(self):
        # kleur ≠ huidige kleur
        # waarde ≠ top waarde
        # geen wild
        self.assertFalse(
            kaart_is_speelbaar(("groen", "5"), ("rood", "9"), "blauw")
        )

    def test_bovenste_kaart_mag_niet_gelezen_worden_als_kleur(self):
        # huidige kleur is GEKOZEN kleur (bij wild)
        # bovenste kaart kan zwart zijn → geen kleurmatch!
        self.assertTrue(
            kaart_is_speelbaar(("rood", "5"), ("zwart", "wild"), "rood")
        )
        self.assertFalse(
            kaart_is_speelbaar(("blauw", "5"), ("zwart", "wild"), "rood")
        )

class TestCardRect(unittest.TestCase):

    def test_rect_berekening(self):
        rect = get_kaart_rect(
        i=0,
        hand_length=5,
        spacing=110,
        scroll_offset=0,
        y=500,
        card_w=100,
        card_h=150,
        screen_width=1280
        )

        self.assertIsInstance(rect, Rect)
        self.assertEqual(rect.y, 500)
        self.assertEqual(rect.width, 100)
        self.assertEqual(rect.height, 150)
    

if __name__ == "__main__":
    unittest.main()
