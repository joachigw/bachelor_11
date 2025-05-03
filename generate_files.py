import os
import sys
import pathlib
import shutil


def generate_files(n_files: int, file_size_mb: int) -> None:
    """Generate a given number of files of a given size in MB.
    
    :param n_files: number of files to generate
    :param file_size_mb: size of each file in MB
    """

    # Folder and file size config
    folder = "./config/files"
    pathlib.Path(folder).mkdir(exist_ok=True)
    chunk_size = 1024 * 1024 * file_size_mb

    # Create the base file to copy
    print(f"Creating {(n_files):_} files of ~4 MB each in '{folder}/'...", end='')
    file_path = os.path.join(folder, "file_0.bin")
    with open(file_path, "wb") as f:
        bytes_written = 0
        while bytes_written < chunk_size:
            chunk = os.urandom(min(chunk_size, chunk_size - bytes_written))
            f.write(chunk)
            bytes_written += len(chunk)

    # Create copies, continue if a copy already exists
    for i in range(n_files):
        file_name = f"{folder}/file_{i+1}.bin"
        if os.path.exists(file_name):
            continue
        shutil.copyfile(f"{file_path}", file_name)

    print("done!")


if __name__ == "__main__":
    match(len(sys.argv)):
        case 1:
            print("Missing parameters 'n_files' and 'file_size_mb'.\n")
            default = input("Generate 1_000 files? (Y/n):")
            if default.upper() == "Y": generate_files(1000, 4)
            else: print("Aborting.")
        case 2:
            print("Missing parameter 'file_size_mb'.")
        case 3:
            generate_files(int(sys.argv[1]), int(sys.argv[2]))
