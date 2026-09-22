# KHU Socket Server Homework

Python Socket Server를 구현하여 클라이언트의 HTTP 요청을 직접 수신하고 저장하는 실습입니다.

## 실습 1 - HTTP Request 저장

클라이언트가 전송한 HTTP Request 전체를 그대로 받아  
`request` 폴더에 이진 파일로 저장합니다.

파일명 형식:

```text
YYYY-MM-DD-HH-MM-SS.bin
```

예시:

```text
request/2026-09-22-21-45-05.bin
```

## 실습 2 - Multipart 이미지 저장

`multipart/form-data` 형식으로 전달된 요청에서 이미지 데이터를 추출하여  
`images` 폴더에 별도 이미지 파일로 저장합니다.

예시:

```text
images/pig.png
```

테스트에 사용한 원본 이미지는 다음 위치에 저장되어 있습니다.

```text
test_images/pig.png
```

## 실행 방법

```bash
python socket_server.py
```

서버 주소:

```text
127.0.0.1:8000
```

## 프로젝트 구조

```text
KHU_Socket_Server_HW/
├─ images/
│  └─ pig.png
├─ request/
│  └─ 2026-09-22-21-45-05.bin
├─ test_images/
│  └─ pig.png
├─ response.bin
├─ socket_server.py
└─ README.md
```
