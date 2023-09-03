import argparse
import socket
import threading

class Ftp:


    def __init__(self, mode):
        self.mode = mode
        self.buffer_size = 4096


    def listen(self, listen_port, listen_num, filename):

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((socket.gethostname(), listen_port))
        server.listen(listen_num)

        while True:

            connection,address = server.accept()
            connection_thread = threading.Thread(target=self._file_handler, args=(connection, address, filename), daemon=True)
            connection_thread.start()

    def _file_handler(self, connection, address, filename):

        data = b""
        receive_data = b""

        while True:

            receive_data = connection.recv(self.buffer_size)
            data += receive_data

            # buffer_size以下の場合、以降データを受信しないため
            if len(receive_data) < self.buffer_size:

                connection.send(b"File successfully sent")
                connection.close()

                break

        with open(filename, 'wb') as f:

            f.write(data)


    def send(self, target_ip, target_port, filename):

        with open(filename, "rb") as f:

            read_data = f.read()

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((target_ip, target_port))

        client.send(read_data)
        print(client.recv(self.buffer_size))
        client.close()

if __name__=="__main__":


    parser = argparse.ArgumentParser(description="FTP Server/Client")
    parser.add_argument("mode", help="server or client")
    parser.add_argument("port", type=int, help="server port to listen/to connect")
    parser.add_argument("file", help="filename to send/to recevive")
    parser.add_argument("--server_ip", help="server ip address to connect")
    args = parser.parse_args()

    if args.mode == "server":

        server = Ftp(mode="server")
        server.listen(listen_port=args.port, listen_num=1, filename=args.file)

    else:

        client = Ftp(mode="client")
        client.send(target_ip=args.server_ip, target_port=args.port, filename=args.file)
