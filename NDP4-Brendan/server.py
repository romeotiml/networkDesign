# Romeo Tim-Louangphixai, Chad Abboud, Brendan Pham
# Network Design: Principles, Protocols & Applications
# Programming Project Phase 4: Implement RDT 3.0 over an unreliable UDP channel with bit-errors and loss


# This file is for the creation and management of the UDP Server

from socket import *
import os
import random

SERVER_PORT = 12001
SEQUENCE_SIZE = 4
CHECKSUM_SIZE = 16
WINDOW_SIZE = 5  # Adjust window size as needed

# Scenario settings for server
DATA_PACKET_BIT_ERROR_RATE = 0  # Bit error rate for data packets
DATA_PACKET_LOSS_RATE = 0  # Loss rate for data packets


# Function to calculate checksum
def calculate_checksum(data):
    s = 0
    for byte in data:
        s += byte  # Sum up the byte values
    checksum_hex = hex(s & 0xffffffffffffffff)[2:].zfill(16)
    return checksum_hex.encode('utf-8')  # Convert the hexadecimal string to bytes


# Function to verify checksum
def verify_checksum(seq_num_bytes, received_checksum, data):
    calculated_checksum = calculate_checksum(seq_num_bytes + data)
    return calculated_checksum == received_checksum


# Function to simulate data packet bit errors
def introduce_data_packet_bit_errors(data_packet, error_rate):
    if random.random() < error_rate:
        byte_index = random.randint(SEQUENCE_SIZE + CHECKSUM_SIZE, len(data_packet) - 1)
        bit_index = random.randint(0, 7)  # Select a random bit position within the byte
        corrupted_byte = data_packet[byte_index] ^ (1 << bit_index)  # Flip the selected bit
        data_packet = data_packet[:byte_index] + bytes([corrupted_byte]) + data_packet[byte_index + 1:]
    return data_packet


# Function to start UDP server
def start_udp_server(port=SERVER_PORT):
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(('', port))
    print(f"Server listening on port {port}.")

    output_directory = r'C:\Users\brend\Desktop'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file_path = os.path.join(output_directory, 'output.jpg')

    window_start = 0
    window_end = WINDOW_SIZE - 1
    packet_buffer = {}

    with open(output_file_path, 'wb') as file:
        print("Ready to receive data...")
        while True:
            packet, client_address = server_socket.recvfrom(2048)
            if random.random() < DATA_PACKET_LOSS_RATE:
                print("Simulating data packet loss.")
                continue  # Skip processing this packet to simulate loss

            seq_num_bytes = packet[:SEQUENCE_SIZE]
            received_checksum = packet[SEQUENCE_SIZE:SEQUENCE_SIZE + CHECKSUM_SIZE]
            data = packet[SEQUENCE_SIZE + CHECKSUM_SIZE:]
            seq_num = int.from_bytes(seq_num_bytes, byteorder='big')

            # Simulate data packet bit-error
            data = introduce_data_packet_bit_errors(data, DATA_PACKET_BIT_ERROR_RATE)

            if verify_checksum(seq_num_bytes, received_checksum, data):
                if window_start <= seq_num <= window_end:
                    packet_buffer[seq_num] = data
                    server_socket.sendto(seq_num_bytes, client_address)

                    while window_start in packet_buffer:
                        next_data = packet_buffer.pop(window_start)
                        file.write(next_data)
                        window_start += 1
                        window_end += 1

                    if seq_num == window_start:
                        window_start += 1
                        window_end += 1
                        server_socket.sendto(seq_num.to_bytes(SEQUENCE_SIZE, byteorder='big'), client_address)
                elif seq_num < window_start:
                    server_socket.sendto((window_start - 1).to_bytes(SEQUENCE_SIZE, byteorder='big'), client_address)
                else:
                    server_socket.sendto(window_end.to_bytes(SEQUENCE_SIZE, byteorder='big'), client_address)
            else:
                print(f"Checksum mismatch for packet {seq_num}. Packet discarded.")

    server_socket.close()
    print("Server shutdown.")


if __name__ == "__main__":
    start_udp_server()
