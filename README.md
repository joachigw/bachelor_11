# Key management PoC

This repo serves as a Proof of Concept for an aspect of a security architecture developed as part of a bachelor's thesis.

It provides AES-256 key derivation using KBKDFHMAC with SHA-256 in Counter Mode, and file encryption using AES-GCM.

There is also a script for generating required Labels and Contexts for use in key derivation, as well as dummy files for encryption.


## Installation

Clone this project to your desired machine.

```bash
git clone https://github.com/joachigw/bachelor_11.git
```

Install all required dependencies, preferably in a [Python Virtual Environment](https://docs.python.org/3/library/venv.html).

```bash
pip install -r requirements.txt
```

## Usage

This system derives AES-256 sub-keys from base-keys located in *config/company_keys.csv*. Additional base-keys can be added here.

![Key hierarchy](/assets/key_hierarchy_readme.png)

The leaf-node derived keys are the keys used to encrypt the dummy files. A key is only used to encrypt one dummy file.

Generate Labels, Contexts and dummy files:

```bash
python3 utils_test_data.py <n_companies> <n_departments> <n_units> <file_size_mb>
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
