# Romeo Tim-Louangphixai, Chad Abboud, Brendan Pham
# Network Design: Principles, Protocols & Applications
# Programming Project Phase 4: Implement RDT 3.0 over an unreliable UDP channel with bit-errors and loss

# This file is for the creation and management of the UDP server

from socket import *
import hashlib
import os
import random

SERVER_PORT = 12001
SEQUENCE_SIZE = 4
CHECKSUM_SIZE = 16

# Scenario settings
ACK_PACKET_BIT_ERROR_RATE = 0.05
DATA_PACKET_BIT_ERROR_RATE = 0.05
ACK_PACKET_LOSS_RATE = 0.1
DATA_PACKET_LOSS_RATE = 0.1

def calculate_checksum(data):
    return hashlib.md5(data).digest()

def start_udp_server(port=SERVER_PORT):
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(('', port))
    print(f"Server listening on port {port}.")

    output_directory = r'C:\Users\romeo\Desktop'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file_path = os.path.join(output_directory, 'output.jpg')

    packet_buffer = {}
    expected_seq_num = 0

    with open(output_file_path, 'wb') as file:
        print("Ready to receive data...")
        while True:
            packet, client_address = server_socket.recvfrom(2048)
            if random.random() < DATA_PACKET_LOSS_RATE:
                print("Simulating data packet loss.")
                continue  # Skip processing this packet to simulate loss

            seq_num_bytes = packet[:SEQUENCE_SIZE]
            received_checksum = packet[SEQUENCE_SIZE:SEQUENCE_SIZE+CHECKSUM_SIZE]
            data = packet[SEQUENCE_SIZE+CHECKSUM_SIZE:]
            seq_num = int.from_bytes(seq_num_bytes, byteorder='big')

            calculated_checksum = calculate_checksum(seq_num_bytes + data)
            if calculated_checksum == received_checksum:
                if seq_num == expected_seq_num or seq_num in packet_buffer:
                    file.write(data)
                    server_socket.sendto(seq_num_bytes, client_address)
                    expected_seq_num += 1

                    while expected_seq_num in packet_buffer:
                        data = packet_buffer.pop(expected_seq_num)
                        file.write(data)
                        expected_seq_num += 1
                else:
                    packet_buffer[seq_num] = data
            else:
                print(f"Checksum mismatch for packet {seq_num}. Packet discarded.")

    server_socket.close()
    print("Server shutdown.")

if __name__ == "__main__":
    start_udp_server()
