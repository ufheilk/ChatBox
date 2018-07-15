from PodSixNet.Connection import ConnectionListener, connection

from time import sleep

from chat_box import ChatBox
from text import Text

from util import *


class ChatBoxClient(ConnectionListener):
    def __init__(self, host='localhost', port=4200):
        pygame.init()
        self.font = pygame.font.Font("Courier New.ttf", 15)
        pygame.display.set_caption("ChatBox")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.username = input('Enter username: ')

        self.chat_box = ChatBox(10, 10, 10, 30, self.font, RED, 3, BLUE,
                                self.username, BLACK)

        self.room_id = None

        self.Connect((host, port))

        self.running = False
        print('Waiting')
        while not self.running:
            self.Pump()
            connection.Pump()
            sleep(0.1)

    def update(self):
        self.Pump()
        connection.Pump()
        self.screen.fill(WHITE)
        self.chat_box.draw(self.screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(1)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.chat_box.input_box.text.subtract(1)
                elif control_pressed(pygame.key.get_pressed()) and event.key == pygame.K_v:
                    # the user wants to paste something
                    self.chat_box.input_box.text.paste()
                elif event.key == pygame.K_RETURN:
                    connection.Send({'action': 'send_message', 'room_id': self.room_id,
                                     'text_items': [t.serialize() for t in self.chat_box.input_box.text.text_items]})
                    #self.chat_box.add(self.chat_box.input_box.text.get_text())
                elif event.key in DISPLAY_KEYS:
                    to_add = chr(event.key)
                    if event.key == pygame.K_q:
                        self.chat_box.input_box.text.delete_lines(2)
                    if shift_pressed(pygame.key.get_pressed()):
                        to_add = shift(to_add)
                    self.chat_box.input_box.text.add(to_add)

    def Network_startchat(self, data):
        self.room_id = data['room_id']

        self.running = True
        print('Connected!')

    # when a message from a user is relayed here via the server
    # add it to the display portion of the chat_box
    def Network_recvmessage(self, data):
        serialized_text_items = data['text_items']
        self.chat_box.add([Text.deserialize(s_t) for s_t in serialized_text_items])


if __name__ == '__main__':
    client = ChatBoxClient()
    while True:
        client.update()