import socket
import threading
import time

class TCPServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.server_socket = self._create_server_socket()
        self.client_socket = None
        self.running = True
    
    def _create_server_socket(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(1)
        print("サーバーが起動しました...")
        return server_socket
    
    def wait_for_connection(self):
        while self.running:
            try:
                self.client_socket, addr = self.server_socket.accept()
                print(f"接続されました: {addr}")
                self.handle_client()
            except Exception as e:
                print(f"接続エラー: {e}")
    
    def handle_client(self):
        while self.client_socket and self.running:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                
                received_message = data.decode()
                print(f"受け取ったデータ: {received_message}")

                if received_message == '1':
                    response = '10'
                    self.client_socket.send(response.encode())
                    print("送信したデータ: 10")
            except Exception as e:
                print(f"クライアント処理エラー: {e}")
                break
    
    def start(self):
        try:
            # 接続待ちを別スレッドで実行
            connection_thread = threading.Thread(target=self.wait_for_connection)
            connection_thread.start()
            
            # メインスレッドでサーバーが稼働している間、待機する
            while self.running:
                # 他の処理やログ出力を行う
                print("a")
                time.sleep(1)  # メインスレッドが過度に負荷がかからないようにスリープを追加
        finally:
            self.close_connections()
    
    def close_connections(self):
        self.running = False
        if self.client_socket:
            self.client_socket.close()
        self.server_socket.close()
        print("サーバーを終了しました")

if __name__ == "__main__":
    server = TCPServer(host='127.0.0.1', port=12345)
    server_thread = threading.Thread(target=server.start)
    server_thread.start()

    Flag = False
    
    # メインスレッドで他の処理を行う
    while True:
        if Flag:
            print("a")
        else:
            print("b")
        time.sleep(0.01)  # メインスレッドが過度に負荷がかからないようにスリープを追加
