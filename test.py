import unittest
from functies import kaart_is_speelbaar, pas_kaart_effect_toe

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

class TestPasKaartEffectToe(unittest.TestCase):
    

if __name__ == "__main__":
    unittest.main()
