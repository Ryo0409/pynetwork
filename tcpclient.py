# -*- coding : UTF-8 -*-

import socket

target_ip = "127.0.0.1"
target_port = 8080
buffer_size = 4096

tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp_client.connect((target_ip,target_port))

while True:

    try:
       message = input(">")

       if not message:
           continue

       if message.replace(' ', '') == '':
           continue

       tcp_client.send(message.encode())

       response = tcp_client.recv(buffer_size)

       print("Response: {}".format(response))

    except (BrokenPipeError, KeyboardInterrupt):

        tcp_client.close()
        print("Connection closed")
        break
