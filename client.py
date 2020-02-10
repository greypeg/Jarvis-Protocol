import socket
import tqdm
import os

SEPARATOR = "<SEPARATOR>"
SERVER_HOST = "79.130.10.14"
SERVER_PORT = 3847
BUFFER_SIZE = 4096

flag = 0

s = socket.socket()
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))

message = s.recv(BUFFER_SIZE).decode()
print("Server:", message)

passw = input("Enter the password: ") 
s.send(passw.encode())

while True:  
    command = input("Enter the command you wanna execute:")
    s.send(command.encode())

    if command.lower() == "exit":
        break

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
                    break
                # we use sendall to assure transimission in busy networks
                s.sendall(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))

    else:
        results = s.recv(BUFFER_SIZE).decode()
        print(results)
    print("helo")   

s.close()