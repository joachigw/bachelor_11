import os
from concurrent.futures import ThreadPoolExecutor
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def encrypt_file(args: tuple) -> None:
    """Read a file in the specified directory, encrypt a copy of it,
    and store the encrypted copy in the specified directory using the provided AES256-key.
    The provided key shall only used to encrypt this specific file.

    :param i_key_pair: tuple of the file-index to encrypt and AES256-key
    """
    i_key_pair, input_dir, output_dir = args
    i, key = i_key_pair
    nonce = os.urandom(12)
    aesgcm = AESGCM(key)

    # Read file to encrypt
    with open(f"{input_dir}/file_{i}.bin", "rb") as f:
        data = f.read()

    ciphertext = aesgcm.encrypt(nonce, data, None)

    # Write encrypted data to file
    with open(f"{output_dir}/file_{i}E.bin", "wb") as f:
        f.write(nonce + ciphertext)


def encrypt_files(keys: list, input_dir: str, output_dir: str) -> None:
    """Encrypt all files in the specified directory using the provided AES256-keys.
    Encrypted files are stored in the specified output directory.

    :param keys: list of all AES256-keys
    :param input_dir: path of files to encrypt
    :param output_dir: path to save encrypted files in
    """

    # One thread per file
    args = [((i, key), input_dir, output_dir) for i, key in enumerate(keys)]
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        executor.map(encrypt_file, args)
    
    print("done!")
