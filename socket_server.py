import os
import socket
from datetime import datetime


class SocketServer:
    def __init__(self):
        self.bufsize = 1024

        with open('./response.bin', 'rb') as file:
            self.RESPONSE = file.read()

        self.DIR_PATH = './request'
        self.createDir(self.DIR_PATH)

    def createDir(self, path):
        """디렉토리 생성"""
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except OSError:
            print("Error: Failed to create the directory.")

    def run(self, ip, port):
        """서버 실행"""

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.sock.bind((ip, port))
        self.sock.listen(10)

        print("Start the socket server...")
        print('"Ctrl+C" for stopping the server!\r\n')

        try:
            while True:
                clnt_sock, req_addr = self.sock.accept()

                clnt_sock.settimeout(5.0)

                print("Request message...\r\n")

                response = b""

                # 원문 전체 콘솔로 출력
                while True:
                    try:
                        data = clnt_sock.recv(self.bufsize)

                        if not data:
                            break

                        response += data

                        if len(data) < self.bufsize:
                            break

                    except socket.timeout:
                        break

                print(response.decode('utf-8', errors='replace'))


                #파일로 저장 (request/년-월-일-시-분-초.bin)
                now = datetime.now()
                file_name = now.strftime("%Y-%m-%d-%H-%M-%S.bin")
                file_path = os.path.join(self.DIR_PATH, file_name)

                with open(file_path, "wb") as file:
                    file.write(response)

                print(f"Saved request: {file_path}")


                
                clnt_sock.sendall(self.RESPONSE)
                clnt_sock.close()

        except KeyboardInterrupt:
            print("\r\nStop the server...")
            self.sock.close()


if __name__ == "__main__":
    server = SocketServer()
    server.run("127.0.0.1", 8000)