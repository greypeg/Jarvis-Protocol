#!/usr/bin/env python

import socket
import tqdm
import os

TCP_IP = "79.130.10.14"
TCP_PORT = 3847
BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

message = s.recv(BUFFER_SIZE).decode()
print("Server:", message)

passw = input("Enter the password: ") 
s.send(passw.encode())

while True:
    command = input("Enter the command you wanna execute:")
    s.send(command.encode())

    if command.lower() == "exit":
        s.close()

    if "send" in command:
        command = command.replace("jarvis ", "")
        filename = command.replace("send ", "")
        filesize = os.path.getsize(filename)
        s.send(f"{filename}{SEPARATOR}{filesize}".encode())

        print(s.recv(BUFFER_SIZE).decode())

        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)

        with open(filename, "rb") as f:
            for _ in progress:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    s.close()
                # we use sendall to assure transimission in busy networks
                s.sendall(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))
        
        print('Successfully get the file')
        s.close()
        print('connection closed')
    
    else:
        results = s.recv(BUFFER_SIZE).decode()
        print(results)