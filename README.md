# basic-messaging
Final Project for EE 419, Computer Communication Networks, at UW

This was my final project for the above mentioned class. It involved using Python's `socket` library to create a basic messaging application with a client-server model.

`server.py` can be ran on any machine on the network and is the server for the TCP-based chat application. It receives and broadcasts client's message to all the other clients.

`client.py` is the client handler for the TCP-based chat application. It connects to the server to receive and send messages. Any number of clients can connect to the server as long as they are on the same network.

`server.py` must be initiated before any clients can connect.
