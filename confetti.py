from pygame import *

class Confetti:
    def __init__(self, x, y, color, orientation, sway):
        self.x, self.y = x, y
        self.color = color
        self.orientation = orientation
        self.sway = sway
    
    def update(self, screen):
        if self.orientation == "vertical": draw.rect(screen, self.color, ((self.x, self.y), (5, 10)))
        if self.orientation == "horizontal": draw.rect(screen, self.color, ((self.x, self.y), (10, 5)))
        self.y += 2
        self.x += self.sway / 2