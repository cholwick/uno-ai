from pygame import *
from data import *
from random import shuffle, randrange, choice
from sys import exit
from confetti import Confetti

# game of uno
# give the functions to main.py
                
def toon_welkom_scherm(screen):
    title_text = FONT_TITLE.render("Welkom bij UNO!", True, RED)
    
    singleplayer_text = FONT_TITLE.render("1. Singleplayer", True, BLACK)
    multiplayer_text = FONT_TITLE.render("2. Multiplayer", True, BLACK)

    while True:
        screen.fill(WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
        screen.blit(singleplayer_text, (WIDTH // 2 - singleplayer_text.get_width() // 2, HEIGHT // 2))
        screen.blit(multiplayer_text, (WIDTH // 2 - multiplayer_text.get_width() // 2, HEIGHT // 2 + 60))

        display.flip()

        for evt in event.get():
            if evt.type == QUIT:
                exit()
            if evt.type == KEYDOWN:
                if evt.key == K_ESCAPE:
                    quit()
                    exit()
                elif evt.key == K_1:
                    return "singleplayer"
                elif evt.key == K_2:
                    return "multiplayer"  


def einde_scherm(screen, winnaar):
    confettis = []
    confettis_timer = 0
    
    winner_text = FONT_TITLE.render(f"{winnaar.capitalize()} wint!", True, RED)
    klik_esc_text = FONT_BUTTON.render("klik esc", True, BLACK)

    active = True

    # eind loop voor confetti
    while active:
        screen.fill(WHITE)
        screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 3))
        screen.blit(klik_esc_text, (WIDTH // 2 - klik_esc_text.get_width() // 2, HEIGHT // 2))

        if confettis_timer == 0:
            # randrange is een een random range function
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

def ai_beurt(hand, bovenste_kaart, aflegstapel, huidige_kleur, richting, huidige_index, spelers_volgorde, spelers_handen, deck, screen):
    print("AI is aan de beurt...")

    # Zoek een speelbare kaart
    speelbare = [k for k in hand if kaart_is_speelbaar(k, bovenste_kaart, huidige_kleur)]

    if speelbare:
        gekozen = speelbare[0]  # simpelste AI: eerste speelbare kaart
        print("AI speelt:", gekozen)
        hand.remove(gekozen)
        aflegstapel.append(gekozen)
        richting, huidige_index, huidige_kleur = pas_kaart_effect_toe(
            screen, gekozen, richting, spelers_volgorde, huidige_index, spelers_handen, deck
        )
    else:
        print("AI trekt een kaart")
        if deck:
            getrokken = deck.pop()
            hand.append(getrokken)
            print(hand)
        huidige_index = (huidige_index + richting) % len(spelers_volgorde)

    return richting, huidige_index, huidige_kleur

def speler_beurt(screen, speler, hand, bovenste_kaart, huidige_kleur, richting, huidige_index, spelers_volgorde, scroll_offset, deck):
    print(f"{speler} bent/is aan de beurt.")
    melding = ""
    melding_timer = 0
    gekozen = None
    trok_kaart = False
    volgende = (huidige_index + richting) % len(spelers_volgorde)

    spacing = 110
    kaart_breedte = 100

    klok = time.Clock()

    while gekozen is None:

        scroll_offset = scroll_hand(scroll_offset, hand, WIDTH, spacing, kaart_breedte)
        toon_spel_status(screen, speler, hand, melding, melding_timer, scroll_offset, bovenste_kaart, huidige_kleur)

        for evt in event.get():
            if evt.type == QUIT:
                quit(); exit()

            if evt.type == KEYDOWN and evt.key == K_ESCAPE:
                quit(); exit()

            # Scroll hand
            if evt.type == MOUSEWHEEL:
                scroll_offset += evt.y * 25

            # Trek kaart knop
            if evt.type == MOUSEBUTTONDOWN and evt.button == 1:
                if Rect(WIDTH//2 - 400, HEIGHT - 260, 230, 60).collidepoint(*evt.pos):
                    if deck:
                        hand.append(deck.pop())
                        gekozen = "getrokken"
                        trok_kaart = True
                        return gekozen, trok_kaart, volgende, scroll_offset

            # Kaart spelen
            if evt.type == MOUSEBUTTONUP and evt.button == 1:
                # kaart rects berekenen zoals eerder
                base_x = (WIDTH - (len(hand)*spacing - 10)) // 2
                for i, kaart in enumerate(hand):
                    x = base_x + i*spacing + scroll_offset
                    # Clamp x so cards don't go out of bounds
                    x = max(0, min(x, WIDTH - 100))
                    rect = Rect(x, HEIGHT - 150, 100, 150)

                    if rect.collidepoint(evt.pos):
                        if kaart_is_speelbaar(kaart, bovenste_kaart, huidige_kleur):
                            gekozen = kaart
                        else:
                            melding = "Die kaart kun jij niet spelen"
                            melding_timer = FPS * 2
                        break

        melding_timer -= 1
        klok.tick(FPS)

    return gekozen, trok_kaart, volgende, scroll_offset

def check_winst(screen, speler, hand):
    if len(hand) == 1:
        print(f"{speler} roept UNO!")

    if len(hand) == 0:
        print(f"{speler} wint!")
        einde_scherm(screen, speler)
        return True
    
    return False

def begin_of_restart_game(spelers_namen):
    """
    Maakt een complete fresh-game-state aan.
    Wordt gebruikt bij het opstarten én bij herstarten na winst.
    """

    # Nieuw deck + schudden
    deck = deck_aanmaken()

    # Handen uitdelen
    spelers_handen, deck = deel_kaarten_uit(deck, spelers_namen)

    # Eerste kaart op de aflegstapel
    aflegstapel, deck = start_aflegstapel(deck)

    # Bouw game state dictionary
    state = {
        "deck": deck,
        "spelers_handen": spelers_handen,
        "aflegstapel": aflegstapel,

        # Spelvolgorde & turn-control
        "richting": 1,  
        "huidige_index": 0,
        "spelers_volgorde": spelers_namen.copy(),

        # Huidige speel-kleur (kan later door wild worden aangepast)
        "huidige_kleur": aflegstapel[-1][0],

        # UI / Animatie state
        "scroll_offset": 0,
        "melding": "",
        "melding_timer": 0,
        "beurt_timer": 0,
    }

    return state


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
    # twee waardes omdat het een lijst is met twee items
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
        nieuwe_kleur = kies_kleur(screen, speler[index])

    return richting, volgende, nieuwe_kleur


def kies_kleur(screen, speler=None):
    """
    Laat de speler een kleur kiezen,
    of kies automatisch voor AI.
    """
    kleuren = [
        ("rood", RED),
        ("geel", YELLOW),
        ("groen", GREEN),
        ("blauw", BLUE)
    ]

    # ------------------------------------------------------------
    # AI kiest direct een kleur (random of slim later)
    # ------------------------------------------------------------
    if speler == "ai" or speler == "AI":
        gekozen_kleur = choice(["rood", "geel", "groen", "blauw"])
        print("AI kiest kleur:", gekozen_kleur)
        return gekozen_kleur
    # ------------------------------------------------------------
    else:
        gekozen_kleur = None
        font_titel = FONT_TITLE
        font_knop = FONT_BUTTON
        klok = time.Clock()

        while gekozen_kleur is None:
            screen.fill(WHITE)

            titel = font_titel.render("Kies een kleur:", True, BLACK)
            screen.blit(titel, (WIDTH // 2 - titel.get_width() // 2, HEIGHT // 5))

            muis_pos = mouse.get_pos()
            knop_breedte = 150
            knop_hoogte = 100
            ruimte = 40
            start_x = WIDTH // 2 - (knop_breedte * 4 + ruimte * 3) // 2
            y_pos = HEIGHT // 2

            for i, (kleur_naam, kleur_rgb) in enumerate(kleuren):
                rect = Rect(start_x + i * (knop_breedte + ruimte), y_pos, knop_breedte, knop_hoogte)

                if rect.collidepoint(muis_pos):
                    draw.rect(screen, kleur_rgb, rect.inflate(10, 10), border_radius=12)
                else:
                    draw.rect(screen, kleur_rgb, rect, border_radius=12)

                tekst = font_knop.render(kleur_naam.capitalize(), True, BLACK)
                screen.blit(tekst, (rect.centerx - tekst.get_width() // 2,
                                    rect.centery - tekst.get_height() // 2))

            for evt in event.get():
                if evt.type == QUIT:
                    exit()

                elif evt.type == MOUSEBUTTONDOWN and evt.button == 1:
                    for i, (kleur_naam, kleur_rgb) in enumerate(kleuren):
                        rect = Rect(start_x + i * (knop_breedte + ruimte), y_pos, knop_breedte, knop_hoogte)
                        if rect.collidepoint(evt.pos):
                            gekozen_kleur = kleur_naam

            display.flip()
            klok.tick(30)

        return gekozen_kleur


def get_kaart_rect(i, hand_length, spacing, scroll_offset, y, card_w, card_h, screen_width):
    base_x = (screen_width - (hand_length * spacing - 10)) // 2
    x = base_x + i * spacing + scroll_offset
    
    # Clamp x so cards don't go too far right or left
    x = max(0, min(x, screen_width - card_w))
    
    return Rect(x, y, card_w, card_h)

def detect_hover(spacing, hand, scroll_offset, y_kaart, kaart_breedte, kaart_hoogte, screen_width):
    muis_pos = mouse.get_pos()
    for i in range(len(hand)):
        kaart_rect = get_kaart_rect(i, len(hand), spacing, scroll_offset, y_kaart, kaart_breedte, kaart_hoogte, screen_width)
        if kaart_rect.collidepoint(muis_pos):
            return i
    return None

def draw_kaart(screen, kaart, rect, huidige_kleur=None):
    kleur, waarde = kaart

    # --- SPECIALE (WILD) KAARTEN ---
    if kleur == "zwart":  
        # huidige_kleur bepaalt de afbeelding bij wild/wild+4
        if huidige_kleur is None:
            path = f"images/special_cards/{waarde}.png"  # standaard naar blauw als fallback
        else:
            kleur_map = {
                "rood": "red",
                "geel": "yellow",
                "groen": "green",
                "blauw": "blue"
            }

            # fallback: als huidige_kleur nog None is (bijv. eerste beurt)
            chosen = kleur_map.get(huidige_kleur, "blue")
            path = f"images/special_cards/{waarde}_{chosen}.png"

    else:
        # --- NORMALE KAARTEN ---
        folder_map = {
            "rood": "red_cards",
            "geel": "yellow_cards",
            "groen": "green_cards",
            "blauw": "blue_cards"
        }

        folder = folder_map[kleur]
        path = f"images/{folder}/{waarde}.png"

    # --- LADEN EN TEKENEN ---
    img = image.load(path).convert_alpha()
    img = transform.scale(img, (rect.width, rect.height))
    screen.blit(img, (rect.x, rect.y))

def draw_kaart_hovered(screen, kaart, rect):
    scale = 1.25
    new_w = int(rect.width * scale)
    new_h = int(rect.height * scale)

    new_x = rect.x - (new_w - rect.width) // 2
    new_y = rect.y - (new_h - rect.height) - 10

    hovered_rect = Rect(new_x, new_y, new_w, new_h)
    draw_kaart(screen, kaart, hovered_rect, huidige_kleur=None)


def toon_spel_status(screen, speler, hand, melding=None, melding_timer=0, scroll_offset=0, bovenste_kaart=None, gekozen_kleur=None):
    screen.fill(WHITE)

    # titel
    font = FONT_TITLE
    text = font.render(f"{speler.capitalize()} is aan de beurt", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 5))

    # bovenste kaart
    if bovenste_kaart is not None:
        kaart_rect = Rect(WIDTH // 2 - 75, HEIGHT // 2 - 100, 150, 225)
        draw_kaart(screen, bovenste_kaart, kaart_rect, huidige_kleur=gekozen_kleur)

    hover_index = detect_hover(110, hand, scroll_offset, HEIGHT - 150, 100, 150, WIDTH)
    for i, kaart in enumerate(hand):
        rect = get_kaart_rect(i, len(hand), 110, scroll_offset, HEIGHT - 150, 100, 150, WIDTH)
        if i == hover_index:
            continue
        draw_kaart(screen, kaart, rect, huidige_kleur=None)

    if hover_index is not None:
        rect = get_kaart_rect(hover_index, len(hand), 110, scroll_offset, HEIGHT - 150, 100, 150, WIDTH)
        kaart = hand[hover_index]
        draw_kaart_hovered(screen, kaart, rect)
    # trek een kaart knop

    draw_button(screen, WIDTH // 2 - 400, HEIGHT - 260, "Trek een kaart", FONT_BUTTON, GREY, BLACK)
    
    # eventuele melding
    if melding_timer > 0 and melding is not None:
        melding_font = FONT_BUTTON
        melding = "dit kaart is niet speelbaar!"
        melding_text = melding_font.render(melding, True, RED)
        screen.blit(melding_text, (WIDTH // 2 - melding_text.get_width() // 2, HEIGHT // 2 - melding_text.get_height() // 2 - 150))  

    # altijd aan het einde!!!!!
    display.flip()

    
def draw_button(screen, x, y, text, font, bg_color, text_color):
    tekst = font.render(text, True, text_color)
    draw.rect(screen, bg_color, ((x + 4, y), (tekst.get_width() + 10, tekst.get_height() + 5)), border_radius=8)
    screen.blit(tekst, (x + 6, y))

    # draw.rect(screen, kaart_kleur, kaart_rect, border_radius=8)
    # kaart_font = FONT_BUTTON
    # kaart_text = kaart_font.render(str(waarde), True, BLACK)
    # text_x = kaart_rect.x + (kaart_rect.width - kaart_text.get_width()) // 2
    # text_y = kaart_rect.y + (kaart_rect.height - kaart_text.get_height()) // 2
    # screen.blit(kaart_text, (text_x, text_y))
    # ==============================================================================

def scroll_hand(scroll_offset, hand, width, spacing, kaart_breedte):
    # totale breedte
    totale_breedte = len(hand) * spacing - 10
    max_offset = max(0, totale_breedte - width + kaart_breedte)

    key_pressed = key.get_pressed()
    if key_pressed[K_LEFT]:
        scroll_offset -= 10  # scroll links (kaarten naar rechts)
    elif key_pressed[K_RIGHT]:
        scroll_offset += 10  # scroll rechts (kaarten naar links)

    # clamp: tussen -max_offset en 0
    if scroll_offset > 0:
        scroll_offset = 0
    elif scroll_offset < -max_offset:
        scroll_offset = -max_offset

    return scroll_offset
