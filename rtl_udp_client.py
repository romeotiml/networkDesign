# Romeo Tim-Louangphixai
# Student ID: 01819835
# Network Design: Principles, Protocols & Applications
# Programming Project Phase 1: UDP Client and Server

#This file if for the creation and managment of the UDP Client

#importing socket library
from socket import *

#Creating function for message to be sent from the UDP client
#Define parameters
def send_udp_message(server_name, server_port, message):
    client_socket = socket(AF_INET, SOCK_DGRAM)
    try: #error handling attempt to send messahe
        # Send the message
        client_socket.sendto(message.encode(), (server_name, server_port))

        # Receive a response
        modified_message, server_address = client_socket.recvfrom(2048)
        print(modified_message.decode())

    finally: #runs whether or not message is sent
        # Close the socket
        client_socket.close()


# Example usage
if __name__ == "__main__":
    server = 'localhost'  # We are using 'hostname' possibly would have to change for future use
    port = 12000  # We are using 12000 would have to change if different one is used
    message = input('Enter your message:')  # Python 3.x use input()
    send_udp_message(server, port, message)

#Sources
#[1] Vinod Vokkarane, "Socket Programming 101 in Python," shared on UML blackboard site for course EECE.4820, Online, Jan 16, 2024, unpublished.
