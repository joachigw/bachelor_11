import os
import shutil
import pandas as pd
from time import time
from pathlib import Path
from dotenv import load_dotenv
from kdf_hmac_sha256 import derive_keys
from encrypt_aesgcm import encrypt_files

load_dotenv()
FILES_DIR = os.environ.get("FILES_DIR")
ENCRYPTED_DIR = os.environ.get("ENCRYPTED_DIR")
CONFIG = os.environ.get("CONFIG")
COMPANY_KEYS_PATH = os.environ.get("COMPANY_KEYS")


Path(ENCRYPTED_DIR).mkdir(exist_ok=True)

if __name__ == "__main__":
    # Remove directory containing encrypted files, if present
    if os.path.exists(ENCRYPTED_DIR):
        shutil.rmtree(ENCRYPTED_DIR)
    
    # Read n_companies, n_departments and n_units
    conf = pd.read_csv(CONFIG, header=None)[0].tolist()
    n_companies, n_departments, n_units = conf

    # Time 5 rounds
    for _ in range(5):
        start_round = time()
        print(">Deriving keys...", end='')
        keys = derive_keys(n_companies, n_departments, n_units, COMPANY_KEYS_PATH)
        print(">Encrypting files...", end='')
        encrypt_files(keys)
        print(f"Total time elapsed: {(time()-start_round):.2f}s\n")