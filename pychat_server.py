#!/usr/bin/env python3.7
# implementing 3-tier structure: Hall --> Room --> Clients;
# 14-Jun-2013

# imports
import select, socket, sys, pdb
from pychat_util import Hall, Room, Player
import pychat_util

# max msg size
READ_BUFFER = 4096

# user argument or leave blank 
host = sys.argv[1] if len(sys.argv) >= 2 else ''
listen_sock = pychat_util.create_socket((host, pychat_util.PORT))

# houses the chatrooms
hall = Hall()
connection_list = []
connection_list.append(listen_sock) # add host server to conn list

# main loop
while True:
    # Player.fileno()
    read_players, write_players, error_sockets = select.select(connection_list, [], []) # read and edit the conn list
    for player in read_players: # for each person
        if player is listen_sock: # new connection, player is a socket
            new_socket, add = player.accept()
            new_player = Player(new_socket)
            connection_list.append(new_player)
            hall.welcome_new(new_player)

        else: # new message
            msg = player.socket.recv(READ_BUFFER) # read msg
            if msg:
                msg = msg.decode().lower()
                hall.handle_msg(player, msg) # send msg to correct chat room
            else:
                player.socket.close()
                connection_list.remove(player)

    for sock in error_sockets: # close error sockets
        sock.close()
        connection_list.remove(sock)