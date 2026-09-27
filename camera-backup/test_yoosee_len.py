import socket

host = "192.168.0.2"
port = 554

def move(direction):
    content = f"ptzCmd:{direction}"
    length = len(content)
    move_str = (
        f"SET_PARAMETER rtsp://{host}/onvif1 RTSP/1.0\r\n"
        "CSeq: 0\r\n"
        "Authorization: Basic YWRtaW46Y252YXNjbzU0\r\n"
        "LibVLC/2.2.1 (LIVE555 Streaming Media v2014.07.25)\r\n"
        "Accept: application/sdp\r\n"
        f"Content-length: {length}\r\n"
        "Content-type: " + content + "\r\n\r\n"
    )
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(move_str.encode('utf-8'))
        data = s.recv(1024)
        print("Resp:", data)

move("RIGHT")
