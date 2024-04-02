# Romeo Tim-Louangphixai, Chad Abboud, Brendan Pham
# Network Design: Principles, Protocols & Applications
# Programming Project Phase 4: Implement RDT 3.0 over an unreliable UDP channel with bit-errors and loss


# This file is for the creation and management of the UDP Client

# Import necessary modules
import socket
import time
import random

# Define server address and port
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 12001

# Timeout and packet sizes
TIMEOUT = 0.05  # Timeout for ACK waiting
SEQUENCE_SIZE = 4
CHECKSUM_SIZE = 16
PACKET_SIZE = 1024

# Scenario settings for client
ACK_PACKET_BIT_ERROR_RATE = 0  # Bit error rate for ACK packets
ACK_PACKET_LOSS_RATE = 0  # Loss rate for ACK packets


# Function to calculate checksum
def calculate_checksum(data):
    # Initialize checksum sum
    s = 0
    # Iterate through data bytes and sum up their values
    for byte in data:
        s += byte
    # Convert the sum to a 16-byte hexadecimal string
    checksum_hex = hex(s & 0xffffffffffffffff)[2:].zfill(16)
    return checksum_hex.encode('utf-8')  # Convert the hexadecimal string to bytes


# Function to verify checksum
def verify_checksum(seq_num_bytes, received_checksum, data):
    calculated_checksum = calculate_checksum(seq_num_bytes + data)
    return calculated_checksum == received_checksum


# Function to create packet
def create_packet(seq_num, data):
    seq_num_bytes = seq_num.to_bytes(SEQUENCE_SIZE, byteorder='big')
    checksum = calculate_checksum(seq_num_bytes + data)
    return seq_num_bytes + checksum + data


# Function to introduce bit errors in ACK packet
def introduce_ack_bit_errors(ack_packet, error_rate=0.01):
    if error_rate <= 0:
        return ack_packet

    num_errors = int(error_rate * len(ack_packet))
    if num_errors <= 0:
        return ack_packet

    corrupted_ack = bytearray(ack_packet)

    for _ in range(num_errors):
        # Check if the length of the packet is greater than the sum of sequence size and checksum size
        if len(corrupted_ack) <= SEQUENCE_SIZE + CHECKSUM_SIZE:
            break  # Exit the loop if the packet size is too small

        byte_index = random.randint(SEQUENCE_SIZE + CHECKSUM_SIZE, len(corrupted_ack) - 1)
        bit_index = random.randint(0, 7)  # Select a random bit position within the byte
        corrupted_ack[byte_index] ^= (1 << bit_index)  # Flip the selected bit

    return bytes(corrupted_ack)


# Function to simulate ACK packet loss
def simulate_ack_packet_loss():
    return random.random() < ACK_PACKET_LOSS_RATE


# Function to send RDT packets
def send_rdt_packets():
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(TIMEOUT)  # Set socket timeout

    file_path = r'C:\Users\brend\Desktop\sample.jpg'  # Specify the file path
    seq_num = 0  # Initialize sequence number
    max_retries = 15  # Maximum number of retries for each packet

    start_time = time.time()  # Start timer

    # Open the file in binary read mode
    with open(file_path, "rb") as file:
        while True:
            data = file.read(PACKET_SIZE)  # Read data from the file
            if not data:
                break  # End of file reached, exit loop

            # Create packet
            packet = create_packet(seq_num, data)

            retry_count = 0  # Initialize retry count
            while retry_count < max_retries:
                client_socket.sendto(packet, (SERVER_ADDRESS, SERVER_PORT))  # Send packet to server
                print(f"Packet {seq_num} sent, waiting for ACK...")

                try:
                    ack_packet, _ = client_socket.recvfrom(SEQUENCE_SIZE + CHECKSUM_SIZE)  # Receive ACK packet

                    # Simulate ACK bit-error
                    ack_packet = introduce_ack_bit_errors(ack_packet, ACK_PACKET_BIT_ERROR_RATE)

                    # Check for ACK packet loss
                    if simulate_ack_packet_loss():
                        print(f"Simulating ACK packet loss for packet {seq_num}.")
                        raise socket.timeout  # Simulate packet loss by raising timeout exception

                    ack_seq_num = int.from_bytes(ack_packet[:SEQUENCE_SIZE], byteorder='big')

                    if ack_seq_num == seq_num:
                        print("ACK received, moving to the next packet.")
                        seq_num += 1  # Move to the next sequence number
                        break  # Exit retry loop
                    else:
                        print(f"Received out of order ACK: {ack_seq_num}, expected: {seq_num}")
                except socket.timeout:
                    print(f"Timeout, resending packet {seq_num}...")
                    retry_count += 1  # Increment retry count
                    continue  # Retry sending the same packet

                retry_count = 0  # Reset retry count after successful transmission

    client_socket.close()  # Close the socket
    end_time = time.time()  # End timer

    print("File transfer completed.")
    print(f"Start Time: {time.strftime('%X', time.localtime(start_time))}")
    print(f"End Time: {time.strftime('%X', time.localtime(end_time))}")
    print(f"Time Taken: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    send_rdt_packets()  # Call the send_rdt_packets function when the script is executed
