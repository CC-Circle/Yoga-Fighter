import socket

def main():
    host = '127.0.0.1'  # Unityサーバーのホストアドレス
    port = 12345        # Unityサーバーのポート番号

    # ソケットの作成
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # サーバーに接続
        client_socket.connect((host, port))
        print("サーバーに接続しました")

        # メッセージの送信
        message = '1'
        client_socket.sendall(message.encode())
        print(f"メッセージ送信: {message}")

        # サーバーからの応答を受信
        response = client_socket.recv(1024)
        print(f"サーバーからの応答: {response.decode()}")

if __name__ == "__main__":
    main()
