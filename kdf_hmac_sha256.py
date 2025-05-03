from pandas import read_csv
from multiprocessing import Pool, cpu_count
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.kbkdf import (CounterLocation, KBKDFHMAC, Mode)

def derive_keys_dep(args) -> list[bytes]:
    """Derive all unit keys within a department.

    :param args: tuple of the department's label and context, the units' labels and contexts, and the department's company key
    :return list of bytes representing derived keys for the department
    """

    department_label, department_context, unit_labels, unit_contexts, company_key = args
    derived_unit_keys = []

    kdf = KBKDFHMAC(
        algorithm=hashes.SHA256(),
        mode=Mode.CounterMode,
        length=32,
        rlen=4,
        llen=4,
        location=CounterLocation.BeforeFixed,
        label=department_label.encode("utf-8"),
        context=department_context.encode("utf-8"),
        fixed=None
    )

    d_key = kdf.derive(company_key.encode("utf-8"))

    for j in range(len(unit_labels)): # units
        kdf = KBKDFHMAC(
            algorithm=hashes.SHA256(),
            mode=Mode.CounterMode,
            length=32,
            rlen=4,
            llen=4,
            location=CounterLocation.BeforeFixed,
            label=unit_labels[j].encode("utf-8"),
            context=unit_contexts[j].encode("utf-8"),
            fixed=None
        )
        key = kdf.derive(d_key)
        derived_unit_keys.append(key)
    return derived_unit_keys


def derive_keys(n_companies: int, n_departments: int, n_units: int, company_keys_path: str) -> list[bytes]:
    """Derive all keys for all specified companies.

    :param n_companies: number of companies
    :param n_departments: numper of departments
    :param n_units: number of units
    :return list of bytes representing derived keys
    """

    derived_keys = []

    # Configuration data for key derivation
    company_keys = [row.iloc[0] for (_, row) in read_csv(company_keys_path, delimiter=",").iterrows()]
    data = read_csv("./config/labels_contexts.csv", delimiter=",")
    department_labels = list((data["department_labels"]))
    department_contexts = list((data["department_contexts"]))
    unit_labels = list((data["unit_labels"]))
    unit_contexts = list((data["unit_contexts"]))

    # Split data before spawning processes
    args = []
    for i in range(n_companies):
        for j in range(n_departments):
            idx = j * n_units
            args.append((
                department_labels[idx],
                department_contexts[idx],
                unit_labels[idx:(idx+n_units)],
                unit_contexts[idx:(idx+n_units)],
                company_keys[i],
            ))

    # Derive all keys for one department within a company
    with Pool(processes=cpu_count()) as pool:
        derived = pool.map(derive_keys_dep, args)

    # Verify that all keys are valid 256-bit AES-keys
    derived_keys = [key for sublist in derived for key in sublist]
    for idx, key in enumerate(derived_keys):
        if not isinstance(key, bytes) or len(key) != 32:
            raise ValueError(f"Invalid key at index {idx}: type={type(key)}, len={len(key)}")

    print("done!")
    return derived_keys
