import argparse,socket

class NetCat:
    def __init__(self, args):
        self.args = args

    def run(self):
        # クライアント or サーバー
        if self.args.listen:
            # サーバー
            self.listen()
        else:
            # クライアント
            self.send()

    # サーバーの処理
    def listen(self):
        # UDPの処理
        if self.args.udp:
            # ソケットを作成（IP4, UDP）
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # ソケットをバインド
            self.socket.bind((self.args.target, self.args.port))
            print('UDP Listening')
            # 待ち受ける
            while True:
                try:
                    # データを受信
                    msg, client_address = self.socket.recvfrom(1024)
                    print(f"message: {msg.decode('utf-8')}  from: {client_address}")
                    # データを返信
                    self.socket.sendto('Success to receive message'.encode('utf-8'), client_address)
                except KeyboardInterrupt:
                    self.socket.close()
                    exit()
        # TCPの処理
        else:
            # ソケットを作成（IP4, TCP）
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # ソケットをバインド
            self.socket.bind((self.args.target, self.args.port))
            self.socket.listen()
            print('TCP Listening')
            # 接続されるまで待ち受け
            client_socket, client_address = self.socket.accept()
            print(f"Connection with {client_address} !")
            while True:
                try:
                    # データを受信
                    msg = client_socket.recv(1024)
                    print(f"message: {msg.decode('utf-8')}")
                    # データを返信
                    client_socket.send('Success to receive message'.encode('utf-8'))
                except KeyboardInterrupt:
                    self.socket.close()
                    exit()

    # クライアントの処理
    def send(self):
        # UDPの処理
        if self.args.udp:
            # ソケットを作成（IP4, UDP）
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            while True:
                try:
                    print('Input any messages, or [Ctrl + c] to exit')
                    message = input()
                    # データを送信
                    self.socket.sendto(message.encode('utf-8'), (self.args.target,self.args.port))
                    # データを受信
                    msg, client_address = self.socket.recvfrom(1024)
                    print(f"message: {msg.decode('utf-8')}  from: {client_address}")
                except KeyboardInterrupt:
                    self.socket.close()
                    exit()
        # TCPの処理
        else:
            # ソケットを作成（IP4, TCP）
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 接続
            self.socket.connect((self.args.target, self.args.port))
            print(f"Connection with {self.args.target, self.args.port} !")
            while True:
                try:
                    print('Input any messages, or [Ctrl + c] to exit')
                    message = input()
                    # データを送信
                    self.socket.send(message.encode())
                    # データを受信
                    msg = self.socket.recv(1024)
                    print(f"message: {msg.decode('utf-8')} ")
                except KeyboardInterrupt:
                    self.socket.close()
                    exit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--listen', action='store_true')
    parser.add_argument('-t', '--target')
    parser.add_argument('-p', '--port', type=int)
    parser.add_argument('-u', '--udp', action='store_true')
    args = parser.parse_args()

    nc = NetCat(args)
    nc.run()