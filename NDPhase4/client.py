from socket import *
import hashlib
import os
import random
import time

SERVER_ADDRESS = 'localhost'
SERVER_PORT = 12001
TIMEOUT = 5  # seconds
RETRY_LIMIT = 20
SEQUENCE_SIZE = 4  # bytes for sequence number
CHECKSUM_SIZE = 16  # bytes for checksum (MD5 produces 16 bytes)
PACKET_SIZE = 1024  # bytes for data part of the packet
WINDOW_SIZE = 4  # window size for sliding window protocol

def calculate_checksum(data):
    return hashlib.md5(data).digest()

def create_packet(seq_num, data):
    seq_num_bytes = seq_num.to_bytes(SEQUENCE_SIZE, byteorder='big')
    checksum = calculate_checksum(seq_num_bytes + data)
    return seq_num_bytes + checksum + data

def introduce_bit_error(data_bytes, error_rate=0.02):
    import numpy as np
    if error_rate <= 0:
        return data_bytes
    new_data = bytearray(data_bytes)
    for i in range(len(new_data)):
        if np.random.random() < error_rate:
            bit_to_flip = 1 << np.random.randint(0, 8)  # Choose a random bit to flip
            new_data[i] ^= bit_to_flip  # XOR to flip the chosen bit
    return bytes(new_data)

def send_rdt_packets():
    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.settimeout(TIMEOUT)

    file_path = r"C:\Users\Brendan's PP\Desktop\GT3_510.jpg"
    error_rate = 0.02
    seq_num = 0
    retries = 0

    send_window = []  # Maintain a send window for packets
    ack_expected = 0  # Sequence number of the next expected ACK

    with open(file_path, "rb") as file:
        while True:
            # Fill the send window with new packets
            while len(send_window) < WINDOW_SIZE:
                data = file.read(PACKET_SIZE)
                if not data:
                    break  # End of file
                packet_without_error = create_packet(seq_num, data)

                # Introduce bit errors based on a random decision
                error_chance = 0.20  # 20% chance of error occurrence
                if random.random() < error_chance:
                    packet_with_error = introduce_bit_error(packet_without_error, error_rate)
                    print(f"Introducing errors to packet {seq_num}.")
                    send_window.append((seq_num, packet_with_error))
                else:
                    send_window.append((seq_num, packet_without_error))
                seq_num += 1  # Increment sequence number

            # Send packets in the send window
            for packet_info in send_window:
                client_socket.sendto(packet_info[1], (SERVER_ADDRESS, SERVER_PORT))
                print(f"Packet {packet_info[0]} sent, waiting for ACK...")

            # Handle ACKs and timeouts
            start_time = time.time()
            while True:
                try:
                    ack_packet, _ = client_socket.recvfrom(1024)
                    ack_seq_num = int.from_bytes(ack_packet[:SEQUENCE_SIZE], byteorder='big')
                    print(f"ACK {ack_seq_num} received.")
                    if ack_seq_num >= ack_expected:
                        # Remove acknowledged packets from the send window
                        send_window = [packet for packet in send_window if packet[0] > ack_seq_num]
                        ack_expected = ack_seq_num + 1  # Update expected ACK
                    if not send_window:
                        break  # All packets in window acknowledged
                except timeout:
                    retries += 1
                    if retries >= RETRY_LIMIT:
                        print("Max retries reached. Giving up.")
                        return
                    else:
                        print(f"Timeout, resending packets in window... (Retry {retries})")
                        break  # Retry sending packets in window

                # Check timeout for entire send window
                if time.time() - start_time > TIMEOUT:
                    print("Timeout for entire send window. Resending window...")
                    break  # Retry sending entire window

    client_socket.close()
    print("File transfer completed.")

if __name__ == "__main__":
    send_rdt_packets()
