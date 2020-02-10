import socket, threading
class ClientThread(threading.Thread):
    
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print ("New connection added: ", clientAddress)
    
    def run(self):
        print ("Connection from : ", clientAddress)
        #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        msg = ''
        while True:
            data = self.csocket.recv(2048)
            msg = data.decode()
            if msg=='bye':
              break
            print ("from client", msg)
            self.csocket.send(bytes(msg,'UTF-8'))
        print ("Client at ", clientAddress , " disconnected...")

LOCALHOST = "0.0.0.0"
PORT = 3847
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
while True:
    server.listen(5)
    client_socket, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, client_socket)
    newthread.start()

    file = open("ips.txt","a")
    file.write(f"{clientAddress}:{client_socket} \n")
    file.close()

    message = "Hello and Welcome".encode()
    client_socket.send(message)