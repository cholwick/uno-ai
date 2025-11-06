from pygame import *
from functies import toon_welkom_scherm,einde_scherm, deck_aanmaken, vraag_speler_profielen, vraag_aantal_spelers, deel_kaarten_uit, start_aflegstapel, kaart_is_speelbaar, pas_kaart_effect_toe, toon_huidige_kleur, toon_spel_status
from data import WIDTH, HEIGHT, FPS, WHITE, BLACK, FONT_TITLE, FONT_BUTTON

init()
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("UNO Spel")
print("Screen ID:", id(screen))

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
scroll_offset = 0  
# ==============================
# Maak één Clock aan voor de loop
klok = time.Clock()

# Hoofd game loop
while True:
    speler = spelers_volgorde[huidige_index]
    hand = spelers_handen[speler]
    bovenste_kaart = aflegstapel[-1]
    gekozen = None  # reset gekozen kaart voor deze beurt

    while gekozen is None:
        scroll_offset = 0  # reset scroll offset aan het begin van elke beurt
        toon_spel_status(screen, speler, hand, bovenste_kaart, huidige_kleur, scroll_offset=scroll_offset)

        for evt in event.get():
            if evt.type == QUIT:
                display.quit()
                quit()

            elif evt.type == MOUSEWHEEL:
                scroll_offset += evt.y * 20  # pas scroll snelheid aan indien nodig

            elif evt.type == KEYDOWN:
                if evt.key == K_LEFT:
                    scroll_offset += 50
                elif evt.key == K_RIGHT:
                    scroll_offset -= 50

            elif evt.type == MOUSEBUTTONDOWN and evt.button == 1:
                x, y = evt.pos
                start_x = 100
                y_kaart = HEIGHT - 150
                spacing = 110
                for i, kaart in enumerate(hand):
                    kaart_rect = Rect(start_x + i * spacing, y_kaart, 100, 130)
                    if kaart_rect.collidepoint(x, y):
                        if kaart_is_speelbaar(kaart, bovenste_kaart, huidige_kleur):
                            gekozen = kaart
                            break  # stop de loop zodra een kaart is gekozen
                        else:
                            toon_spel_status(
                                screen, speler, hand, bovenste_kaart, huidige_kleur,
                                             melding="Die kaart kun je niet spelen!"
                                             )
        max_offset = max(0, len(hand) * 110 - (WIDTH - 200))
        scroll_offset = max(-max_offset, min(0, scroll_offset))

        klok.tick(FPS)  # houd framerate constant

    # Kaart spelen of kaart trekken
    if gekozen is not None:
        print(f"{speler} speelt {gekozen}")
        hand.remove(gekozen)
        aflegstapel.append(gekozen)
        richting, huidige_index, huidige_kleur = pas_kaart_effect_toe(
            screen, gekozen, richting, huidige_index, spelers_volgorde, spelers_handen, deck
        )
    else:
        # Dit gebeurt eigenlijk nooit met de klik-logica, maar blijft fallback
        print(f"{speler} kan geen kaart spelen en moet een kaart trekken.")
        if deck:
            getrokken = deck.pop()
            hand.append(getrokken)
        huidige_index = (huidige_index + richting) % len(spelers_volgorde)

    # Check UNO of winst
    if len(hand) == 1:
        print(f"{speler} roept UNO!")
    elif len(hand) == 0:
        print(f"{speler} heeft gewonnen!")
        einde_scherm(screen, speler)  # optioneel: toon einde scherm
        break
