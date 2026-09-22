import os
import socket
from datetime import datetime


class SocketServer:
    def __init__(self):
        self.bufsize = 1024

        with open('./response.bin', 'rb') as file:
            self.RESPONSE = file.read()

        self.DIR_PATH = './request'
        self.IMAGE_DIR_PATH = './images'

        self.createDir(self.DIR_PATH)
        self.createDir(self.IMAGE_DIR_PATH)

    def createDir(self, path):
        """디렉토리 생성"""
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except OSError:
            print("Error: Failed to create the directory.")

    def getBoundary(self, response):
        """HTTP Header에서 multipart boundary 추출"""

        header_end = response.find(b"\r\n\r\n")

        if header_end == -1:
            return None

        header = response[:header_end].decode('utf-8', errors='ignore')

        for line in header.split("\r\n"):
            if "Content-Type: multipart/form-data" in line and "boundary=" in line:
                boundary = line.split("boundary=")[1].strip()
                return boundary

        return None

    def saveImage(self, response):
        """multipart/form-data에서 이미지 파일 추출 및 저장"""

        boundary = self.getBoundary(response)

        if boundary is None:
            print("Multipart boundary not found.")
            return

        boundary_bytes = ("--" + boundary).encode()

        parts = response.split(boundary_bytes)

        for part in parts:

            # 이미지 파일이 포함된 part 찾기
            if b'filename="' not in part:
                continue

            # part의 Header와 Body 분리
            header_end = part.find(b"\r\n\r\n")

            if header_end == -1:
                continue

            part_header = part[:header_end].decode('utf-8', errors='ignore')
            image_data = part[header_end + 4:]

            # filename 추출
            file_name = None

            for line in part_header.split("\r\n"):
                if 'filename="' in line:
                    file_name = line.split('filename="')[1].split('"')[0]
                    break

            if file_name is None:
                continue

            # boundary 앞의 CRLF 제거
            if image_data.endswith(b"\r\n"):
                image_data = image_data[:-2]

            file_path = os.path.join(self.IMAGE_DIR_PATH, file_name)

            with open(file_path, "wb") as file:
                file.write(image_data)

            print(f"Saved image: {file_path}")

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

                # 클라이언트 요청 수신
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

                # 원문 전체 콘솔 출력
                print(response.decode('utf-8', errors='replace'))


                #파일로 저장 (request/년-월-일-시-분-초.bin)
                now = datetime.now()
                file_name = now.strftime("%Y-%m-%d-%H-%M-%S.bin")
                file_path = os.path.join(self.DIR_PATH, file_name)

                with open(file_path, "wb") as file:
                    file.write(response)

                print(f"Saved request: {file_path}")


                # multipart 이미지 저장
                self.saveImage(response)
                
                clnt_sock.sendall(self.RESPONSE)
                clnt_sock.close()

        except KeyboardInterrupt:
            print("\r\nStop the server...")
            self.sock.close()


if __name__ == "__main__":
    server = SocketServer()
    server.run("127.0.0.1", 8000)