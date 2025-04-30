import sys
import pathlib
import pandas as pd
from time import time


def generate_labels_contexts(n_companies: int, n_departments: int, n_units: int):
    folder = "./config"
    pathlib.Path(folder).mkdir(exist_ok=True)
    file_path = f"{folder}/labels_contexts.csv"
    
    print(f"""Creating labels and contexts for:\n
          {(n_companies):_} companies,
          {(n_departments):_} departments per company,
          and {(n_units):_} units per department
          in '{(file_path)}'...""")

    start = time()

    all_department_labels = []
    all_department_contexts = []
    all_unit_labels = []
    all_unit_contexts = []

    for _ in range(n_companies):
        for i_department in range(n_departments):
            department_label = f"Label department {i_department}"
            department_context = f"Context department {i_department}"
            for i_unit in range(n_units):
                all_department_labels.append(department_label)
                all_department_contexts.append(department_context)
                all_unit_labels.append(f"Label unit {i_unit}")
                all_unit_contexts.append(f"Context unit {i_unit}")

    data = pd.DataFrame({
        'department_labels': all_department_labels,
        'department_contexts': all_department_contexts,
        'unit_labels': all_unit_labels,
        'unit_contexts': all_unit_contexts
    })
    data.to_csv(file_path, index=False)

    end = time()
    print(f"""Done! Generating labels and contexts took {(end-start):.2f}s.
          Saved in {file_path}.
          """)


if __name__ == "__main__":
    match(len(sys.argv)):
        case 1:
            print("Missing parameters 'n_companies', 'n_departments' and 'n_units'.")
        case 2:
            print("Missing parameters 'n_departments' and 'n_units'.")
        case 3:
            print("Missing parameter 'n_units'.")
        case 4:
            generate_labels_contexts(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))