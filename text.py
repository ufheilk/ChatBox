from util import *


class Text:
    def __init__(self, x, y, font, color, text=""):
        # x and y are the leftmost center part of the line of text
        self.font = font
        self.color = color
        self.text = text
        self.surface = font.render(text, True, color)
        self.rect = self.surface.get_rect()
        # self.rect.centery = y
        self.rect.y = y
        self.rect.left = x
        self.allow_textflow = False

    @classmethod
    def deserialize(cls, serialized_text):
        return Text(0, 0, generate_font("Courier New.ttf", 15), serialized_text['color'],
                    serialized_text['text'])

    def __len__(self):
        return len(self.text)

    def add(self, extra_text):
        self.text += extra_text
        self.surface = self.font.render(self.text, True, self.color)

    def subtract(self, num_back):
        self.text = self.text[0:len(self.text) - num_back]
        self.surface = self.font.render(self.text, True, self.color)

    def move(self, rel_x, rel_y):
        self.rect.move_ip(rel_x, rel_y)

    def height(self):
        return self.rect.top

    def last_char(self):
        return self.text[-1]

    # returns a dictionary of simple objects that can be used to reconstruct this Text
    # for use in send a Text object over a network with PodSixNet
    def serialize(self):
        return dict(color=self.color, text=self.text)

    def draw(self, screen):
        screen.blit(self.surface, self.rect)
