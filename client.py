'''
Nick Jenkins
June 08, 2022
EE 419, University of Washington
Final Project
client.py

I worked individually, so all work is my own.

client.py is the client handler for the TCP-based chat application. It connects to the TCP server to receive and send messages

connection_init(): creates the client socket with user-input IP and port, connects to server,
 asks user about username, sends to server

message_handling(): prints messages from other users

input_handling(): sends user messages with their username concatenated
'''

from socket import *
import threading
from time import sleep

class Client:
    def connection_init():
        # get user-input ip and port
        ip = input("IP address: ")
        port = input("Port number: ")

        # build TCP socket
        global clientSocket
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((ip, int(port)))
        print("Connection to " + ip + " on port " + port + " successful.")

        # get a username
        global username 
        username = input("Please enter your username: ")

        # send a welcome message
        clientSocket.send((username + " has joined the server. Welcome!").encode())

        # thread for message_handling
        messageHandling = threading.Thread(target = Client.message_handling)
        messageHandling.start()

        # thread for input_handling
        inputHandling = threading.Thread(target = Client.input_handling)
        inputHandling.start()

    def message_handling():
        # global var for killing threads
        global kill
        kill = 0

        # loop forever
        while True:
            # take in a message
            msg = input("Enter message (or 'end' to close): ")
            # if the 'end' message is sent, close the socket
            if (msg == 'end'):
                # let the server know client is leaving
                clientSocket.send(("{} has left.".format(username)).encode())
                clientSocket.send("end".encode())
                # kill input thread and wait a bit to allow thread to finish
                kill = 1
                sleep(1)
                # close socket
                clientSocket.close()
                # kill this thread
                break
            else:
                # format message with username
                msg = "{}: {}".format(username, msg)
                # send message to server
                clientSocket.send(msg.encode())

    def input_handling():
        # loop forever
        while True:
            # if killed, close thread
            if kill:
                break
            # receive and print messages from server
            recv_msg = clientSocket.recv(1024).decode()
            print(recv_msg)

# initialize connection
Client.connection_init()