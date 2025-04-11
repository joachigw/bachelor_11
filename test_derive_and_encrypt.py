import os
from cryptography.hazmat.primitives.kdf.kbkdf import (CounterLocation, KBKDFCMAC, Mode)
from cryptography.hazmat.primitives.ciphers import algorithms, Cipher, modes
from cryptography.hazmat.backends import default_backend
from string import ascii_uppercase, ascii_lowercase
from time import time
from pathlib import Path

start = time()

# Config
n_companies = 5
n_departments = 1
n_units = 1
files_dir = "files"
encrypted_dir = "encrypted_files"
Path(encrypted_dir).mkdir(exist_ok=True)

# Static company keys
company_keys = [
    "QRm9yuXDi2kfRJkxR6hyAUaNw7OV7OTu", # A
    "Q1H3IjqprpMp3vPbQBMwULv9WUhReXT7",
    "ekDC5nVxmnsN2HNwbhril8vFq7EjDuby",
    "mP1skq4dnl91OHwIpRdt2Amcr7q9jBGM",
    "pXc4YrcgUVbxZHzhSbmpjRpFb3CDqdVd",
    "qiLGZODzagplAUamvuakGY0nKwBFited",
    "H2jAHGe9v2kFPat1LoMq5UxYyaZb067M",
    "GnnFmPvCpKqgPa3xAhWBI772l424Xdz2",
    "pRdrA3tHzKUqhyw4PSJNV1726DMMDpf2",
    "ELDTBg9U0lLNO59l8FD6CJaujbDu4lGB", # J (10)
    "zVzE5nu7LOX3e4Qt3pj7uAez0rR728ys",
    "hwHxx6tIx8CRQdowDWTGjQg2PitgUIIj",
    "ADXPnbcAtBesJ1j5K8wal5PEyKNZfUzI",
    "CFjBle2OApEh3rTYvNpo6PNjPqJNAwnO",
    "Wuo6WPbNIijjqPvrzmG0SPvnAgp4WP2J",
    "bAGYp64kjjY60SbggCbm4c39CUFLUFM3",
    "itvzPcfCg1qOKjZohUEvkjbl0jODhuZP",
    "s4Enb9M2Vy8yeqBqO3sxLAUyrjpDH6l4",
    "wFrNPqUJqtLy9qgP1astD2H5WmEIiBNW",
    "59btfMdaS7iWeLjDhsD3bZeeZTUIoe07" # T (20)
]

# Labels/contexts
letters = list(ascii_uppercase)
letters_lower = list(ascii_lowercase)
department_labels = [f"Label department {c}" for c in letters]
department_contexts = [f"Context department {c}" for c in letters_lower]
unit_labels = [f"Label unit {i}" for i in range(n_units)]
unit_contexts = [f"Context unit {i}" for i in range(n_units)]

# Store derived unit keys
derived_unit_keys = []

# Derive 5 unit keys
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
        
        for k in range(n_units):
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
            print(f"Key derived: {key.hex()}")

# Encrypt the 5 "software"-files with the corresponding derived key
backend = default_backend()

print("\n\n### File encryption ###")
for idx in range(len(derived_unit_keys)):
    file_path = os.path.join(files_dir, f"file_{idx+1}.bin")
    enc_file_path = os.path.join(encrypted_dir, f"enc_file_{idx+1}.bin")

    if not os.path.exists(file_path):
        print(f"The file '{file_path}' was not found. Skipping...")
        continue
    cipher = Cipher(algorithms.AES(derived_unit_keys[idx]), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()

    print(f"Encrypting: {file_path} → {enc_file_path}")
    with open(file_path, "rb") as fin, open(enc_file_path, "wb") as fout:
        while True:
            chunk = fin.read(16 * 1024)
            if not chunk:
                break
            # Pad final block deterministically
            if len(chunk) % 16 != 0:
                chunk += b"\x00" * (16 - len(chunk) % 16)
            fout.write(encryptor.update(chunk))
        fout.write(encryptor.finalize())

end = time()

print(f"\nFile encryption complete.\nTime elapsed: {end - start}s")
