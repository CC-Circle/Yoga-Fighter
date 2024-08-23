import socket
import threading
import time

class TCPServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.server_socket = self._create_server_socket()
        self.Flag = False
        self.SceneMode = -1
        self.client_socket = None
        self.running = True  # サーバーの状態を管理するフラグ
    
    def _create_server_socket(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(1)
        print("サーバーが起動しました...")
        return server_socket
    
    def wait_for_connection(self):
        self.client_socket, addr = self.server_socket.accept()
        print(f"接続されました: {addr}")
        return self.client_socket
    
    def handle_client(self, client_socket):
        try:
            while self.running:
                if self.client_socket is None:  # クライアントソケットが閉じられている場合に終了
                    break
                data = client_socket.recv(1024)
                if not data:
                    break
                
                received_message = data.decode()
                print(f"受け取ったデータ: {received_message}")

                scene_mode = int(received_message)
                if scene_mode > 0:
                    self._set_SceneMode(scene_mode)
                    response = received_message + '0'
                    client_socket.send(response.encode())
                    print(f"送信したデータ: {response}")
        except OSError as e:
            print(f"エラーが発生しました: {e}")
        finally:
            self.client_socket = None  # クライアントソケットの参照を解除
            client_socket.close()
            print("クライアント接続が切れました")
            self._set_SceneMode(-1)
    
    def start(self):
        try:
            while self.running:
                print("接続待ち...")
                if not self.running:  # サーバーが停止している場合に接続処理を終了
                    break
                client_socket = self.wait_for_connection()
                if not self.running:  # サーバーが停止している場合に接続処理を終了
                    break
                self.handle_client(client_socket)
        finally:
            self.close_connections()
    
    def close_connections(self):
        # クライアントに、サーバーが終了したことを通知
        if self.client_socket:
            self.client_socket.send("exit".encode())
            self.client_socket.close()

        if self.server_socket:
            self.server_socket.close()
        print("サーバーを終了しました")

    def _get_Flag(self):
        return self.Flag
    
    def _set_Flag(self, value):
        self.Flag = value

    def _get_SceneMode(self) -> int:
        return self.SceneMode
    
    def _set_SceneMode(self, value: int):
        self.SceneMode = value

    def send_data_to_client(self, message):
        if self.client_socket:
            try:
                self.client_socket.send(message.encode())
                print(f"送信したデータ: {message}")
            except Exception as e:
                print(f"データ送信中にエラーが発生しました: {e}")
        else:
            print("クライアントが接続されていません")

if __name__ == "__main__":
    server = TCPServer(host='127.0.0.1', port=12345)
    server_thread = threading.Thread(target=server.start)
    server_thread.start()

    hoge = 0

    try:
        while True:
            print("SceneMode: ", server._get_SceneMode())

            if server._get_SceneMode() == 1:
                server.send_data_to_client("100")
                #hoge += 1
            
            if hoge >= 100:
                break

            time.sleep(0.05)
    finally:
        server.running = False
        server.close_connections()
        server_thread.join()  # サーバースレッドが終了するのを待つ
