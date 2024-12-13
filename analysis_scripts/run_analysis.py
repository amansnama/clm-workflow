# Created by amans
# 2024/12/13

import os
from nbconvert import NotebookExporter, ExecutePreprocessor
from nbformat import read, write
from nbformat.exceptions import NBFormatError

def execute_notebook(notebook_path):
    try:
        # Read the notebook
        with open(notebook_path, "r", encoding="utf-8") as f:
            notebook = read(f, as_version=4)

        # Set up the preprocessor
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

        # Execute the notebook
        ep.preprocess(notebook, {'metadata': {'path': os.path.dirname(notebook_path)}})

        # Write the executed notebook back to the file
        with open(notebook_path, "w", encoding="utf-8") as f:
            write(notebook, f)

        print(f"{notebook_path} executed successfully.")
    except NBFormatError as e:
        print(f"Error: Failed to read {notebook_path}.")
        print(e)
    except Exception as e:
        print(f"Error: Failed to execute {notebook_path}")
        print(e)
