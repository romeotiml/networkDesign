# Romeo Tim-Louangphixai, Chad Abboud, Brendan Pham
# Network Design: Principles, Protocols & Applications
# Programming Project Phase 4: Implement RDT 3.0 over an unreliable UDP channel with bit-errors and loss


# This file is for the creation and management of the UDP Client

from socket import *
import hashlib
from bit_error_simulation import introduce_bit_error
import time
import random

SERVER_ADDRESS = 'localhost'
SERVER_PORT = 12001
TIMEOUT = 0.05  # Timeout for ACK waiting
SEQUENCE_SIZE = 4
CHECKSUM_SIZE = 16
PACKET_SIZE = 1024
LOSS_SIMULATION_RATE = 0.1  # Chance to simulate packet loss

# Scenario settings
ACK_PACKET_BIT_ERROR_RATE = 0.05
DATA_PACKET_BIT_ERROR_RATE = 0.05
ACK_PACKET_LOSS_RATE = 0.1
DATA_PACKET_LOSS_RATE = 0.1


def calculate_checksum(data):
    return hashlib.md5(data).digest()


def create_packet(seq_num, data):
    seq_num_bytes = seq_num.to_bytes(SEQUENCE_SIZE, byteorder='big')
    checksum = calculate_checksum(seq_num_bytes + data)
    return seq_num_bytes + checksum + data


def send_rdt_packets():
    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.settimeout(TIMEOUT)

    file_path = r'C:\Users\romeo\Desktop\gojira.jpg'  # Update this with your actual image path
    seq_num = 0

    start_time = time.time()  # Start timer

    with open(file_path, "rb") as file:
        while True:
            data = file.read(PACKET_SIZE)
            if not data:
                break
            packet = create_packet(seq_num, data)

            # Simulate data packet loss
            if random.random() < DATA_PACKET_LOSS_RATE:
                print(f"Simulating data packet loss for packet {seq_num}.")
                continue

            # Simulate data packet bit-error
            if random.random() < DATA_PACKET_BIT_ERROR_RATE:
                packet = introduce_bit_error(packet, DATA_PACKET_BIT_ERROR_RATE)

            retry_count = 0
            while retry_count < 3:
                client_socket.sendto(packet, (SERVER_ADDRESS, SERVER_PORT))
                print(f"Packet {seq_num} sent, waiting for ACK...")

                try:
                    ack_packet, _ = client_socket.recvfrom(SEQUENCE_SIZE + CHECKSUM_SIZE)
                    ack_seq_num = int.from_bytes(ack_packet[:SEQUENCE_SIZE], byteorder='big')

                    # Simulate ACK packet bit-error
                    if random.random() < ACK_PACKET_BIT_ERROR_RATE:
                        ack_packet = introduce_bit_error(ack_packet, ACK_PACKET_BIT_ERROR_RATE)

                    # Simulate ACK packet loss
                    if random.random() < ACK_PACKET_LOSS_RATE:
                        print(f"Simulating ACK loss for packet {seq_num}.")
                        raise timeout

                    if ack_seq_num == seq_num:
                        print("ACK received, moving to the next packet.")
                        seq_num += 1
                        break
                    else:
                        print(f"Received out of order ACK: {ack_seq_num}, expected: {seq_num}")
                except timeout:
                    print(f"Timeout, resending packet {seq_num}...")
                    retry_count += 1

    client_socket.close()
    end_time = time.time()  # End timer

    print("File transfer completed.")
    print(f"Start Time: {time.strftime('%X', time.localtime(start_time))}")
    print(f"End Time: {time.strftime('%X', time.localtime(end_time))}")
    print(f"Time Taken: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    send_rdt_packets()
