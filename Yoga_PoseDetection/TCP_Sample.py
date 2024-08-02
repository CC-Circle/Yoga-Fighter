import socket

def main():
    # サーバーの設定
    host = '127.0.0.1'
    port = 12345

    # ソケットの作成
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("サーバーが起動しました...")

    # クライアントからの接続を待機
    client_socket, addr = server_socket.accept()
    print(f"接続されました: {addr}")

    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        
        print(f"受け取ったデータ: {data.decode()}")

        if data.decode() == '1':
            response = '10'
            client_socket.send(response.encode())
            print("送信したデータ: 10")

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()


'''
import socket

class TCPServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.server_socket = self._create_server_socket()
    
    def _create_server_socket(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(1)
        print("サーバーが起動しました...")
        return server_socket
    
    def wait_for_connection(self):
        client_socket, addr = self.server_socket.accept()
        print(f"接続されました: {addr}")
        return client_socket
    
    def handle_client(self, client_socket):
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            
            received_message = data.decode()
            print(f"受け取ったデータ: {received_message}")

            if received_message == '1':
                response = '10'
                #client_socket.send(response.encode())
                print("送信したデータ: 10")
    
    def start(self):
        try:
            client_socket = self.wait_for_connection()
            self.handle_client(client_socket)
        finally:
            self.close_connections()
    
    def close_connections(self):
        self.server_socket.close()
        print("サーバーを終了しました")

if __name__ == "__main__":
    server = TCPServer(host='127.0.0.1', port=12345)
    server.start()
'''
