# Key management PoC

This Proof of Concept demonstrates a secure and scalable key management system for hierarchical AES-256 key derivation and file encryption, as part of a bachelor’s thesis focused on secure software distribution.

It provides AES-256 key derivation using KBKDFHMAC with SHA-256 in Counter Mode, and file encryption using AES-GCM.

There is also a script for generating required Labels and Contexts for use in key derivation, as well as dummy files for encryption.

<br>

## Prerequisites

- Python 3.10 or higher
- (Optional) Virtual environment tool (such as `virtualenv`)
<br>

## Installation

Clone this project to your desired machine.

```bash
git clone https://github.com/joachigw/bachelor_11.git
```

Install all required dependencies, preferably in a [Python Virtual Environment](https://docs.python.org/3/library/venv.html).

```bash
pip install -r requirements.txt
```
<br>

## Usage

This system derives AES-256 sub-keys from keys located in `config/company_keys.csv`.<br>Additional AES-256 keys can be added here.

<img src="/assets/key_hierarchy_readme.png" alt="Key hierarchy" width="800">

The leaf-node derived keys are the keys used to encrypt the dummy files. A key is only used to encrypt one dummy file.

Generate Labels, Contexts and dummy files:

```bash
python3 scripts/utils_test_data.py <n_companies> <n_departments> <n_units> <file_size_mb>
```

The number of keys to derive and files to encrypt is the product of `<n_companies>, <n_departments> and <n_units>`.

Due to there only being 20 keys in `config/company_keys.csv`, the maximum number of `n_companies` will be 20.

### Example usage

Generate dummy data for 2 companies, 3 departments per company, 4 units per departments, with 5 MB dummy files:

```bash
python3 scripts/utils_test_data.py 2 3 4 5
```

There will be created 2 * 3 * 4 = 24 dummy files of 5 MB each.

### Run benchmark

After the dummy data has been generated, run a benchmark for time measurements:

```bash
python3 crypto_benchmark.py
```

By default, the benchmark runs 5 rounds of key derivation and file encryption.
<br>When the benchmark has finished, the following output is printed to the terminal:

<img src="/assets/benchmark_summary.png" alt="Benchmark summary of key derivation and file encryption" width="800">
<br>

## Authors
- Heine Mærde Brakstad – [@joachigw](https://github.com/joachigw)
- Mikkel Bentzrud Rasch – [@colaxin](https://github.com/colaxin)
- Joachim Grimen Westgaard – [@heinemb](https://github.com/heinemb)

## License

See [LICENSE.md](./LICENSE.md) for licensing details.
