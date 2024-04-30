import socket
import time
import random

# Define server address and port
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 12001

# Timeout and packet sizes
TIMEOUT = 0.1  # Timeout for ACK waiting
SEQUENCE_SIZE = 4
CHECKSUM_SIZE = 16
PACKET_SIZE = 1024
WINDOW_SIZE = 10  # Size of the sliding window

# Scenario settings for client
ACK_PACKET_BIT_ERROR_RATE = 0  # Bit error rate for ACK packets
ACK_PACKET_LOSS_RATE = 0  # Loss rate for ACK packets


# Function to calculate checksum
def calculate_checksum(data):
    s = sum(data)
    checksum_hex = hex(s & 0xffffffffffffffff)[2:].zfill(16)
    return checksum_hex.encode('utf-8')


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
        if len(corrupted_ack) <= SEQUENCE_SIZE + CHECKSUM_SIZE:
            break

        byte_index = random.randint(SEQUENCE_SIZE + CHECKSUM_SIZE, len(corrupted_ack) - 1)
        bit_index = random.randint(0, 7)
        corrupted_ack[byte_index] ^= (1 << bit_index)

    return bytes(corrupted_ack)


# Function to simulate ACK packet loss
def simulate_ack_packet_loss():
    return random.random() < ACK_PACKET_LOSS_RATE


# Function to send RDT packets using Go-Back-N protocol
def send_rdt_packets():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(TIMEOUT)

    file_path = r"C:\Users\Brendan's PP\Desktop\sample.jpg"  # Specify the file path
    window = []  # Initialize window buffer
    base = 0  # Initialize base of the window
    next_seq_num = 0  # Initialize next sequence number

    start_time = time.time()  # Start timer

    with open(file_path, "rb") as file:
        while True:
            # Send packets within the window
            while next_seq_num < base + WINDOW_SIZE:
                if next_seq_num < len(window):
                    packet = window[next_seq_num]
                else:
                    data = file.read(PACKET_SIZE)  # Read data from the file
                    if not data:
                        break  # End of file reached, exit loop
                    packet = create_packet(next_seq_num, data)
                    window.append(packet)
                client_socket.sendto(packet, (SERVER_ADDRESS, SERVER_PORT))  # Send packet to server
                print(f"Packet {next_seq_num} sent, waiting for ACK...")
                next_seq_num += 1

            try:
                ack_packet, _ = client_socket.recvfrom(SEQUENCE_SIZE + CHECKSUM_SIZE)  # Receive ACK packet

                # Simulate ACK bit-error
                ack_packet = introduce_ack_bit_errors(ack_packet, ACK_PACKET_BIT_ERROR_RATE)

                # Check for ACK packet loss
                if simulate_ack_packet_loss():
                    print(f"Simulating ACK packet loss for packet {base}.")
                    continue  # Skip processing this ACK packet

                ack_seq_num = int.from_bytes(ack_packet[:SEQUENCE_SIZE], byteorder='big')
                ack_checksum = ack_packet[SEQUENCE_SIZE:SEQUENCE_SIZE + CHECKSUM_SIZE]
                ack_data = ack_packet[SEQUENCE_SIZE + CHECKSUM_SIZE:]

                # Verify checksum
                if verify_checksum(ack_packet[:SEQUENCE_SIZE], ack_checksum, ack_data):
                    # Slide the window
                    while base < ack_seq_num + 1:
                        base += 1
                else:
                    print("Invalid ACK received. Discarding.")

            except socket.timeout:
                print("Timeout, resending packets...")
                next_seq_num = base
                continue  # Retry sending packets within the window

            if base == len(window):
                break  # Exit loop if all packets are acknowledged

    client_socket.close()  # Close the socket
    end_time = time.time()  # End timer

    print("File transfer completed.")
    print(f"Start Time: {time.strftime('%X', time.localtime(start_time))}")
    print(f"End Time: {time.strftime('%X', time.localtime(end_time))}")
    print(f"Time Taken: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    send_rdt_packets()  # Call the send_rdt_packets function when the script is executed
