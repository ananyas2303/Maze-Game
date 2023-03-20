import socket
from _thread import *
import sys


server = "192.168.223.237"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(4)
print('Waiting for connections')


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


def thread_client(connection):
    connection.send(str.encode("Connected"))
    reply = ""
    while True:
        try:
            data = connection.recv(1024)
            reply = data.decode("utf-8")
            if not data:
                print("Disconnected")
                break
            else:
                print("Recieved ", reply)
                print("sending ", reply)
            connection.sendall(str.encode(reply))

        except:
            break
    print("Lost connection")
    connection.close()


while True:
    connection, addr = s.accept()
    print('connected to', addr)
    start_new_thread(thread_client, (connection,))
