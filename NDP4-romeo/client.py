# Romeo Tim-Louangphixai, Chad Abboud, Brendan Pham
# Network Design: Principles, Protocols & Applications
# Programming Project Phase 3: Implement RDT 2.2 over an unreliable UDP channel with bit-errors

# This file is for the creation and management of the UDP Client

from socket import *
import hashlib
from bit_error_simulation import introduce_bit_error
import time
import random

SERVER_ADDRESS = 'localhost'
SERVER_PORT = 12001
TIMEOUT = 2.0  # Adjusted timeout to 2 seconds to give more time for processing and avoid unnecessary resends
SEQUENCE_SIZE = 4
PACKET_SIZE = 1024

# Adjust these rates based on the scenario testing
DATA_PACKET_LOSS_RATE = 0.1
DATA_PACKET_BIT_ERROR_RATE = 0.05


def calculate_checksum(data):
    return hashlib.md5(data).digest()


def create_packet(seq_num, data):
    seq_num_bytes = seq_num.to_bytes(SEQUENCE_SIZE, byteorder='big')
    checksum = calculate_checksum(seq_num_bytes + data)
    return seq_num_bytes + checksum + data


def send_rdt_packets():
    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.settimeout(TIMEOUT)

    file_path = r'C:\Users\romeo\Desktop\gojira.jpg'  # Ensure this path is correct
    seq_num = 0

    with open(file_path, "rb") as file:
        while True:
            data = file.read(PACKET_SIZE)
            if not data:
                break  # End of file

            # Simulate packet loss or bit errors before creating the packet
            if random.random() >= DATA_PACKET_LOSS_RATE:
                packet = create_packet(seq_num, data)
                if random.random() < DATA_PACKET_BIT_ERROR_RATE:
                    packet = introduce_bit_error(packet, DATA_PACKET_BIT_ERROR_RATE)

                client_socket.sendto(packet, (SERVER_ADDRESS, SERVER_PORT))
                print(f"Packet {seq_num} sent, waiting for ACK...")

                try:
                    ack_packet, _ = client_socket.recvfrom(SEQUENCE_SIZE)
                    ack_seq_num = int.from_bytes(ack_packet, byteorder='big')
                    if ack_seq_num == seq_num:
                        print("ACK received, moving to the next packet.")
                        seq_num += 1  # Proceed to the next packet only after receiving the correct ACK
                    else:
                        print(
                            f"Received out-of-order ACK: {ack_seq_num}, expected: {seq_num}. Resending packet {seq_num}.")
                        # If out-of-order ACK is received, the packet will be resent in the next loop iteration
                except timeout:
                    print(f"Timeout, resending packet {seq_num}...")
            else:
                print(f"Simulating data packet loss for packet {seq_num}. Skipping send.")

    client_socket.close()
    print("File transfer completed.")


if __name__ == "__main__":
    send_rdt_packets()
