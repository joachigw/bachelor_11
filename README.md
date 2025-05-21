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

This system derives AES-256 sub-keys from keys located in *config/company_keys.csv*.<br>Additional AES-256 keys can be added here.

![]()
<img src="/assets/key_hierarchy_readme.png" alt="Key hierarchy" width="800">

The leaf-node derived keys are the keys used to encrypt the dummy files. A key is only used to encrypt one dummy file.

Generate Labels, Contexts and dummy files:

```bash
python3 utils_test_data.py <n_companies> <n_departments> <n_units> <file_size_mb>
```

The number of keys to derive and files to encrypt is the product of ```<n_companies>, <n_departments> and <n_units>```.

After the dummy data has been generated, run a benchmark for time measurements:

```bash
python3 crypto_benchmark.py
```

By default, the benchmark runs 5 rounds of key derivation and file encryption.
<br>When the benchmark has finished, the following output is printed to the terminal:

<img src="/assets/benchmark_summary.png" alt="Benchmark summary of key derivation and file encryption" width="800">

## Authors
- Heine Mærde Brakstad – [@joachigw](https://github.com/joachigw)
- Mikkel Bentzrud Rasch – [@colaxin](https://github.com/colaxin)
- Joachim Grimen Westgaard – [@heinemb](https://github.com/heinemb)

## License

See [LICENSE.md](./LICENSE.md) for licensing details.
