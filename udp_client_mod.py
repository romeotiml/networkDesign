# Romeo Tim-Louangphixai, Chad Abboud, Brendan Pham
# Student ID: 01819835
# Network Design: Principles, Protocols & Applications
# Programming Project Phase 2: UDP Client and Server -->: Implement RDT 1.0 over a reliable UDP channel

#This file if for the creation and managment of the UDP Client

#importing socket library
from socket import *

#Creating function for message to be sent from the UDP client
#Define parameters

        #******************************************************* Phase 2 Comments will start at a double tab ************************************************

        # Phase 2 UDP Changes:
        # * Phase 2 UDP Client will need to read the BMP file in chucks
        # * Send each chunk as a UDP Packet to the server
        # * RDT 1.0 assumes that every packet sent is received in order. There is no need for a packet to requested to be re-sent

        #***************************************************************************************************************************************************

        # make_packet function definition
        # function will take the image file and break it down to several fixed packet size

def make_packet(file, packet_size = 1024):

    #Needs to read the file and allocate packet data at a fixed size
    while True: #this will start the loop, and until keeping going until it is broken
        data = file.read(packet_size)
        if not data: #will check if data is empty --> after the entire file has been read file.read(packet_size) should return a empty byte and then break
            break
        yield data #works like return but it will call data without ending the function entirely

        #Changing function name to best match UDP file being sent

def send_udp_file(server_name, server_port, file): #fxn name chance to file instead of message
    client_socket = socket(AF_INET, SOCK_DGRAM)

    #Attempt to open the file in binary mode --> "rb" will be able to set in binary mode
    with open(file_path, "rb") as file:
        #Start to Read and Send the file in packets
        for packet in make_packet(file): #utilizes make_packet function file chunks and yields these chunk one bby one
            client_socket.sendto(packet, (server_name, server_port)) #for each packet yielded send to the specified server.

        #Close the Socket
        client_socket.close() #After all the packet is sent, socket must be closed and will free up system resources.


# Example usage
if __name__ == "__main__":
    server = 'localhost'  # We are using 'hostname' possibly would have to change for future use
    port = 12000  # We are using 12000 would have to change if different one is used
    file_path = input('Enter the path of the BMP file you wish to send: ') #instead of making a specified address this will allow the user to send whatever BMP file if multiple need to be sent, but they can just copy and past the path
    send_udp_file(server,port,file_path)

#Sources
#[1] Vinod Vokkarane, "Socket Programming 101 in Python," shared on UML blackboard site for course EECE.4820, Online, Jan 16, 2024, unpublished.

