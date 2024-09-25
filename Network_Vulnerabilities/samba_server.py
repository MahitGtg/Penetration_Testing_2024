#!/usr/bin/env python3
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 9999))  # Telnet port 9999
server_socket.listen(5)

while True:
    client_socket, addr = server_socket.accept()
    client_socket.sendall(b"Busy with an appointment right now, leave your message behind.\\n")

    data = client_socket.recv(1024).decode().strip()
    if data == "GET RADIN_CREDS":
        client_socket.sendall(b"Username: Radin, Password: un1corn_r0b0t\\n")
    else:
        client_socket.sendall(b"Alright see you soon!. Try again.\\n")

    client_socket.close()
