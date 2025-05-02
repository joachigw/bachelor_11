import os
from dotenv import load_dotenv
from time import time
from concurrent.futures import ThreadPoolExecutor
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

load_dotenv()
INPUT_DIR = os.environ.get("FILES_DIR")
OUTPUT_DIR = os.environ.get("ENCRYPTED_DIR")

"""
Read a file, encrypt a copy of it, and store the encrypted copy in the './config/files'-directory using the provided AES256-key.
The provided key shall only used to encrypt this specific file.

:param i_key_pair: tuple of the file-index to encrypt and AES256-key
"""
def encrypt_file(i_key_pair: tuple):
    i, key = i_key_pair
    nonce = os.urandom(12)
    aesgcm = AESGCM(key)

    with open(f"{INPUT_DIR}/file_{i}.bin", "rb") as f:
        data = f.read()

    ciphertext = aesgcm.encrypt(nonce, data, None)

    with open(f"{OUTPUT_DIR}/file_{i}E.bin", "wb") as f:
        f.write(nonce + ciphertext)

"""
Encrypt all existing files using the provided AES256-keys.

:param keys: list of all AES256-keys
"""
def encrypt_files(keys: list):
    start_encryption = time()

    # One thread per file
    with ThreadPoolExecutor(max_workers=16) as executor:
        executor.map(encrypt_file, enumerate(keys))

    time_encryption = f"{(time() - start_encryption):.5f}"
    files_per_sec = f"{(int)(len(keys)/(float(time_encryption))):_}"
    print("done!")
    print(f"    Time to encrypt {len(keys):_} files: {str(time_encryption).replace('.', ',')}\n    (files/sec={files_per_sec})")
