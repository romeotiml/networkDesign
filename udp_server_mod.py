# Romeo Tim-Louangphixai, Chad Abboud, Brendan Pham
# Student ID: 01819835
# Network Design: Principles, Protocols & Applications
# Programming Project Phase 2: UDP CLient and Server --> : Implement RDT 1.0 over a reliable UDP channel

#This file if for the creation and managment of the UDP Server

#importing socket library
from socket import *

#creating server and defining parameters --> I am using a function to create this server in which would be called onto
#for organization and for possible need to edit future server name and port number easier
#to start server all you would have to do is call function define the value of server_pport

#******************************************************* Phase 2 Comments will start at a double tab ************************************************

        # Phase 2 UDP Server Changes:
        # * Phase 2 it will Recieve data packets from the UDP Client
        # * Wrote these packets to a BMP file to reconstruct the original file
        # * Remove any logic related to sending responses back to the client as RDT 1.0 operates under  the assumption of a reliable channel

        #*********************************************************************************************
def start_udp_server(server_port, file_path):       #adding additional parameter file_path
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(('', server_port))
    print("The UDP is established now the server is ready to receive!\n")

    # We need to create a output.bmp file so that will be able to write the file with the data from client
    file_path = file_path = directory_path + '\\output.bmp'

        #Needs to open the file for writing in Binary Mode --> "wb" will open a file for writing in binary  mode
    with open(file_path, "wb") as file: # -> writing to the variable file
        while True: # start loop
            packet, client_address = server_socket.recvfrom(1024) #server waits for data to arrive, receives up too 2048 bytes of data from the client
            #NOTE: in the textbook the use function calls like extract(packet) and deliver_data
                ## when you receive a packet using the recvfrom() method, the data you receive is essentially the result of the extract() operation.
                ###. When you write the received packet to a file (file.write(packet)), you are delivering the data to its final destination (the file), so it serves the deliver_data(data) function

            if not packet: #Will check is the recived message is empty this is a sign that there is no more data needed to be sent.
                break
            file.write(packet)

    server_socket.close() #close the socket


#Example usage
if __name__ == "__main__":
    port = 12000
    directory_path = input('What is the directory path you would like the create and recieve the BMP file being transferred:')
    start_udp_server(port, directory_path)

#Sources Used:
# [1] Vinod Vokkarane, "Socket Programming 101 in Python," shared on UML blackboard site for course EECE.4820, Online, Jan 16, 2024, unpublished.
