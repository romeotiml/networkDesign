from socket import *
import hashlib
import os
import random

SERVER_PORT = 12001
SEQUENCE_SIZE = 4
CHECKSUM_SIZE = 16
WINDOW_SIZE = 5  # Adjust window size as needed

# Scenario settings
ACK_PACKET_BIT_ERROR_RATE = 0.05
DATA_PACKET_BIT_ERROR_RATE = 0.05
ACK_PACKET_LOSS_RATE = 0.1
DATA_PACKET_LOSS_RATE = 0.1

def calculate_checksum(data):
    return hashlib.md5(data).digest()

def verify_checksum(seq_num_bytes, received_checksum, data):
    calculated_checksum = calculate_checksum(seq_num_bytes + data)
    return calculated_checksum == received_checksum

def start_udp_server(port=SERVER_PORT):
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(('', port))
    print(f"Server listening on port {port}.")

    output_directory = r'C:\Users\brend\Desktop'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file_path = os.path.join(output_directory, 'output.jpg')

    expected_seq_num = 0
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

            if verify_checksum(seq_num_bytes, received_checksum, data):
                if seq_num >= window_start and seq_num <= window_end:
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
                        server_socket.sendto((seq_num).to_bytes(SEQUENCE_SIZE, byteorder='big'), client_address)
                elif seq_num < window_start:
                    server_socket.sendto((window_start - 1).to_bytes(SEQUENCE_SIZE, byteorder='big'), client_address)
                else:
                    server_socket.sendto((window_end).to_bytes(SEQUENCE_SIZE, byteorder='big'), client_address)
            else:
                print(f"Checksum mismatch for packet {seq_num}. Packet discarded.")

    server_socket.close()
    print("Server shutdown.")

if __name__ == "__main__":
    start_udp_server()
