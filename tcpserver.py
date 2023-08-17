# -*- coding : UTF-8 -*-

import socket
import threading

SERVER_PORT = 8080
LISTEN_NUM = 2
BUFFER_SIZE = 1024


def connection_handle(connection, address):

    while True:

        try:

            data = connection.recv(BUFFER_SIZE)

            if data:
                print("[*] Received Data from {} : {}".format(address,data))

            connection.send(b"ACK")

        except BrokenPipeError:

            connection.close()
            print("[*] Connection from {} closed".format(address))
            break


def main():

    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    tcp_server.bind((socket.gethostname(), SERVER_PORT))

    tcp_server.listen(LISTEN_NUM)

    while True:

        try:

            connection,address = tcp_server.accept()
            print("[*] Connection from {} open".format(address))

            connection_thread = threading.Thread(target=connection_handle, args=(connection, address))
            connection_thread.start()

        except KeyboardInterrupt:

            connection.close()
            print("[*] Server terminated")
            exit()

if __name__ == "__main__":

    main()
