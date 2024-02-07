# Romeo Tim-Louangphixai
# Student ID: 01819835
# Network Design: Principles, Protocols & Applications
# Programming Project Phase 1: UDP CLient and Server

#This file if for the creation and managment of the UDP Server

#importing socket library
from socket import *

#creating server and defining parameters --> I am using a function to create this server in which would be called onto
#for organization and for possible need to edit future server name and port number easier
#to start server all you would have to do is call function define the value of server_pport
def start_udp_server(server_port):
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(('', server_port))
    print("The UDP is established now the server is ready to recieve!\n")

#Estsablishes how server socket is recieving data --> 2048 is max amount of data to be received at once in bytes
    while True:
        message, client_address = server_socket.recvfrom(2048)
        modified_message = message.decode()
        print(f"Received message: {modified_message} from {client_address}") # f allows you to include the values of variables directly within the string.

        #Echoing back the recieved message
        server_socket.sendto(modified_message.encode(), client_address)

#Calling Function with defined port number
start_udp_server(12000)


#Sources Used:
# [1] Vinod Vokkarane, "Socket Programming 101 in Python," shared on UML blackboard site for course EECE.4820, Online, Jan 16, 2024, unpublished.