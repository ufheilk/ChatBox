import pygame

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


def generate_font(font_name, size):
    return pygame.font.Font(font_name, size)


def get_font_height(font):
    text_surface = font.render('a', True, (0, 0, 0))
    # 0.9 is a good multiplier to make sure the text doesn't write
    # over itself
    return text_surface.get_rect().height * 0.9


def get_font_width(font):
    text_surface = font.render('a', True, (0, 0, 0))
    return text_surface.get_rect().width
