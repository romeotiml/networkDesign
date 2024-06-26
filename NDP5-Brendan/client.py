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
    file_path = r"C:\Users\Brendan's PP\Desktop\sample.jpg"
    window = []
    base = 0
    next_seq_num = 0
    start_time = time.time()

    try:
        with open(file_path, "rb") as file:
            while True:
                while next_seq_num < base + WINDOW_SIZE:
                    if next_seq_num >= len(window):
                        data = file.read(PACKET_SIZE)
                        if not data:
                            break
                        packet = create_packet(next_seq_num, data)
                        window.append(packet)
                    client_socket.sendto(window[next_seq_num], (SERVER_ADDRESS, SERVER_PORT))
                    print(f"Sent packet {next_seq_num}, waiting for ACK...")
                    next_seq_num += 1

                if base == len(window):
                    break

                ack_packets = []
                while True:
                    try:
                        ack_packet, _ = client_socket.recvfrom(SEQUENCE_SIZE + CHECKSUM_SIZE)
                        ack_packets.append(ack_packet)
                    except socket.timeout:
                        break

                for ack_packet in ack_packets:
                    ack_packet = introduce_ack_bit_errors(ack_packet, ACK_PACKET_BIT_ERROR_RATE)
                    if simulate_ack_packet_loss():
                        print(f"ACK for packet {base} lost.")
                        continue

                    ack_seq_num = int.from_bytes(ack_packet[:SEQUENCE_SIZE], byteorder='big')
                    ack_checksum = ack_packet[SEQUENCE_SIZE:SEQUENCE_SIZE + CHECKSUM_SIZE]
                    ack_data = ack_packet[SEQUENCE_SIZE + CHECKSUM_SIZE:]

                    print(f"Received ACK for packet {ack_seq_num}. Verifying checksum...")

                    if verify_checksum(ack_packet[:SEQUENCE_SIZE], ack_checksum, ack_data):
                        while base < ack_seq_num + 1:
                            base += 1
                        print(f"ACK for packet {ack_seq_num} verified. Advancing base to {base}.")
                    else:
                        print("Invalid ACK received. Discarding.")

    except (socket.error, FileNotFoundError) as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()
        end_time = time.time()
        print("File transfer completed.")
        print(f"Start Time: {time.strftime('%X', time.localtime(start_time))}")
        print(f"End Time: {time.strftime('%X', time.localtime(end_time))}")
        print(f"Time Taken: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    send_rdt_packets()
