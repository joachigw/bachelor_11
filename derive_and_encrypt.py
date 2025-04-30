import os
import pandas as pd
import multiprocessing
from cryptography.hazmat.primitives.kdf.kbkdf import (CounterLocation, KBKDFCMAC, Mode)
from cryptography.hazmat.primitives.ciphers import algorithms, Cipher, modes
from cryptography.hazmat.backends import default_backend
from time import time
from pathlib import Path



files_dir = "./config/files"
encrypted_dir = "./config/encrypted_files"
Path(encrypted_dir).mkdir(exist_ok=True)

# Import company keys, labels and contexts
company_keys = [row.iloc[0] for (_, row) in pd.read_csv("./config/company_keys.csv", delimiter=",").iloc[1:].iterrows()]
data = pd.read_csv("./config/labels_contexts.csv", delimiter=",")
department_labels = data["department_labels"]
department_contexts = data["department_contexts"]
unit_labels = data["unit_labels"]
unit_contexts = data["department_labels"]

"""
Derive an amount of keys using KBKDFCMAC in Counter Mode with AES256.

:param n_companies: Number of companies
:param n_departments: Number of departments per company
:param n_units: Number of units per department
:return: The derived AES256-keys
"""
def derive_keys(n_companies: int, n_departments: int, n_units: int):
    start_derive = time()
    derived_unit_keys = []

    print("\n### Key derivation ###")
    for i in range(n_companies): # companies
        for j in range(n_departments): # departments
            kdf = KBKDFCMAC(
                algorithm=algorithms.AES256,
                mode=Mode.CounterMode,
                length=32,
                rlen=4,
                llen=4,
                location=CounterLocation.BeforeFixed,
                label=department_labels[j].encode("utf-8"),
                context=department_contexts[j].encode("utf-8"),
                fixed=None
            )
            d_key = kdf.derive(company_keys[i].encode("utf-8"))
            
            for k in range(n_units): # units
                kdf = KBKDFCMAC(
                    algorithm=algorithms.AES256,
                    mode=Mode.CounterMode,
                    length=32,
                    rlen=4,
                    llen=4,
                    location=CounterLocation.BeforeFixed,
                    label=unit_labels[k].encode("utf-8"),
                    context=unit_contexts[k].encode("utf-8"),
                    fixed=None
                )
                key = kdf.derive(d_key)
                derived_unit_keys.append(key)
                # print(f"Key derived: {key.hex()}")

    time_derive = time() - start_derive
    print(f"Time to derive {len(derived_unit_keys):_} keys: {time_derive:.5f}s ({(int) (len(derived_unit_keys)/time_derive):_} keys/sec)")
    return derived_unit_keys


"""
Encrypts files in the ./config/files-directory with the provided AES256 keys.
A key is only used to encrypt one file.

:param derived_unit_keys: The AES256-keys to encrypt with
"""
def encrypt_files(derived_unit_keys: list):
    start_encrypt = time()
    backend = default_backend()
    print("\n\n### File encryption ###")
    for idx in range(len(derived_unit_keys)):
        file_path = os.path.join(files_dir, f"file_{idx+1}.bin")
        enc_file_path = os.path.join(encrypted_dir, f"enc_file_{idx+1}.bin")

        if not os.path.exists(file_path):
            print(f"The file '{file_path}' was not found. Skipping...")
            continue
        
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(derived_unit_keys[idx]), modes.CTR(iv), backend=backend)
        encryptor = cipher.encryptor()

        # print(f"Encrypting: {file_path} → {enc_file_path}")
        with open(file_path, "rb") as fin, open(enc_file_path, "wb") as fout:
            while True:
                chunk = fin.read(256 * 1024)
                if not chunk:
                    break
                # Pad final block deterministically
                if len(chunk) % 256 != 0:
                    chunk += b"\x00" * (256 - len(chunk) % 256)
                fout.write(encryptor.update(chunk))
            fout.write(encryptor.finalize())

    time_encryption = time() - start_encrypt
    print(f"Time to encrypt {len(derived_unit_keys):_} files:",
          f"{time_encryption:.5f}s ({(int) (len(derived_unit_keys)/(time_encryption)):_} files/sec)")


# derived_unit_keys = derive_keys(10, 10, 80)
# def encrypt_single_file(key, in_filename, out_filename, chunk_size=256*1024):
#     """Encrypts a single file using AES-256-CTR with a unique IV."""
#     backend = default_backend()
#     iv = os.urandom(16)
#     cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=backend)
#     encryptor = cipher.encryptor()

#     try:
#         with open(in_filename, "rb") as fin, open(out_filename, "wb") as fout:
#             fout.write(iv)
#             while True:
#                 chunk = fin.read(chunk_size)
#                 if not chunk:
#                     break
#                 fout.write(encryptor.update(chunk))
#             fout.write(encryptor.finalize())
#         return True
#     except Exception as e:
#         print(f"Error encrypting {in_filename}: {e}")
#         return False

# start_encrypt = time()
# backend = default_backend()
# print("\n\n### File encryption (Optimized + Parallel) ###")

# processes = []
# for idx in range(len(derived_unit_keys)):
#     file_path = os.path.join(files_dir, f"file_{idx+1}.bin")
#     enc_file_path = os.path.join(encrypted_dir, f"enc_file_{idx+1}.bin")

#     if not os.path.exists(file_path):
#         print(f"The file '{file_path}' was not found. Skipping...")
#         continue

#     process = multiprocessing.Process(target=encrypt_single_file,
#                                     args=(derived_unit_keys[idx], file_path, enc_file_path))
#     processes.append(process)
#     process.start()

# for process in processes:
#     process.join()

# time_encryption = time() - start_encrypt
# print(f"Time to encrypt {len(derived_unit_keys):_} files:",
#     f"{time_encryption:.5f}s ({(int) (len(derived_unit_keys)/(time_encryption)):_} files/sec)")


if __name__ == "__main__":
    start = time()
    keys = derive_keys(10, 10, 80)
    encrypt_files(keys)
    end = time()
    print(f"Total time elapsed: {(end-start):.2f}s")
