# Romeo Tim-Louangphixai, Chad Abboud, Brendan Pham
# Student ID: 01819835
# Network Design: Principles, Protocols & Applications
# Programming Project Phase 2: UDP Client and Server --> : Implement RDT 1.0 over a reliable UDP channel

# This file if for the creation and management of the UDP Server

# importing socket library


# creating server and defining parameters --> I am using a function to create this server in which would be called onto
# for organization and for possible need to edit future server name and port number easier
# to start server all you would have to do is call function define the value of server_pport

# ************************************* Phase 2 Comments will start at a double tab ***********************************

# Phase 2 UDP Server Changes:
# * Phase 2 it will Receive data packets from the UDP Client
# * Wrote these packets to a BMP file to reconstruct the original file
# * Remove any logic related to sending responses back to the client as RDT 1.0 operates under  the assumption of a reliable channel

# *********************************************************************************************


# Importing necessary libraries
from socket import *
import os


def start_udp_server(server_port, directory_path):
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(('', server_port))
    print("The UDP server is now ready to receive!\n")

    # Ensure directory_path is correctly handled
    if not os.path.isdir(directory_path):
        print(f"The provided directory path does not exist: {directory_path}")
        return

    output_file_path = os.path.join(directory_path, 'output.bmp')

    with open(output_file_path, "wb") as file:
        while True:
            packet, client_address = server_socket.recvfrom(1024)

            # Check for the end of file marker
            if packet.decode('utf-8', errors='ignore') == "EOF":
                break

            file.write(packet)

    server_socket.close()
    print("File received and written successfully.")


if __name__ == "__main__":
    port = 12000
    directory_path = input(
        'What is the directory path you would like to create and receive the BMP file being transferred: ')
    start_udp_server(port, directory_path)

# Sources Used:
# [1] Vinod Vokkarane, "Socket Programming 101 in Python," shared on UML blackboard site for course EECE.4820, Online, Jan 16, 2024, unpublished.
# [2] J. F. Kurose and K. W. Ross, Computer Networking: A Top-down Approach (7th Ed.). Boston: Pearson, 2017.
