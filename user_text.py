from text import Text
from util import get_font_height
import xerox

USER_PROMPT = ':'


# returns whether text contains only ASCII characters
def is_ascii(text):
    try:
        text.encode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        return True


class UserText:
    def __init__(self, x, y, max_columns, max_rows, font, username, color):
        # where the first line will start
        self.x = x
        self.y = y
        self.max_cols = max_columns
        self.max_rows = max_rows
        self.font = font
        self.username = username
        self.prompt = username + USER_PROMPT
        self.color = color
        self.text_items = [Text(x, y, font, color, self.prompt)]
        self.newline_offset = get_font_height(self.font)

    def __len__(self):
        return len(self.text_items)

    def add(self, text):
        last_line = self.text_items[-1]
        if len(last_line) + len(text) > self.max_cols:
            # we have reached the right edge of the box

            if len(self.text_items) == self.max_rows:
                # we have reached the bottom edge of the box
                return

            # have reached the end of current line. make new line
            self.text_items.append(Text(self.x, last_line.height() + self.newline_offset,
                                        self.font, self.color))

            if text.isspace():
                return

            words_on_line = last_line.text.split()  # space delimiter

            if len(words_on_line) > 1 and last_line.last_char() != ' ':
                # take most recently line and put it onto the next
                last_word = words_on_line[-1]
                last_line.subtract(len(last_word))
                self.text_items[-1].add(last_word)

        self.text_items[-1].add(text)

    def subtract(self, num_back):
        last_line = self.text_items[-1]
        on_prompt_line = len(self.text_items) == 1

        if on_prompt_line:
            # don't want to allow the prompt to be erased
            if len(last_line) - num_back < len(self.prompt):
                num_back = len(last_line) - len(self.prompt)
            last_line.subtract(num_back)

        else:
            if len(last_line) - num_back < 0:
                # the backspacing has eliminated this line
                num_to_delete = num_back - len(last_line)
                del self.text_items[-1]
                self.subtract(num_to_delete)
            else:
                self.text_items[-1].subtract(num_back)
                # now, check if there should be word back-flow
                words_on_line = last_line.text.split()  # split on space
                if len(words_on_line) == 1:
                    # there is only one word, so it can potentially be put back on the
                    # previous line
                    if len(words_on_line[0]) + len(self.text_items[-2]) <= self.max_cols:
                        word_to_add = words_on_line[0]
                        del self.text_items[-1]
                        self.text_items[-1].add(word_to_add)

    def paste(self):
        clipboard = xerox.paste()
        if is_ascii(clipboard):
            for char in clipboard:
                self.add(char)

    def move(self, rel_y):
        for text_item in self.text_items:
            text_item.move(0, rel_y)

    def delete_lines(self, num_to_delete):
        delete_from = len(self) - num_to_delete
        if delete_from > 0:
            del self.text_items[delete_from:]

    # returns all of the Text objects associated with this UserText
    def get_text(self):
        return self.text_items

    def draw(self, screen):
        for text_item in self.text_items:
            text_item.draw(screen)

