from user_text import UserText
import pygame
from rect import Rect
from util import get_font_height, get_font_width


class InputBox:
    """Class that record's the user input (along with prompt) in a box"""
    def __init__(self, x, y, max_width, num_lines, font, box_background, user, text_color):
        self.font = font
        self.text_color = text_color
        self.user = user
        font_height = get_font_height(font)
        font_width = get_font_width(font)
        box_height = font_height * num_lines
        box_width = font_width * max_width

        self.box = Rect(x, y, box_height, box_width, box_background)
        self.text = UserText(x, y, max_width, num_lines, font, user, text_color)

    def draw(self, screen):
        self.box.draw(screen)
        self.text.draw(screen)


class ChatBox:
    """A box for the user to compose messages and see other's messages"""

    def __init__(self, x, y, num_lines_display, max_width, font, display_background,
                 num_lines_input, input_background, user, input_text_color):
        self.x = x
        self.y = y
        self.num_lines_display = num_lines_display
        self.max_width = max_width
        self.font = font
        self.font_height = get_font_height(font)
        font_width = get_font_width(font)
        display_box_height = self.font_height * num_lines_display
        display_box_width = font_width * max_width
        self.display_box = Rect(x, y, display_box_height, display_box_width,
                                display_background)

        self.display_text = []

        self.display_bottom = y + display_box_height
        self.input_box = InputBox(x, self.display_bottom, max_width, num_lines_input, font,
                                  input_background, user, input_text_color)

    def add(self, text_items):
        for item in text_items:
            item.rect.x = self.x
            item.rect.y = self.display_bottom
            self.display_text.insert(0, item)  # add new text to the bottom
            self.move_display_up()  # move up old text
        # if some text has spilled off the top, get rid of it
        del self.display_text[self.num_lines_display:]

    # moves all text items in the display window up 1
    def move_display_up(self):
        for text in self.display_text:
            text.move(0, -self.font_height)

    def draw(self, screen):
        self.display_box.draw(screen)
        for line in self.display_text:
            line.draw(screen)
        self.input_box.draw(screen)
