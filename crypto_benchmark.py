import os
import shutil
import pandas as pd
from time import time
from tabulate import tabulate
from kdf_hmac_sha256 import derive_keys
from encrypt_aesgcm import encrypt_files
from utils_test_data import load_envs
from typing import Callable, TypeVar, Any, Tuple


envs = load_envs()

T = TypeVar("T")
def time_function(function: Callable[..., T], *args: Any, **kwargs: Any) -> Tuple[T, float]:
    """Measure elapsed runtime of a function.

    :param function: the function to time, takes any arguments and returns any generic type
    :param *args: list of arguments to pass to the function
    :param **kargs: dict/keyword arguments to pass to the function
    :return Tuple of result from function and elapsed time
    """
    start = time()
    result = function(*args, **kwargs)
    elapsed = time() - start
    return result, elapsed
    

def run_benchmarks(n_rounds: int) -> tuple:
    """Run a specified number of rounds of deriving keys and encrypting files.

    :param n_rounds: number of rounds to run
    :return tuple of derivation time and rate, and encryption time and rate
    """
    round_times = []
    derivation_times, derivation_rates = [], []
    encryption_times, encryption_rates = [], []
    for i in range(n_rounds):
        print(f"\n===ROUND {i+1}===")
        start_round = time()

        # Remove directory containing encrypted files, if present
        if os.path.exists(envs["OUTPUT_DIR"]):
            shutil.rmtree(envs["OUTPUT_DIR"])

        print(">Deriving keys...", end='')
        keys, time_derivation = time_function(derive_keys, n_companies, n_departments, n_units, envs["COMPANY_KEYS_PATH"])
        derivation_times.append(f"{time_derivation:.5f}".replace('.', ','))
        derivation_rates.append(f"{len(keys)//time_derivation}")

        print(">Encrypting files...", end='')
        _, time_encryption = time_function(encrypt_files, keys, envs["INPUT_DIR"], envs["OUTPUT_DIR"])
        encryption_times.append(f"{time_encryption:.5f}".replace('.', ','))
        encryption_rates.append(f"{len(keys)//time_encryption}")

        round_times.append(f"{(time()-start_round):.5f}")

    return round_times, derivation_times, derivation_rates, encryption_times, encryption_rates


if __name__ == "__main__":
    # Read configured n_companies, n_departments and n_units
    conf = pd.read_csv(envs["CONFIG"], header=None)[0].tolist()
    n_companies, n_departments, n_units = conf
    n_keys = n_companies*n_departments*n_units
    print(f"=== Parameters ===\n  keys to derive/files to encrypt: {n_keys:_}")

    # Time 5 rounds
    round_times, derivation_times, derivation_rates, encryption_times, encryption_rates = run_benchmarks(5)

    # Print results in tabular format
    headers = ["Round"] + [f"\033[1mRound {i+1}\033[0m" for i in range(5)]
    table = [
        ["Key Derivation (s)"] + derivation_times,
        ["Key Derivation rate (keys/s)"] + derivation_rates,
        ["File Encryption (s)"] + encryption_times,
        ["File Encryption rate (files/s)"] + encryption_rates,
        ["TOTAL (s)"] + round_times
    ]
    # Right-align all columns
    colalign = ["left"] + ["right"] * 5

    print(f"\n=== Results summary ({n_keys:_} keys) ===")
    print(tabulate(table, headers=headers, tablefmt="grid", colalign=colalign))
