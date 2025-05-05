import os
import sys
import shutil
import pathlib
import pandas as pd
from dotenv import load_dotenv


def generate_labels_contexts(n_companies: int, n_departments: int, n_units: int) -> None:
    """Generate placeholder labels and contexts.

    :param n_companies: the number of companies
    :param n_departments: the number of departments per company
    :param n_units: the number of units per department
    """

    # Folder config
    folder = "./config"
    file_path = f"{folder}/labels_contexts.csv"
    conf_path = f"{folder}/conf.csv"
    pathlib.Path(folder).mkdir(exist_ok=True)
    
    print("\nCreating labels and contexts...", end='')

    all_department_labels, all_department_contexts = [], []
    all_unit_labels, all_unit_contexts = [], []

    for _ in range(n_companies):
        for i_department in range(n_departments):
            department_label = f"Label department {i_department}"
            department_context = f"Context department {i_department}"
            for i_unit in range(n_units):
                all_department_labels.append(department_label)
                all_department_contexts.append(department_context)
                all_unit_labels.append(f"Label unit {i_unit}")
                all_unit_contexts.append(f"Context unit {i_unit}")

    # Save labels and contexts to a .csv
    data = pd.DataFrame({
        'department_labels': all_department_labels,
        'department_contexts': all_department_contexts,
        'unit_labels': all_unit_labels,
        'unit_contexts': all_unit_contexts
    })
    data.to_csv(file_path, index=False)

    # Save number of companies, departments and units
    conf = pd.DataFrame([n_companies, n_departments, n_units])
    conf.to_csv(conf_path, index=False, header=False)

    print("done!")


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

def load_envs() -> dict:
    """Load environment variables.
    
    :return dictionary of the env-variables
    """
    load_dotenv()
    env_vars = {
        "FILES_DIR": os.environ.get("FILES_DIR"),
        "ENCRYPTED_DIR": os.environ.get("ENCRYPTED_DIR"),
        "CONFIG": os.environ.get("CONFIG"),
        "COMPANY_KEYS": os.environ.get("COMPANY_KEYS"),
    }
    not_found = []
    for name, value in env_vars.items():
        if value is None:
            not_found.append(name)
    if len(not_found) > 0:
        print(f"Environment variables {not_found} could not be set!\nPlease verify 'os.environ.get()' and/or directory-paths in .env.")
        exit()

    # Optionally assign to variables
    return {"INPUT_DIR": env_vars["FILES_DIR"],
            "OUTPUT_DIR": env_vars["ENCRYPTED_DIR"],
            "CONFIG": env_vars["CONFIG"],
            "COMPANY_KEYS_PATH": env_vars["COMPANY_KEYS"]}

if __name__ == "__main__":
    match(len(sys.argv)):
        case 1:
            default = input("Generate the following:\n  1_000 labels&contexts\n  1_000 dummy files of 4MB each (~4GB)\n(Y/n): ")
            if default.upper() == "Y":
                generate_labels_contexts(10, 10, 10)
                generate_files(1_000, 4)
            else: print("Aborting.")
        case 2:
            print("Missing parameters 'n_departments', 'n_units', 'n_files' and 'file_size_mb'.")
        case 3:
            print("Missing parameters 'n_units', 'n_files' and 'file_size_mb'.")
        case 4:
            print("Missing parameters 'n_files' and 'file_size_mb'.")
        case 5:
            print("Missing parameter 'file_size_mb'.")
        case 6:
            n_companies = (int(sys.argv[1]))
            n_departments = (int(sys.argv[2]))
            n_units = (int(sys.argv[3]))
            generate_labels_contexts(n_companies, n_departments, n_units)
        
            n_files = (int(sys.argv[4]))
            file_size_mb = (int(sys.argv[5]))
            if (n_files*file_size_mb/1024) > 500:
                print("Cannot create file directory with size greater than 500GB. Please try again.")

            if n_files > 250_000:
                print("Cannot create more than 500 000 files. Please try again.")

            if file_size_mb > 2_048:
                print("Cannot create files larger than ~2GB. Please try again.")
                
            generate_files(n_files, file_size_mb)
