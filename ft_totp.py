import hashlib
import hmac
import struct
import os
import sys
import time  # Adding import for the 'time' module

KEY_FILE = "ft_otp.key"
KEY_SIZE = 64
OTP_LENGTH = 6
TIME_INTERVAL = 30  # Time interval in seconds
SHA1_DIGEST_LENGTH = 20  # SHA-1 hash output length in bytes


def save_key(key):
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key.encode())
        print("Key was successfully saved in", KEY_FILE)


def generate_totp(key):
    key = bytes.fromhex(key)
    time_step = int(time.time()) // TIME_INTERVAL
    packed_time = struct.pack('>Q', time_step)

    hmac_digest = hmac.new(key, packed_time, hashlib.sha1).digest()
    offset = hmac_digest[-1] & 0x0F

    truncated_hash = hmac_digest[offset:offset + 4]
    binary_code = struct.unpack('>I', truncated_hash)[0] & 0x7FFFFFFF

    otp = str(binary_code % (10 ** OTP_LENGTH)).zfill(OTP_LENGTH)
    return otp


def main():
    if len(sys.argv) < 3:
        print("Usage: python ft_otp.py -g <key.txt>"
              "&& python ft_otp.py -k <key.txt>")
        return

    option = sys.argv[1]
    key_file_path = sys.argv[2]

    if not os.path.isfile(key_file_path):
        print("Error: Key file does not exist.")
        return

    with open(key_file_path, 'r') as key_file:
        key = key_file.read().strip()

    if not all(c in "0123456789ABCDEFabcdef" for c in key):
        print("Error:"
              "Key file must contain a valid 64-character hexadecimal key.")
        return

    if option == "-g":
        save_key(key)
    elif option == "-k":
        otp = generate_totp(key)
        print(otp)
    else:
        print("Invalid command.")


if __name__ == "__main__":
    main()
