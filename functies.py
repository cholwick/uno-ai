from pygame import *
from data import *
from random import shuffle, randrange, choice
from sys import exit
from confetti import Confetti

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
                exit()
            if evt.type == KEYDOWN:
                if evt.key == K_ESCAPE:
                    quit()
                    exit()
                else:
                    return    


def einde_scherm(screen, winnaar):
    confettis = []
    confettis_timer = 0
    
    winner_text = FONT_TITLE.render(f"{winnaar.capitalize()} wint!", True, RED)
    klik_esc_text = FONT_BUTTON.render("klik esc", True, BLACK)

    active = True

    while active:
        screen.fill(WHITE)

        screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 3))
        screen.blit(klik_esc_text, (WIDTH // 2 - klik_esc_text.get_width() // 2, HEIGHT // 2))

        if confettis_timer == 0:
            confettis.append(Confetti(randrange(0, WIDTH), 0, choice([RED, YELLOW, GREEN, BLUE]), choice(["vertical", "horizontal"]), randrange(-3, 4)))
            confettis_timer = 5

        confettis_timer -= 1

        for confetti in confettis:
            confetti.update(screen)
        
        confettis = [confetti for confetti in confettis if confetti.y < HEIGHT]

        # wacht op afsluiten
        for evt in event.get():
            if evt.type == QUIT:
                quit()
                exit()
            if evt.type == KEYDOWN:
                if evt.key == K_ESCAPE:
                    active = False
        
        display.flip()


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
                exit()
            if evt.type == KEYDOWN:
                if evt.key == K_ESCAPE:
                    quit()
                    exit()
                elif evt.key == K_RETURN:
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
                exit()
            if evt.type == KEYDOWN:
                if evt.key == K_ESCAPE:
                    quit()
                    exit()
                elif evt.key == K_RETURN:
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
    _, top_waarde = bovenste_kaart

    # kaart is speelbaar als de kleur of waarde overeenkomt, of als het een wild kaart is
    return (kleur == huidige_kleur or
            waarde == top_waarde or
            kleur == "zwart"
            )

def Bepaal_effect(kaart, spelers_aantal):
    kleur , waarde = kaart

    if waarde == "skip":
        return {"skip":True}
    if waarde == "reverse":
        return {"reverse":True, "skip": spelers_aantal == 2}
    if waarde == "+2":
        return {"kaarten_trekken":2, "skip":True}
    if waarde == "wild+4":
        return {"kaarten_trekken":4, "skip": True, "kleur_kiezen":True}
    if waarde == "wild":
        return {"kleur_kiezen":True}
    
    return {}

def voer_effect_uit(effect, deck, spelers_handen, slachtoffer):
    if "kaarten_trekken" in effect:
        for _ in range(effect["kaarten_trekken"]):
            spelers_handen[slachtoffer].append(deck.pop())
        

def pas_kaart_effect_toe(screen, kaart, richting, speler, index, spelers_handen, deck):
    effect = Bepaal_effect(kaart, len(speler))

    if effect.get("reverse"):
        richting *= -1

    # wie is volgende speler
    stappen = 2 if effect.get("skip") else 1
    volgende = (index + stappen * richting) % len(speler)

    # strafkaarten
    slachtoffer = speler[(index + richting) % len(speler)]
    voer_effect_uit(effect, deck, spelers_handen, slachtoffer)

    #kleurkeuze
    nieuwe_kleur = kaart[0]
    if effect.get("kleur_kiezen"):
        nieuwe_kleur = kies_kleur(screen)

    return richting, volgende, nieuwe_kleur


def kies_kleur(screen):
    kleuren = [
        ("rood", RED),
        ("geel", YELLOW),
        ("groen", GREEN),
        ("blauw", BLUE)
    ]

    gekozen_kleur = None
    font_titel = FONT_TITLE
    font_knop = FONT_BUTTON
    klok = time.Clock()  # frame limiter

    while gekozen_kleur is None:
        # achtergrond
        screen.fill(WHITE)
        

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

        

        # events afhandelen
        for evt in event.get():
            if evt.type == QUIT:
                exit()
                raise SystemExit
            if evt.type == KEYDOWN:
                if evt.key == K_ESCAPE:
                    quit()
                    exit()
            elif evt.type == MOUSEBUTTONDOWN and evt.button == 1:
                for i, (kleur_naam, kleur_rgb) in enumerate(kleuren):
                    rect = Rect(start_x + i * (knop_breedte + ruimte), y_pos, knop_breedte, knop_hoogte)
                    if rect.collidepoint(evt.pos):
                        gekozen_kleur = kleur_naam
                        
        display.flip()

        klok.tick(30)  # 30 FPS om CPU te sparen

    return gekozen_kleur


def toon_spel_status(screen, speler, hand, bovenste_kaart, huidige_kleur, melding=None, melding_timer=0, scroll_offset=0, dynamic=0):
    screen.fill(WHITE)

    # titel
    font = FONT_TITLE
    text = font.render(f"{speler.capitalize()} is aan de beurt", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 5))

    # bovenste kaart
    kaart_font = FONT_BUTTON
    kleur_map = {
        "rood": RED,
        "geel": YELLOW,
        "groen": GREEN,
        "blauw": BLUE,
        "zwart": BLACK
    }
    kaart_kleur = kleur_map.get(bovenste_kaart[0], (230, 230, 230))  # fallback grijs
    kaart_rect = Rect(WIDTH // 2 - 75, 80, 150, 200)
    kaart_text = bovenste_kaart[1]
    kaart = draw_kaart(screen, bovenste_kaart, (WIDTH // 2 - 75, 125), huidige_kleur, 150, 200, kaart_waarde=kaart_text)
    bovenste_kaart_text = kaart_font.render(f"Bovenste kaart", True, BLACK)
    screen.blit(bovenste_kaart_text, ((WIDTH // 2) - (bovenste_kaart_text.get_width() // 2), 80))


    # hand van de speler
    max_zichtbare_kaarten = 7
    x = 50
    y = (HEIGHT - 150) + (dynamic * 5)
    spacing = 110
    kaart_breedte = 100
    kaart_hoogte = 150

    # berekening van startindex op basis van scroll_offset (scroll gebruikt als page index)
    start_index = max(0, -scroll_offset // spacing)
    eind_index = min(len(hand), start_index + max_zichtbare_kaarten)

    # zichtbare_kaarten = hand[start_index:eind_index]
    

    base_x = (WIDTH - (len(hand) * spacing - 10)) // 2

    # muispositie voor hover-detectie
    muis_pos = mouse.get_pos()

    # teken eerst niet-hovered kaarten, bewaar hovered kaart om later bovenop te tekenen
    hovered = None
    for i, kaart in enumerate(hand):
        kaart_kleur = kleur_map.get(kaart[0], (230, 230, 230))  # fallback grijs
        kaart_waarde = kaart[1]
        rect_x = base_x + i * spacing
        kaart_rect = Rect(rect_x + scroll_offset, y, kaart_breedte, kaart_hoogte)

        if kaart_rect.collidepoint(muis_pos):
            # bewaar hovered kaart om later bovenop te tekenen
            hovered = (i, kaart, kaart_rect, kaart_kleur)
            continue

        # teken normale kaart met png

        #draw.rect(screen, kaart_kleur, kaart_rect, border_radius=10) 'rood': 'red_cards', 'geel': 'yellow_cards', 'groen': 'green_cards', 'blauw': 'blue_cards', 'zwart': 'special_cards', 
        screen.blit(transform.scale(image.load("images/" + {RED: "red_cards", YELLOW: "yellow_cards", GREEN: "green_cards", BLUE: "blue_cards", BLACK: "special_cards"}[kaart_kleur] + "/" + kaart_waarde + ".png").convert_alpha(), (kaart_breedte, kaart_hoogte)), (kaart_rect))
        
        # teken waarde
        # kaart_text = kaart_font.render(str(kaart[1]), True, BLACK)
        # text_x = kaart_rect.x + (kaart_rect.width - kaart_text.get_width()) // 2
        # text_y = kaart_rect.y + (kaart_rect.height - kaart_text.get_height()) // 2
        # screen.blit(kaart_text, (text_x, text_y))

    # teken hovered kaart als die er is, iets groter en iets omhoog geplaatst
    if hovered is not None:
        i, kaart, kaart_rect, kaart_kleur = hovered
        kaart_waarde = kaart[1]
        scale = 1.25
        new_w = int(kaart_rect.width * scale)
        new_h = int(kaart_rect.height * scale)
        new_x = kaart_rect.x - (new_w - kaart_rect.width) // 2
        new_y = kaart_rect.y - (new_h - kaart_rect.height) - 10
        enlarged_rect = Rect(new_x, new_y, new_w, new_h)
        # achtergrond en border
        # draw.rect(screen, kaart_kleur, enlarged_rect, border_radius=10)
        # draw.rect(screen, BLACK, enlarged_rect, 2, border_radius=10)
        screen.blit(transform.scale(image.load("images/" + {RED: "red_cards", YELLOW: "yellow_cards", GREEN: "green_cards", BLUE: "blue_cards", BLACK: "special_cards"}[kaart_kleur] + "/" + kaart_waarde + ".png").convert_alpha(), (kaart_breedte * scale, kaart_hoogte * scale)), (enlarged_rect))
        # teken waarde gecentreerd
        # kaart_text = kaart_font.render(str(kaart[1]), True, BLACK)
        # text_x = enlarged_rect.x + (enlarged_rect.width - kaart_text.get_width()) // 2
        # text_y = enlarged_rect.y + (enlarged_rect.height - kaart_text.get_height()) // 2
        # screen.blit(kaart_text, (text_x, text_y))
    

    # trek een kaart
    #trek_knop_rect = Rect(WIDTH // 2 - 115, HEIGHT - 260, 230, 60)
    draw_button(screen, WIDTH // 2 - 115, HEIGHT - 260, "Trek een kaart", FONT_BUTTON, GREY, BLACK)
    
    # eventuele melding
    if melding_timer > 0:
        melding_text = kaart_font.render(melding, True, "Red")
        screen.blit(melding_text, (WIDTH // 2 - melding_text.get_width() // 2, HEIGHT // 2 - 70))    

    # altijd aan het einde!!!!!
    display.flip()

    
def draw_button(screen, x, y, text, font, bg_color, text_color):
    tekst = font.render(text, True, text_color)
    draw.rect(screen, bg_color, ((x + 4, y), (tekst.get_width() + 10, tekst.get_height() + 5)), border_radius=8)
    screen.blit(tekst, (x + 6, y))

def draw_kaart(screen, kaart, positie, huidige_kleur, kaart_breedte=100, kaart_hoogte=150,  kaart_waarde=None):
    kleur_map = {
        "rood": RED,
        "geel": YELLOW,
        "groen": GREEN,
        "blauw": BLUE,
        "zwart": BLACK
    }
    kleur, waarde = kaart
    kaart_kleur = kleur_map.get(kleur, (230, 230, 230))  # fallback grijs
    if waarde != "wild+4" and waarde != "wild": screen.blit(transform.scale(image.load("images/" + {RED: "red_cards", YELLOW: "yellow_cards", GREEN: "green_cards", BLUE: "blue_cards", BLACK: "special_cards"}[kaart_kleur] + "/" + kaart_waarde + ".png").convert_alpha(), (kaart_breedte, kaart_hoogte)), positie)
    else: screen.blit(transform.scale(image.load("images/special_cards/" + kaart_waarde + "_" + {"rood": "red", "geel": "yellow", "groen": "green", "blauw": "blue", "zwart": "black"}[huidige_kleur] + ".png").convert_alpha(), (kaart_breedte, kaart_hoogte)), positie)
    # draw.rect(screen, kaart_kleur, kaart_rect, border_radius=8)
    # kaart_font = FONT_BUTTON
    # kaart_text = kaart_font.render(str(waarde), True, BLACK)
    # text_x = kaart_rect.x + (kaart_rect.width - kaart_text.get_width()) // 2
    # text_y = kaart_rect.y + (kaart_rect.height - kaart_text.get_height()) // 2
    # screen.blit(kaart_text, (text_x, text_y))
    return f"{kleur} {waarde}"

def scroll_hand(scroll_offset, hand, width, spacing, kaart_breedte):
    # totale breedte
    totale_breedte = len(hand) * spacing -10
    max_offset = max(0, totale_breedte - width + kaart_breedte)

    key_pressed = key.get_pressed()
    if key_pressed[K_LEFT] :
        scroll_offset += 10
    elif key_pressed[K_RIGHT]:
        scroll_offset -= 10

    if scroll_offset > 0:
        scroll_offset = 0
    elif scroll_offset < -max_offset:
        scroll_offset = -max_offset

    return scroll_offset
