from pygame import *

# scherminstellingen en functies voor het spel
# krijgt de afmetingen van mijn scherm
WIDTH,HEIGHT = 900,600
FPS = 60

# kleuren
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# lettertypen
font.init()
FONT_TITLE = font.Font(None, 80)
FONT_BUTTON = font.Font(None, 50)

# kaartkleuren en waarden
KLEUREN = ["rood", "geel", "groen", "blauw"]
WAARDEN = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "skip", "reverse", "+2"]
SPECIAAL = ["wild", "wild+4"]