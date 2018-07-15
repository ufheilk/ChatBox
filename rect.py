import pygame


class Rect:
    """Class to represent rectangle objects to be drawn"""
    def __init__(self, x, y, height, width, color):
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)