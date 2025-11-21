import socket
import os

def send_file(conn, filename):
    filesize = os.path.getsize(filename)
    header = f"{filename}|{filesize}\n"
    conn.sendall(header.encode())

    with open(filename, 'rb') as f:
        while chunk := f.read(1024):
            conn.sendall(chunk)
    print(f"Sent {filename}")


def receive_file(conn):
    header = b""
    while not header.endswith(b'\n'):
        header += conn.recv(1)
    filename, filesize = header.decode().strip().split("|")
    filesize = int(filesize)

    with open("received_" + filename, 'wb') as f:
        received = 0
        while received < filesize:
            data = conn.recv(1024)
            if not data:
                break
            f.write(data)
            received += len(data)
    print(f"Received {filename}")


def server(host='127.0.0.1', port=5001):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    print(f"Server listening on {host}:{port}")
    conn, addr = s.accept()
    print(f"Connected by {addr}")
    print("Enter 'send <file>', 'recv' or 'quit': ")

    while True:
        action = input('> ')
        if action.startswith('send '):
            send_file(s, action.split(' ',1)[1])
        elif action == 'recv':
            receive_file(s)
        elif action == 'quit':
            break

    conn.close()
    s.close()

if __name__ == "__main__":
    server()
