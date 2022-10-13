import socket
import threading


class ClientHandler:
    def __init__(self, server_instance, client):
        self.svr_instance = server_instance
        self.client = client
        self.secret = b'IFMA'

    def recv(self, size):
        try:
            d = b''
            for i in range(size):
                d+= self.client.recv(1)
            return d
        except:
            return b''

    def hand_shake(self):
        dd = self.recv(4)
        if dd != self.secret:
            self.client.close()
            self.svr_instance.remove(self)
            return False
        return True
    
    def send(self, data):
        try:
            self.client.send(data)
            return True
        except:
            self.svr_instance.remove(self)
            return False
        

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen()

        self.clients = []

        self.t = threading.Thread(target=self.accept_client)
        self.t.start()

    def remove(self, client):
        try: self.clients.remove(client)
        except ValueError: pass

    def accept_client(self):
        print(f'Waiting for conenctions at {self.host}:{self.port}')
        while True:
            client, addr = self.sock.accept()
            self.clients.append(ClientHandler(self, client))
            print('handshaking')
            if self.clients[-1].hand_shake():
                print('Accepted connection', addr)
    
    def send_to_all(self, datas):
        ts = []
        for client in self.clients:
            t = threading.Thread(target=self._send_to_client, args=(client, datas))
            t.start()
            ts.append(t)

    def _send_to_client(self, client, datas):
        for data in datas:
            if  not client.send(data):
                break
            
