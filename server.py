import socket
import pickle
from _thread import *
from main import other_players_list
import sys


server = "192.168.223.237"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print('Waiting for connections')


def thread_client(connection, player):
    connection.send(pickle.dumps(other_players_list[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(connection.recv(1024))
            other_players_list[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = other_players_list[0]
                else:
                    reply = other_players_list[1]
                print("Recieved ", data)
                print("sending ", reply)
            connection.sendall(pickle.dumps(reply))
        except:
            break
    print("Lost connection")
    connection.close()


curr_player = 0
while True:
    connection, addr = s.accept()
    print('connected to', addr)
    start_new_thread(thread_client, (connection, curr_player))
    curr_player += 1
