#!/usr/bin/env python3

import socket
import threading
import subprocess

def handle_client(client_socket):
    try:
        # Receive data from the client
        client_socket.send(b"Enter the name of the file to display:\n")
        filename = client_socket.recv(1024).decode('utf-8').strip()

        # Vulnerable code: directly using user input in a system command
        command = "cat " + filename
        output = subprocess.getoutput(command)

        # Send the output back to the client
        client_socket.send(output.encode('utf-8') + b"\n")
    except Exception as e:
        client_socket.send(f"An error occurred: {e}\n".encode('utf-8'))
    finally:
        client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8888))
    server.listen(5)
    print("Server listening on port 8888...")

    while True:
        client_sock, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_sock,))
        client_handler.start()

if __name__ == "__main__":
    main()
