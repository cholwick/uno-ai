from pygame import *
from functies import toon_welkom_scherm, deck_aanmaken, vraag_speler_profielen, vraag_aantal_spelers, deel_kaarten_uit, start_aflegstapel, pas_kaart_effect_toe, speler_beurt, ai_beurt, check_winst, begin_of_restart_game
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

state = begin_of_restart_game(spelers_namen)

# ==============================
# Maak één Clock aan voor de loop
klok = time.Clock()

# Hoofd game loop
while True:
    speler = state['spelers_volgorde'][state['huidige_index']]
    hand = state['spelers_handen'][speler]
    bovenste_kaart = state['aflegstapel'][-1]

    # AI beurt
    if speler == "AI":
        state['richting'], state['huidige_index'], state['huidige_kleur'] = ai_beurt(
            hand, bovenste_kaart, state['aflegstapel'], state['huidige_kleur'],
            state['richting'], state['huidige_index'], state['spelers_volgorde'], state['spelers_handen'], state['deck'], screen
        )
        if check_winst(screen, speler, hand):
            state = begin_of_restart_game(spelers_namen)
        continue

    # Speler beurt
    gekozen, trok_kaart, volgende_speler, state['scroll_offset'] = speler_beurt(
        screen, speler, hand, bovenste_kaart, state['huidige_kleur'],
        state['richting'], state['huidige_index'], state['spelers_volgorde'], state['scroll_offset'], state['deck']
    )

    # Trek kaart? -> beurt klaar
    if gekozen == "getrokken":
        state['huidige_index'] = volgende_speler
        continue

    # Speel kaart
    hand.remove(gekozen)
    state['aflegstapel'].append(gekozen)
    state['richting'], state['huidige_index'], state['huidige_kleur'] = pas_kaart_effect_toe(
        screen, gekozen, state['richting'], state['spelers_volgorde'], state['huidige_index'], state['spelers_handen'], state['deck']
    )

    # Winst?
    if check_winst(screen, speler, hand):
        state = begin_of_restart_game(spelers_namen)