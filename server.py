'''
Nick Jenkins
June 08, 2022
EE 419, University of Washington
Final Project
server.py

server.py is the server for the TCP-based chat application
It receives and broadcasts client's message to all the other clients
Uses threading library to allow multiple connections

server_init(): initializes server TCP socket using user-input IP and port number,
 always listening, makes a list to maintain clients, accepts clients, relevant prints

broadcast(user_message): broadcasts a client's message to all other clients

client_handling(client_socket, client_address): receives messages from clients,
 when client joins server for first time, broadcast its name
'''

from socket import *
import threading
from time import sleep

class Server:
    global clientSockets
    clientSockets = set()

    def server_init():
        # get user-input ip and port
        ip = input("IP address: ")
        port = input("Port number: ")
        
        # build TCP socket
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.bind((ip, int(port)))
        serverSocket.listen(1)
        
        while True:
            # receive client socket
            clientSocket, clientAddr = serverSocket.accept()
            
            # add client to list
            clientSockets.add(clientSocket)

            # thread for client handling
            clientHandling = threading.Thread(target = Server.client_handling, args = (clientSocket, clientAddr))
            clientHandling.start() 
    
    def broadcast(user_message):
        # for all clients in list, send the message
        for i in clientSockets:
            i.send(user_message.encode())    

    def client_handling(client_socket, client_address):
        # kill var for ending thread
        kill = 0
        # loop forever
        while True:
            # end thread if kill
            if kill:
                break
            # receive message
            msg = client_socket.recv(1024).decode()
            # if message is 'end' message, kill thread, wait a bit, remove client from broadcast list, and close socket
            if msg == 'end':
                kill = 1
                sleep(1)
                clientSockets.remove(client_socket)
                client_socket.close()
                break
            # broadcast message to all clients
            else:
                Server.broadcast(msg)

# initialize server
Server.server_init()