from pygame import *
from functies import toon_welkom_scherm, deck_aanmaken, vraag_speler_profielen, vraag_aantal_spelers, deel_kaarten_uit, start_aflegstapel, pas_kaart_effect_toe, speler_beurt, ai_beurt, check_winst, restart_game
from data import WIDTH, HEIGHT
from sys import exit

init()
screen = display.set_mode((WIDTH, HEIGHT),flags = SCALED| HWSURFACE|DOUBLEBUF)
display.set_caption("UNO Spel")
print("Screen ID:", id(screen))

# ==== welkom + spelers setup ====
#welkom scherm tonen
gamemode = toon_welkom_scherm(screen)
event.clear()
if gamemode == "singleplayer":
    spelers_namen = ["Jij", "AI"]
    # Voeg hier singleplayer logica toe indien nodig
elif gamemode == "multiplayer":
    # --- Vraag aantal spelers ---
    aantal_spelers = vraag_aantal_spelers(screen)   
    print("Aantal spelers gekozen:", aantal_spelers)
    # --- Vraag namen van spelers ---
    spelers_namen = vraag_speler_profielen(screen, aantal_spelers)  
    print("Spelers:", spelers_namen)

# ==============================

# ==== spelvoorbereiding ====
deck = deck_aanmaken()
spelers_handen, deck = deel_kaarten_uit(deck, spelers_namen)
aflegstapel, deck = start_aflegstapel(deck)

richting = 1  # 1 voor met de klok mee, -1 voor tegen de klok in
huidige_index = 0  # index van de huidige speler in spelers_namen
huidige_kleur = aflegstapel[-1][0]
spelers_volgorde = spelers_namen.copy()
scroll_offset = 0
melding = ""
melding_timer = 0
beurt_timer = 0
spacing = 110
kaart_breedte = 100

# ==============================
# Maak één Clock aan voor de loop
klok = time.Clock()

# Hoofd game loop
while True:

    speler = spelers_volgorde[huidige_index]
    hand = spelers_handen[speler]
    bovenste_kaart = aflegstapel[-1]

    # AI beurt
    if speler == "AI":
        richting, huidige_index, huidige_kleur = ai_beurt(
            hand, bovenste_kaart, aflegstapel, huidige_kleur,
            richting, huidige_index, spelers_volgorde, spelers_handen, deck, screen
        )
        if check_winst(screen, speler, hand):
            restart_game(spelers_namen)
        continue

    # Speler beurt
    gekozen, trok_kaart, volgende_speler, scroll_offset = speler_beurt(
        screen, speler, hand, bovenste_kaart, huidige_kleur,
        richting, huidige_index, spelers_volgorde, scroll_offset, deck
    )

    # Trek kaart? -> beurt klaar
    if gekozen == "getrokken":
        huidige_index = volgende_speler
        continue

    # Speel kaart
    hand.remove(gekozen)
    aflegstapel.append(gekozen)
    richting, huidige_index, huidige_kleur = pas_kaart_effect_toe(
        screen, gekozen, richting, spelers_volgorde ,huidige_index, spelers_handen, deck
    )

    # Winst?
    if check_winst(screen, speler, hand):
        restart_game(spelers_namen)