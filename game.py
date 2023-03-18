import socket
import errno
import time
import pickle

GAME_PORT = 6005
# participating clients must use this port for game communication


############## GAME LOGIC ##############
"""def read_pos(pos):
    pos = pos.split(",")
    return int(pos[0]), int(pos[1])


def make_pos(tup):
    return pos(tup[0]) + "," + pos(tup[1])"""

############## EXPORTED FUNCTIONS ##############


def game_server(after_connect):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as accepter_socket:
        accepter_socket.bind(('', GAME_PORT))
        accepter_socket.listen(3)

        # non-blocking to allow keyboard interupts (^c)
        accepter_socket.setblocking(False)
        while True:
            try:
                game_socket, addr = accepter_socket.accept()
            except socket.error as e:
                if e.errno == errno.EAGAIN or e.errno == errno.EWOULDBLOCK:
                    time.sleep(0.1)
                    continue
            break

        game_socket.setblocking(True)
        with game_socket:
            after_connect()
            print('Game Started')

            while True:
                pos = ""
                opp_pos = game_socket.recv(1024).decode()
                # pickle.loads(game_socket.recv(1024))
                if not opp_pos:
                    break
                game_socket.send(pos.encode())
                # game_socket.send(pickle.dumps(pos))


def game_client(opponent):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as game_socket:
        game_socket.connect((opponent, GAME_PORT))
        print('Game Started')

        while True:
            pos = ""
            game_socket.send(pos.encode())
            # game_socket.send(pickle.dumps(pos))
            opp_pos = game_socket.recv(1024).decode()
            # pickle.loads(game_socket.recv(1024))
            if not opp_pos:
                break
