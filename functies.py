from pygame import *
from data import *
from random import shuffle

# game of uno
# give the functions to main.py
def toon_welkom_scherm(screen):
    title_text = FONT_TITLE.render("Welkom bij UNO!", True, RED)
    start_text = FONT_BUTTON.render("Druk op een toets om te starten", True, GREEN)

    while True:
        screen.fill(WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
        display.flip()

        for evt in event.get():
            if evt.type == QUIT:
                quit()
            elif evt.type == KEYDOWN:
                return    


def einde_scherm(screen, winnaar):
    init()
    screen = display.set_mode((400, 300))
    display.set_caption("Einde van het Spel")

    font = font.SysFont(None, 48)
    text = font.render(f"{winnaar} heeft gewonnen!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(200, 150))

    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                running = False
            elif evt.type == KEYDOWN:
                running = False

        screen.fill((0, 0, 0))
        screen.blit(text, text_rect)
        display.flip()

    quit()

def deck_aanmaken():
    deck = []
    for kleur in KLEUREN:
        for waarde in WAARDEN:
            # elke kaart twee keer toevoegen behalve de 0
            deck.append((kleur, waarde))
            if waarde != "0":
                deck.append((kleur, waarde))  
    for _ in range(4):
        deck.append(("zwart", "wild"))
        deck.append(("zwart", "wild+4"))
    shuffle(deck)
    print("Deck aangemaakt met", len(deck), "kaarten.")
    return deck

def deel_kaarten_uit(deck, spelers_namen):
    spelers_handen = {

    }
    for naam in spelers_namen:
        hand = []
        for _ in range(7):
            hand.append(deck.pop())
        spelers_handen[naam] = hand
    return spelers_handen, deck

def start_aflegstapel(deck):
    top_kaart = deck.pop()
    while top_kaart[0] == "zwart":  
        deck.insert(0, top_kaart)  # terugleggen onderaan de stapel
        top_kaart = deck.pop()
    aflegstapel = [top_kaart]
    return aflegstapel, deck

def vraag_speler_profielen(screen, aantal_spelers):
    event.clear()
    namen = [] # reset lijst met namen
    input_text = ''
    huidige_speler = 1 

    while huidige_speler <= aantal_spelers:
        for evt in event.get():
            if evt.type == QUIT:
                quit()
            if evt.type == KEYDOWN:
                if evt.key == K_RETURN:
                    if input_text.strip() != '':
                        namen.append(input_text.strip())
                        input_text = ''
                        huidige_speler += 1
                elif evt.key == K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += evt.unicode

        # Scherm bijwerken
        screen.fill(WHITE)
        titel = FONT_TITLE.render(f"Speler {huidige_speler} naam:", True, BLACK)
        invoer = FONT_BUTTON.render(f"Speler {huidige_speler} naam: {input_text}", True, BLACK)
        screen.blit(titel, (WIDTH // 2 - titel.get_width() // 2, HEIGHT // 3))
        screen.blit(invoer, (WIDTH // 2 - invoer.get_width() // 2, HEIGHT // 2))
        display.flip()

    return namen 

def vraag_aantal_spelers(screen):

    aantal_text = ''

    while True:
        for evt in event.get():
            if evt.type == QUIT:
                quit()
            if evt.type == KEYDOWN:
                if evt.key == K_RETURN:
                    if aantal_text.isdigit() and 2 <= int(aantal_text) <= 10:
                        return int(aantal_text)
                elif evt.key == K_BACKSPACE:
                    aantal_text = aantal_text[:-1]
                else:
                    aantal_text += evt.unicode

        # Scherm bijwerken
        screen.fill(WHITE)
        titel = FONT_TITLE.render("Hoeveel spelers?", True, BLACK)
        invoer = FONT_BUTTON.render(aantal_text, True, BLACK)
        hint = FONT_BUTTON.render("(2 t/m 10 spelers)", True, BLACK)
        screen.blit(titel, (WIDTH//2 - titel.get_width()//2, HEIGHT//3))
        screen.blit(invoer, (WIDTH//2 - invoer.get_width()//2, HEIGHT//2))
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT//2 + 60))
        display.flip()

def kaart_is_speelbaar(kaart, bovenste_kaart, huidige_kleur):
    kleur, waarde = kaart
    top_kleur, top_waarde = bovenste_kaart

    # kaart is speelbaar als de kleur of waarde overeenkomt, of als het een wild kaart is
    return (kleur == huidige_kleur or
            waarde == top_waarde or
            kleur == "zwart"
            )

def pas_kaart_effect_toe(screen, kaart, richting, huidige_index, spelers_volgorde, spelers_handen, deck):
    kleur, waarde = kaart

    volgende_index = (huidige_index + richting ) % len(spelers_volgorde)
    nieuwe_kleur = kleur

    if waarde == "reverse":
        richting *= -1
        #bij 2 spelers werkt reverse als skip
        if len(spelers_volgorde) == 2:
            volgende_index = (huidige_index + richting ) % len(spelers_volgorde)

    elif waarde == "skip":
        # sla een speler over
        volgende_index = (huidige_index + 2 * richting) % len(spelers_volgorde)

    elif waarde == "+2":
        # laat de volgende speler 2 kaarten trekken
        slachtoffer = spelers_volgorde[volgende_index]
        for _ in range(2):
            if deck:
                spelers_handen[slachtoffer].append(deck.pop())
        volgende_index = (huidige_index + 2 * richting) % len(spelers_volgorde)

    elif waarde == "wild":
        print("Je hebt een wild kaart gespeeld.")
        nieuwe_kleur = kies_kleur(screen, nieuwe_kleur)

    elif waarde == "wild+4":
        # laat de volgende speler 4 kaarten trekken
        print("Je hebt een wild+4 kaart gespeeld.")
        nieuwe_kleur = kies_kleur(screen, nieuwe_kleur)
        slachtoffer = spelers_volgorde[volgende_index]
        for _ in range(4):
            if deck:
                spelers_handen[slachtoffer].append(deck.pop())
        volgende_index = (huidige_index + 2 * richting) % len(spelers_volgorde)

    return richting, volgende_index, nieuwe_kleur

def kies_kleur(screen, oude_kleur):
    kleuren = [
        ("rood", RED),
        ("geel", YELLOW),
        ("groen", GREEN),
        ("blauw", BLUE)
    ]

    gekozen_kleur = None
    font_titel = FONT_TITLE
    font_knop = FONT_BUTTON

    while gekozen_kleur is None:
        # achtergrond
        screen.fill(WHITE)

        toon_huidige_kleur(screen, oude_kleur)

        titel = font_titel.render("Kies een kleur:", True, BLACK)
        screen.blit(titel, (WIDTH // 2 - titel.get_width() // 2, HEIGHT // 5))

        # muispositie
        muis_pos = mouse.get_pos()

        # knoppen tekenen
        knop_breedte = 150
        knop_hoogte = 100
        ruimte = 40
        start_x = WIDTH // 2 - (knop_breedte * len(kleuren) + ruimte * (len(kleuren) - 1)) // 2
        y_pos = HEIGHT // 2

        for i, (kleur_naam, kleur_rgb) in enumerate(kleuren):
            rect = Rect(start_x + i * (knop_breedte + ruimte), y_pos, knop_breedte, knop_hoogte)

            if rect.collidepoint(muis_pos):
                draw.rect(screen, kleur_rgb, rect.inflate(10, 10), border_radius=12)
            else:
                draw.rect(screen, kleur_rgb, rect, border_radius=12)

            tekst = font_knop.render(kleur_naam.capitalize(), True, BLACK)
            screen.blit(tekst, (rect.centerx - tekst.get_width() // 2, rect.centery - tekst.get_height() // 2))

        display.flip()

        for evt in event.get():
            if evt.type == QUIT:
                return
            elif evt.type == MOUSEBUTTONDOWN and evt.button == 1:
                for i, (kleur_naam, kleur_rgb) in enumerate(kleuren):
                    rect = Rect(start_x + i * (knop_breedte + ruimte), y_pos, knop_breedte, knop_hoogte)
                    if rect.collidepoint(evt.pos):
                        gekozen_kleur = kleur_naam
    return gekozen_kleur

def toon_huidige_kleur(screen, huidige_kleur):
    kleur_rgb = {
        "rood": RED,
        "geel": YELLOW,
        "groen": GREEN,
        "blauw": BLUE
    }.get(huidige_kleur, BLACK)

    label = FONT_BUTTON.render(f"Huidige kleur:", True, BLACK)
    screen.blit(label, (WIDTH - 280, 20))

    draw.circle(screen, kleur_rgb, (WIDTH - 120, 90), 30)
