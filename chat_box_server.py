import PodSixNet.Channel
import PodSixNet.Server

from time import sleep


# interface to the Client
class ClientChannel(PodSixNet.Channel.Channel):
    def Network_send_message(self, data):
        print('entered network send message')
        room_id = data['room_id']
        serialized_text_items = data['text_items']
        self._server.send_message(room_id, serialized_text_items)


class ChatBoxServer(PodSixNet.Server.Server):

    channelClass = ClientChannel

    def __init__(self, host='localhost', port=4200):
        PodSixNet.Server.Server.__init__(self, localaddr=(host, port))

        self.chat_rooms = []
        self.queue = None
        self.room_index = 0

        print('SERVER STARTED ON ' + host)

    # function called whenever connection with new client made
    def Connected(self, channel, addr):
        print('New connection with: {}'.format(channel))
        channel.roomID = self.room_index

        # when there is a new connection, check if there is a game in the queue
        if self.queue is None:
            self.queue = Room(channel, self.room_index)

        else:
            # connect this player with the user already in the queue
            self.queue.user_channels.append(channel)

            # signal to the users that the chat has started
            for user in self.queue.user_channels:
                user.Send({'action': 'startchat', 'room_id': self.room_index})

            # add this game to the list of active games
            self.chat_rooms.append(self.queue)

            # empty queue
            self.queue = None

            # move onto next room
            self.room_index += 1

    def send_message(self, room_id, serialized_text_items):
        chat_room = self.chat_rooms[room_id]
        for connection in chat_room.user_channels:
            connection.Send({'action': 'recvmessage', 'text_items': serialized_text_items})


class Room:
    def __init__(self, player, room_index):
        self.user_channels = [player]
        self.room_ID = room_index


if __name__ == '__main__':
    s = ChatBoxServer()
    while True:
        s.Pump()
        sleep(0.0001)
