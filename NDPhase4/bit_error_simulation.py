# Romeo Tim-Louangphixai, Chad Abboud, Brendan Pham
# Network Design: Principles, Protocols & Applications
# Programming Project Phase 3: Implement RDT 2.2 over an unreliable UDP channel with bit-errors
import random

def introduce_bit_errors(data_bytes, error_rate=0.01):
    """
    Introduces bit errors into a byte array based on a specified error rate.

    :param data_bytes: The original data bytes.
    :param error_rate: The probability of a bit error.
    :return: Byte array with bit errors introduced.
    """
    if error_rate <= 0:
        return data_bytes

    num_errors = int(error_rate * 8 * len(data_bytes))  # Calculate total number of bit errors

    if num_errors == 0:
        return data_bytes

    corrupted_data = bytearray(data_bytes)

    for _ in range(num_errors):
        byte_index = random.randint(0, len(corrupted_data) - 1)
        bit_index = random.randint(0, 7)  # Select a random bit position within the byte
        corrupted_data[byte_index] ^= (1 << bit_index)  # Flip the selected bit

    return bytes(corrupted_data)
