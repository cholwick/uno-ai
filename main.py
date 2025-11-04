from pygame import *
from functies import toon_welkom_scherm,einde_scherm, deck_aanmaken, vraag_speler_profielen, vraag_aantal_spelers, deel_kaarten_uit, start_aflegstapel, kaart_is_speelbaar, pas_kaart_effect_toe, toon_huidige_kleur
from data import WIDTH, HEIGHT, FPS, WHITE, BLACK, FONT_TITLE, FONT_BUTTON

init()
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("UNO Spel")

# ==== welkom + spelers setup ====
#welkom scherm tonen
toon_welkom_scherm(screen)
event.clear()
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
# ==============================

# Hoofd game loop
while True:
    speler = spelers_volgorde[huidige_index]
    hand = spelers_handen[speler]
    bovenste_kaart = aflegstapel[-1]

    screen.fill(WHITE)
    toon_huidige_kleur(screen, huidige_kleur)
    time.delay(1000)  # korte pauze voor duidelijkheid
    display.flip()
    
    # Toon status
    print(f"\n{speler} is aan de beurt.")
    print("Bovenste kaart op aflegstapel:", bovenste_kaart)
    print("Jouw hand:", hand)

    # vind speelbare kaarten
    speelbare_kaarten = [kaart for kaart in hand if kaart_is_speelbaar(kaart, bovenste_kaart, huidige_kleur)]  

    if speelbare_kaarten:
        gekozen = speelbare_kaarten[0]  # voor nu automatisch de eerste speelbare kaart kiezen
        print(f"{speler} speelt {gekozen}")
        hand.remove(gekozen)
        aflegstapel.append(gekozen)
        huidige_kleur = gekozen[0] if gekozen[0] != "zwart" else huidige_kleur
        richting, huidige_index, huidige_kleur= pas_kaart_effect_toe(
            screen, gekozen, richting, huidige_index, spelers_volgorde, spelers_handen, deck
            )
    else:
        print(f"{speler} kan geen kaart spelen en moet een kaart trekken.")
        getrokken = deck.pop()
        hand.append(getrokken)
        huidige_index = (huidige_index + richting) % len(spelers_volgorde)

    
    # check op UNO of winst
    if len(hand) == 1:
        print(f"{speler} roept UNO!")
    elif len(hand) == 0:
        print(f"{speler} heeft gewonnen!")
        break