# -*- coding : UTF-8 -*-

import socket
import threading
import subprocess

SERVER_PORT = 8080
LISTEN_NUM = 2
BUFFER_SIZE = 4096


def command_handler(connection, address):

    while True:

        try:

            command = connection.recv(BUFFER_SIZE).decode()

            if command:

                print("[*] Received command from {} : {}".format(address,command))

                process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

                connection.send(process.stdout.encode())

            else:

                connection.send(b"Received any commands")

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

            connection_thread = threading.Thread(target=command_handler, args=(connection, address))
            connection_thread.start()

        except KeyboardInterrupt:

            connection.close()
            print("[*] Server terminated")
            exit()

if __name__ == "__main__":

    main()
