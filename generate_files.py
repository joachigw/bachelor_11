import os
import pathlib

# Folder and file config
folder = "files"
file_size_bytes = 1 * 1024 * 1024 * 4  # 4 MB
num_files = 10_000
chunk_size = 1024 * 1024  # 1 MB

# Ensure folder exists
pathlib.Path(folder).mkdir(exist_ok=True)

print(f"Creating {num_files} files of ~4 MB each in '{folder}/'...")

for i in range(num_files):
    file_path = os.path.join(folder, f"file_{i+1}.bin")
    # print(f"Writing: {file_path}")
    with open(file_path, "wb") as f:
        bytes_written = 0
        while bytes_written < file_size_bytes:
            chunk = os.urandom(min(chunk_size, file_size_bytes - bytes_written))
            f.write(chunk)
            bytes_written += len(chunk)

print("Done!")
