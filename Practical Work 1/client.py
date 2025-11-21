import socket
import os

def send_file(sock, filename):
    filesize = os.path.getsize(filename)
    header = f"{filename}|{filesize}\n"
    sock.sendall(header.encode())

    with open(filename, 'rb') as f:
        while chunk := f.read(1024):
            sock.sendall(chunk)
    print(f"Sent {filename}")

def receive_file(sock):
    header = b""
    while not header.endswith(b'\n'):
        header += sock.recv(1)
    filename, filesize = header.decode().strip().split("|")
    filesize = int(filesize)

    with open("received_" + filename, 'wb') as f:
        received = 0
        while received < filesize:
            data = sock.recv(1024)
            if not data:
                break
            f.write(data)
            received += len(data)
    print(f"Received {filename}")

def client(host='127.0.0.1', port=5001):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print(f"Connected to {host}:{port}")
    print("Enter 'send <file>', 'recv' or 'quit': ")

    while True:
        action = input('> ')
        if action.startswith('send '):
            send_file(sock, action.split(' ',1)[1])
        elif action == 'recv':
            receive_file(sock)
        elif action == 'quit':
            break

    sock.close()

if __name__ == "__main__":
    client()
