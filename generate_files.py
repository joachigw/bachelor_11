import os
import pathlib
import shutil
from time import time

# Folder and file config
folder = "./config/files"
file_size_bytes = 1 * 1024 * 1024 * 4  # 4 MB
num_files = 8000
chunk_size = 1024 * 1024 * 4  # 4 MB

# Ensure folder exists
pathlib.Path(folder).mkdir(exist_ok=True)

print(f"Creating {(num_files):_} files of ~4 MB each in '{folder}/'...")
start = time()
file_path = os.path.join(folder, "file_0.bin")
with open(file_path, "wb") as f:
    bytes_written = 0
    while bytes_written < file_size_bytes:
        chunk = os.urandom(min(chunk_size, file_size_bytes - bytes_written))
        f.write(chunk)
        bytes_written += len(chunk)
for i in range(num_files):
    file_name = f"{folder}/file_{i+1}.bin"
    if os.path.exists(file_name):
        continue
    shutil.copyfile(f"{file_path}", file_name)

end = time()
print(f"Done! File generation took {(end-start):.2f}s.")
