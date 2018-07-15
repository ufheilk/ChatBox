import pygame
import copy
from user_text import UserText
from chat_box import ChatBox, InputBox
WINDOW_HEIGHT = 300
WINDOW_WIDTH = 300

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (100, 100, 250)
RED = (255, 80, 80)

DISPLAY_KEYS = [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d,
                pygame.K_e, pygame.K_f, pygame.K_g, pygame.K_h,
                pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l,
                pygame.K_m, pygame.K_n, pygame.K_o, pygame.K_p,
                pygame.K_q, pygame.K_r, pygame.K_s, pygame.K_t,
                pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x,
                pygame.K_y, pygame.K_z, pygame.K_SPACE, pygame.K_PERIOD,
                pygame.K_COMMA, pygame.K_SEMICOLON, pygame.K_LEFTBRACKET,
                pygame.K_RIGHTBRACKET, pygame.K_BACKSLASH, pygame.K_BACKQUOTE,
                pygame.K_EQUALS, pygame.K_MINUS, pygame.K_SLASH, pygame.K_QUOTE, pygame.K_1,
                pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6,
                pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]


SPECIAL_SHIFT_PAIRS = {'`': '~', '1': '!', '2': '@', '3': '#', '4': '$', '5': '%',
                       '6': '^', '7': '&', '8': '*', '9': '(', '0': ')', '-': '_',
                       '=': '+', '[': '{', ']': '}', '\\': '|', ';': ':', '\'': '"',
                       ',': '<', '.': '>', '/': '?'}


def shift_pressed(keys_pressed):
    return keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_RSHIFT]


def control_pressed(keys_pressed):
    return keys_pressed[pygame.K_LCTRL] or keys_pressed[pygame.K_RCTRL]


# applies the keyboard shift to the given char
def shift(char):
    try:
        return SPECIAL_SHIFT_PAIRS[char]
    except KeyError:
        return char.upper()


pygame.init()
font = pygame.font.Font("Courier New.ttf", 15)
pygame.display.set_caption("ChatBox")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

user_text = UserText(10, 10, 30, 15, font, 'sluggo', BLACK)
input_box = InputBox(10, 10, 30, 15, font, BLUE, 'sluggo', BLACK)
chat_box = ChatBox(10, 10, 10, 30, font, RED, 3, BLUE, 'sluggo', BLACK)

running = True

while running:
    screen.fill(WHITE)
    chat_box.draw(screen)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                chat_box.input_box.text.subtract(1)
            elif control_pressed(pygame.key.get_pressed()) and event.key == pygame.K_v:
                # the user wants to paste something
                chat_box.input_box.text.paste()
            elif event.key == pygame.K_RETURN:
                tmp_user_text = UserText(chat_box.input_box.text.x,
                                         chat_box.input_box.text.y,
                                         chat_box.input_box.text.max_cols,
                                         chat_box.input_box.text.max_rows,
                                         chat_box.input_box.text.font,
                                         chat_box.input_box.text.username,
                                         chat_box.input_box.text.color)
                for line in chat_box.input_box.text.text_items:
                    for letter in line.text:
                        tmp_user_text.add(letter)
                chat_box.add(tmp_user_text)
            elif event.key in DISPLAY_KEYS:
                to_add = chr(event.key)
                if event.key == pygame.K_q:
                    chat_box.input_box.text.delete_lines(2)
                if shift_pressed(pygame.key.get_pressed()):
                    to_add = shift(to_add)
                chat_box.input_box.text.add(to_add)

