from pygame import *
from functies import toon_welkom_scherm,einde_scherm, deck_aanmaken, vraag_speler_profielen, vraag_aantal_spelers, deel_kaarten_uit, start_aflegstapel, kaart_is_speelbaar, pas_kaart_effect_toe, toon_spel_status, draw_button, scroll_hand
from data import WIDTH, HEIGHT, FPS, WHITE, BLACK, FONT_TITLE, FONT_BUTTON
from sys import exit

init()
screen = display.set_mode((WIDTH, HEIGHT),flags = SCALED| FULLSCREEN)
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
    print(hand)
    bovenste_kaart = aflegstapel[-1]
    gekozen = None  # reset gekozen kaart voor deze beurt
    # sentinel to mark that the player drew a card and the turn should end
    trok_kaart = False
    

    # compute the normal next player (one step in current direction)
    volgende_speler = (huidige_index + richting) % len(spelers_volgorde)

    while gekozen is None:
        
        scroll_offset = scroll_hand(scroll_offset, hand, WIDTH, spacing, kaart_breedte)
        toon_spel_status(screen, speler, hand, bovenste_kaart, huidige_kleur, melding, melding_timer, scroll_offset=scroll_offset, dynamic=beurt_timer)

        for evt in event.get():
            if evt.type == QUIT:
                quit()
                exit()

            if evt.type == KEYDOWN:
                if evt.key == K_ESCAPE:
                    quit()
                    exit()

            elif evt.type == MOUSEWHEEL:
                scroll_offset += evt.y * 20  # pas scroll snelheid aan indien nodig

            elif evt.type == MOUSEBUTTONDOWN and evt.button == 1:
                x, y = evt.pos
                start_x = 100
                y_kaart = HEIGHT - 150
                spacing = 110

                # controleer op klikkenvan trek kaart knop
                trek_knop_rect = Rect(WIDTH // 2 - 115, HEIGHT - 260, 230, 60)
                if trek_knop_rect.collidepoint(x, y):
                    if deck:
                        getrokken = deck.pop()
                        hand.append(getrokken)
                        print(hand)
                        # mark that the player drew a card and end their turn
                        trok_kaart = True
                        gekozen = 'getrokken'  # non-None to break out of the input loop

            elif evt.type == MOUSEBUTTONUP and evt.button == 1 and beurt_timer <= 0:
                x, y = evt.pos
                spacing = 110
                kaart_breedte = 100
                kaart_hoogte = 150
                y_kaart = HEIGHT - 150

                # zelfde berekening als in toon_spel_status()
                base_x = (WIDTH - (len(hand) * spacing - 10)) // 2

                for i, kaart in enumerate(hand):
                    kaart_x = base_x + i * spacing + scroll_offset
                    kaart_rect = Rect(kaart_x, y_kaart, kaart_breedte, kaart_hoogte)

                    # tijdelijke visuele debug — laat rode rand zien waar de rect echt ligt
                    draw.rect(screen, "red", kaart_rect, 3)
                    display.flip()

                    if kaart_rect.collidepoint(x, y):
                        if kaart_is_speelbaar(kaart, bovenste_kaart, huidige_kleur):
                            gekozen = kaart
                            beurt_timer = 10
                            break
                        else:
                            melding = "Die kaart kun jij niet spelen"
                            melding_timer = FPS * 2


        melding_timer -= 1

        if beurt_timer > 0:
            beurt_timer -= 1
       
        klok.tick(FPS)  # houd framerate constant

    # Kaart spelen of kaart trekken
    # Als de speler een kaart trok: ga direct door naar de volgende speler
    if gekozen == 'getrokken' and trok_kaart and beurt_timer <= 0:
        huidige_index = volgende_speler
        scroll_offset = 0
        continue

    if gekozen is not None and gekozen != 'getrokken':
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
            huidige_index = volgende_speler

    # Check UNO of winst
    if len(hand) == 1:
        print(f"{speler} roept UNO!")
    elif len(hand) == 0:
        print(f"{speler} heeft gewonnen!")
        einde_scherm(screen, speler) # optioneel: toon einde scherm

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
        melding = ""
        melding_timer = 0
        beurt_timer = 0



