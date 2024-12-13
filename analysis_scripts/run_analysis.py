# Created by amans
# 2024/12/13

import os
from nbconvert.preprocessors import ExecutePreprocessor
from nbformat import read, write
from nbformat.reader import NotJSONError
from datetime import date


# Read and parse the configuration file
# Slightly different form read_config() in Snakefile
# This read_config() also detects multi-line config vars
def read_config(file_path):
    variables = {}
    with open(file_path, "r") as f:
        for line in f:
            # Skip empty lines and comments
            line = line.strip().rstrip(",")
            if not line or line.startswith("#"):
                continue
            # Parse key-value pairs
            if "=" in line:
                key, value = line.split("=", 1)
                current_key = key.strip()
                value = value.strip().strip('"')

                if key == "BOOKS":  # BOOKS, which maybe multi-line
                    # save as a list
                    if "," in value:
                        value = [item.strip() for item in value.split(",")]
                    variables[key] = [value]
                else:
                    variables[key] = value

            # If the line doesn't contain "=", it continues the previous value (multi-line handling)
            elif current_key is not None:
                extra_value = line.strip('"').strip()
                if isinstance(variables[current_key], list):
                    variables[current_key].append(extra_value)
                else:
                    raise TypeError("Multi-line values must be saved as list.")

    return variables


def execute_notebook(notebook_path, savepath):
    try:
        # Read the notebook
        with open(notebook_path, "r", encoding="utf-8") as f:
            notebook = read(f, as_version=4)

        # Set up the preprocessor
        ep = ExecutePreprocessor(timeout=600, kernel_name="python3")

        # Execute the notebook
        ep.preprocess(
            notebook, {"metadata": {"path": os.path.dirname(notebook_path)}}
        )

        # Write the executed notebook back to the file
        with open(notebook_path, "w", encoding="utf-8") as f:
            write(notebook, f)

        print(f"{notebook_path} executed successfully.")
    except NotJSONError as e:
        print(f"Error: Failed to read {notebook_path}.")
        print(e)
    except Exception as e:
        print(f"Error: Failed to execute {notebook_path}")
        print(e)


def main(run=True):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    vars = read_config(os.path.join(dir_path, "scripts_to_run.cfg"))
    print(vars)

    # Execute each notebook iteratively
    for notebook in vars["BOOKS"]:
        # add date to executed file and save
        savepath = os.path.join(
            vars["OUTDIR"] + date.today().strftime("%y%m%d") + "_" + notebook
        )

        if run:
            execute_notebook(
                os.path.join(vars["HYDROBOOKSDIR"], notebook), savepath
            )

    print("All notebooks executed successfully.")


if __name__ == "__main__":
    main(run=False)
