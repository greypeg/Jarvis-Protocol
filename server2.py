import socket
from threading import Thread
from socketserver import ThreadingMixIn
import subprocess
import tqdm
import os

TCP_IP = "0.0.0.0"
TCP_PORT = 3847
BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"

class ClientThread(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print (" New thread started for "+ip+":"+str(port))

    def run(self):

        file = open("ips.txt","a")
        file.write(f"{ip}:{port} \n")
        file.close()

        message = "Hello and Welcome from " + ip
        self.sock.send(message.encode())

        corr = self.sock.recv(BUFFER_SIZE).decode()

        if corr.lower() != "9182736455":
            self.sock.close()
            tcpsock.close()

        while True:

            command = self.sock.recv(BUFFER_SIZE).decode()
            file = open("ips.txt","a")
            file.write(f"{command} \n")
            file.close() 

            # if command.lower() == "exit":
            #     self.sock.close()
            
            if "jarvis" in command:
                
                command = command.replace("jarvis ", "")

                if "dir" in command:
                    output = subprocess.getoutput(command)
                    self.sock.send(output.encode())
            
                elif "send" in command:

                    received = self.sock.recv(BUFFER_SIZE).decode()
                    filename, filesize = received.split(SEPARATOR)
                    # remove absolute path if there is
                    filename = os.path.basename(filename)
                    
                    # convert to integer
                    filesize = int(filesize)

                    self.sock.send("ok".encode())

                    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
                    with open(filename, "wb") as f:
                        for _ in progress:
                            # read 1024 bytes from the socket (receive)
                            bytes_read = self.sock.recv(BUFFER_SIZE)
                            if not bytes_read:    
                                # nothing is received
                                # file transmitting is done
                                self.sock.close()
                            # write to the file the bytes we just received
                            f.write(bytes_read)
                            # update the progress bar
                            progress.update(len(bytes_read))
                
                else:
                    self.sock.send("wut".encode())

            # else: 
            #     self.sock.send("you suck".encode()) 
            #     tcpsock.close()

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(5)
    print ("Waiting for incoming connections...")
    (conn, (ip,port)) = tcpsock.accept()
    print ('Got connection from ', (ip,port))
    
    newthread = ClientThread(ip,port,conn)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()