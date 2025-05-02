import os
import sys
import pathlib
import shutil
from time import time


def generate_files(n_files: int, file_size_mb: int):
    # Folder and file config
    folder = "./config/files"
    pathlib.Path(folder).mkdir(exist_ok=True)
    chunk_size = 1024 * 1024 * file_size_mb

    print(f"Creating {(n_files):_} files of ~4 MB each in '{folder}/'...")
    start = time()
    file_path = os.path.join(folder, "file_0.bin")
    with open(file_path, "wb") as f:
        bytes_written = 0
        while bytes_written < chunk_size:
            chunk = os.urandom(min(chunk_size, chunk_size - bytes_written))
            f.write(chunk)
            bytes_written += len(chunk)
    for i in range(n_files):
        file_name = f"{folder}/file_{i+1}.bin"
        if os.path.exists(file_name):
            continue
        shutil.copyfile(f"{file_path}", file_name)

    end = time()
    print(f"Done! File generation took {(end-start):.2f}s.")

if __name__ == "__main__":
    match(len(sys.argv)):
        case 1:
            print("Missing parameters 'n_files' and 'file_size_mb'.")
        case 2:
            print("Missing parameter 'file_size_mb'.")
        case 3:
            generate_files(int(sys.argv[1]), int(sys.argv[2]))
