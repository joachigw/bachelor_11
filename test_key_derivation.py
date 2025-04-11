from cryptography.hazmat.primitives.kdf.kbkdf import (CounterLocation, KBKDFCMAC, Mode)
from cryptography.hazmat.primitives.ciphers import algorithms
from string import ascii_uppercase, ascii_lowercase
from time import time
import ctypes


# Key hierarchy:
# 20 companies (A-T)
# 20 departments per company (a-t)
# 1000 units per department
n_companies = 20
n_departments = 20
n_units = 1000
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

letters = list(ascii_uppercase)
letters_lower = list(ascii_lowercase)
department_labels = []
department_contexts = []
for i in range(len(letters)):
    department_labels.append(f"Label department {letters_lower[i]}")
    department_contexts.append(f"Context department {letters_lower[i]}")

unit_labels = []
unit_contexts = []
for i in range(n_units):
    unit_labels.append(f"Label unit {i}")
    unit_contexts.append(f"Context unit {i}")

start = time()

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
            # print(f"Company {letters[i]}, department {letters_lower[j]} and unit {k+1}: {key}")

end = time()
print(f"Keys derived: {(n_companies*n_departments*n_units):_}")
print(f"Elapsed time: {end - start}s")
