# Romeo Tim-Louangphixai, Chad Abboud, Brendan Pham
# Network Design: Principles, Protocols & Applications
# Programming Project Phase 3: Implement RDT 2.2 over an unreliable UDP channel with bit-errors

# This file is for the creation and management of the UDP Client

from socket import *
import hashlib
from bit_error_simulation import introduce_bit_error
import time
import random  # Import the random module

SERVER_ADDRESS = 'localhost'
SERVER_PORT = 12001
TIMEOUT = 2  # seconds
RETRY_LIMIT = 5
SEQUENCE_SIZE = 4  # bytes for sequence number
CHECKSUM_SIZE = 16  # bytes for checksum (MD5 produces 16 bytes)
PACKET_SIZE = 1024  # bytes for data part of the packet

def calculate_checksum(data):
    return hashlib.md5(data).digest()

def create_packet(seq_num, data):
    seq_num_bytes = seq_num.to_bytes(SEQUENCE_SIZE, byteorder='big')
    checksum = calculate_checksum(seq_num_bytes + data)
    return seq_num_bytes + checksum + data

def send_rdt_packets():
    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.settimeout(TIMEOUT)

    file_path = r'C:\Users\romeo\Desktop\corgi.jpeg'
    error_rate = 0.02
    seq_num = 0

    with open(file_path, "rb") as file:
        while True:
            data = file.read(PACKET_SIZE)
            if not data:
                break  # End of file
            packet_without_error = create_packet(seq_num, data)

            #Introduce bit errors absed on a random deicsion

            # When deciding whether to introduce bit errors:
            error_chance = 0.20  # 20% chance. Change this to change percentage of error occurs

            if random.random() < error_chance:
                packet_with_error = introduce_bit_error(packet_without_error, error_rate)
                print(f"Introducing errors to packet {seq_num}.")
                client_socket.sendto(packet_with_error, (SERVER_ADDRESS, SERVER_PORT))
            else:
                client_socket.sendto(packet_without_error, (SERVER_ADDRESS, SERVER_PORT))

            print(f"Packet {seq_num} sent, waiting for ACK...")
            retries = 0

            while retries < RETRY_LIMIT:
                try:
                    ack_packet, _ = client_socket.recvfrom(1024)
                    print("ACK received.")
                    break  # Move to the next packet
                except timeout:
                    retries += 1
                    print(f"Timeout, resending packet {seq_num}... (Retry {retries})")
                    client_socket.sendto(packet_without_error, (SERVER_ADDRESS, SERVER_PORT))  # Use packet_without_error for resending

            if retries == RETRY_LIMIT:
                print("Max retries reached. Giving up.")
                break

            seq_num += 1  # Increment sequence number for the next packet

    client_socket.close()
    print("File transfer completed.")

if __name__ == "__main__":
    send_rdt_packets()
