import os
import shutil
import pandas as pd
from time import time
from pathlib import Path
from tabulate import tabulate
from dotenv import load_dotenv
from kdf_hmac_sha256 import derive_keys
from encrypt_aesgcm import encrypt_files


load_dotenv()
INPUT_DIR = os.environ.get("FILES_DIR")
OUTPUT_DIR = os.environ.get("ENCRYPTED_DIR")
CONFIG = os.environ.get("CONFIG")
COMPANY_KEYS_PATH = os.environ.get("COMPANY_KEYS")
Path(OUTPUT_DIR).mkdir(exist_ok=True)


def run_benchmarks(n_rounds: int) -> tuple:
    """Run a specified number of rounds of deriving keys and encrypting files.

    :param n_rounds: number of rounds to run
    :return tuple of derivation time and rate, and encryption time and rate
    """
    derivation_times, derivation_rates = [], []
    encryption_times, encryption_rates = [], []
    for i in range(n_rounds):
        print(f"\n===ROUND {i+1}===")
        start_round = time()

        start_derivation = time()
        print(">Deriving keys...", end='')
        keys = derive_keys(n_companies, n_departments, n_units, COMPANY_KEYS_PATH)
        derivation_time = time() - start_derivation
        derivation_times.append(f"{derivation_time:.5f}".replace('.', ','))
        derivation_rates.append(f"{len(keys)/derivation_time:.0f}")

        print(">Encrypting files...", end='')
        start_encryption = time()
        encrypt_files(keys, INPUT_DIR, OUTPUT_DIR)
        encryption_time = time() - start_encryption
        encryption_times.append(f"{encryption_time:.5f}".replace('.', ','))
        encryption_rates.append(f"{len(keys)/encryption_time:.0f}")

        print(f"Total time elapsed: {(time()-start_round):.2f}s\n")
    return derivation_times, derivation_rates, encryption_time, encryption_rates


if __name__ == "__main__":
    # Remove directory containing encrypted files, if present
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    
    # Read n_companies, n_departments and n_units
    conf = pd.read_csv(CONFIG, header=None)[0].tolist()
    n_companies, n_departments, n_units = conf
    n_keys = n_companies*n_departments*n_units

    # Time 5 rounds
    derivation_times, derivation_rates, encryption_times, encryption_rates = run_benchmarks(5)
    
    # Print results in tabular format
    headers = ["Round"] + [f"Round {i+1}" for i in range(5)]
    table = [
        ["Key Derivation Time (s)"] + derivation_times,
        ["Key Derivation Rate (keys/s)"] + derivation_rates,
        ["File Encryption Time (s)"] + encryption_times,
        ["File Encryption Rate (files/s)"] + encryption_rates,
    ]
    # Right-align all columns
    colalign = ["left"] + ["right"] * 5

    print(f"\n=== Results summary ({len(n_keys):_} keys) ===")
    print(tabulate(table, headers=headers, tablefmt="grid", colalign=colalign))
