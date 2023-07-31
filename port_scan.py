import argparse,socket

class NetCat:
    def __init__(self, args):
        self.args = args

    def run(self):
        if self.args.listen:
            self.listen()
        elif self.args.pscan:
            self.port_scan()
        else:
            self.send()

    def listen(self):
        print('listening')
        # ソケットを作成（IP4, TCP）
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # ソケットをバインド
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(3)
        # 接続されるまで待ち受け
        client_socket, _ = self.socket.accept()
        while True:
            request = client_socket.recv(1024)
            print(f'[*] Received: {request.decode("utf-8")}')
            client_socket.send(b'ACK')

    def send(self):
        # ソケットを作成（IP4, TCP）
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.args.target, self.args.port))
        print('connect')
        while True:
            message = input('[*] Send: ')
            self.socket.send(message.encode())
            recv = self.socket.recv(1024)
            print(f'[*] Received: {recv.decode("utf-8")}')

    def port_scan(self):
        if self.args.port.find('-') != -1:
            port_list = self.args.port.split('-')
            min_port = int(port_list[0])
            max_port = int(port_list[1])
        else:
            min_port = int(self.args.port)
            max_port = int(self.args.port)

        for port in range(min_port,max_port+1):
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            return_code = self.socket.connect_ex((self.args.target, port))
            self.socket.close()
            if return_code == 0:
                print(f'{port}: open')
            else:
                print(f'{port}: close')




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--listen', action='store_true')
    parser.add_argument('-t', '--target')
    parser.add_argument('-p', '--port')
    parser.add_argument('-z', '--pscan', action='store_true')
    args = parser.parse_args()

    nc = NetCat(args)
    nc.run()