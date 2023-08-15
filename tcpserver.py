# -*- coding : UTF-8 -*-

import socket

server_ip = "127.0.0.1"
server_port = 8080
listen_num = 5
buffer_size = 1024


tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp_server.bind((server_ip, server_port))

tcp_server.listen(listen_num)


connection,address = tcp_server.accept()
print("[*] Connection open [ Source : {}]".format(address))

while True:

    try:

        data = connection.recv(buffer_size)

        if data:
           print("[*] Received Data : {}".format(data))

        connection.send(b"ACK")

    except BrokenPipeError:

        connection.close()
        print("Connection closed")
        break

    except KeyboardInterrupt:

        connection.close()
        print("Server terminated")
        break
