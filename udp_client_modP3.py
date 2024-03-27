# Romeo Tim-Louangphixai, Chad Abboud, Brendan Pham
# Network Design: Principles, Protocols & Applications
# Programming Project Phase 3: Implement RDT 2.2 over an unreliable UDP channel with bit-errors

# This file is for the creation and management of the UDP Client

# Importing socket library
from socket import *
import hashlib

# Constants
SEQUENCE_SIZE = 32  # Size of the sequence number in bits
PACKET_SIZE = 1024  # Packet size in bytes

# Function to create RDT 2.2 packet
def create_packet(seq_num, data):
    seq_num_bytes = seq_num.to_bytes(SEQUENCE_SIZE // 8, 'big')
    checksum = calculate_checksum(seq_num_bytes + data)
    return seq_num_bytes + checksum + data

# Function to calculate checksum using MD5 hashing
def calculate_checksum(data):
    hash_object = hashlib.md5()
    hash_object.update(data)
    checksum = hash_object.digest()
    return checksum

# Function to send UDP file using RDT 2.2 protocol
def send_rdt_packets(server_name, server_port, file_path):
    client_socket = socket(AF_INET, SOCK_DGRAM)
    with open(file_path, "rb") as file:
        seq_num = 0
        for packet_data in make_packet(file):
            rdt_packet = create_packet(seq_num, packet_data)
            client_socket.sendto(rdt_packet, (server_name, server_port))
            seq_num = (seq_num + 1) % (2 ** SEQUENCE_SIZE)

        # Send end-of-file marker
        eof_marker = create_packet(seq_num, b"EOF")
        client_socket.sendto(eof_marker, (server_name, server_port))

    client_socket.close()

# Function to break file into fixed-sized packets
def make_packet(file, packet_size=PACKET_SIZE):
    while True:
        data = file.read(packet_size)
        if not data:
            break
        yield data

if __name__ == "__main__":
    server = 'localhost'
    port = 12001
    file_path = input('Enter the path of the JPEG file you wish to send: ')
    send_rdt_packets(server, port, file_path)
