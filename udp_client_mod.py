# Romeo Tim-Louangphixai, Chad Abboud, Brendan Pham
# Student ID: 01819835
# Network Design: Principles, Protocols & Applications
# Programming Project Phase 2: UDP Client and Server -->: Implement RDT 1.0 over a reliable UDP channel

# This file if for the creation and management of the UDP Client

# importing socket library
from socket import *

# Creating function for message to be sent from the UDP client
# Define parameters

# ************************************* Phase 2 Comments will start at a double tab ************************************

# Phase 2 UDP Changes:
# * Phase 2 UDP Client will need to read the BMP file in chucks
# * Send each chunk as a UDP Packet to the server
# * RDT 1.0 assumes that every packet sent is received in order.There is no need for a packet to requested to be re-sent

# **********************************************************************************************************************

# make_packet function definition
# function will take the image file and break it down to several fixed packet size


# Importing socket library

def make_packet(file, packet_size=1024):
    while True:
        data = file.read(packet_size)
        if not data:
            break
        yield data


def send_udp_file(server_name, server_port, file_path):
    client_socket = socket(AF_INET, SOCK_DGRAM)
    with open(file_path, "rb") as file:
        for packet in make_packet(file):
            client_socket.sendto(packet, (server_name, server_port))

        # Send a specific message to signal the end of the file transmission
        end_of_file_marker = "EOF".encode()  # Encoding the string "EOF" to bytes
        client_socket.sendto(end_of_file_marker, (server_name, server_port))

    client_socket.close()


if __name__ == "__main__":
    server = 'localhost'
    port = 12000
    file_path = input('Enter the path of the BMP file you wish to send: ')
    send_udp_file(server, port, file_path)


# Sources
# [1] Vinod Vokkarane, "Socket Programming 101 in Python," shared on UML blackboard site for course EECE.4820, Online, Jan 16, 2024, unpublished.
# [2] J. F. Kurose and K. W. Ross, Computer Networking: A Top-down Approach (7th Ed.). Boston: Pearson, 2017.
