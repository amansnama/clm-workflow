import os
import subprocess
import argparse


def run_xmlchange(caseroot, cfg_file):
    # Change the working directory to CASEROOT
    try:
        os.chdir(caseroot)
        print(f"Changed working directory to: {caseroot}")
    except FileNotFoundError:
        print(f"Error: CASEROOT directory '{caseroot}' does not exist.")
        return
    except Exception as e:
        print(f"Error: Unable to change directory to '{caseroot}': {e}")
        return

    with open(cfg_file, "r") as f:
        for line in f:
            # Remove leading/trailing whitespace
            line = line.strip()
            if line:  # if line is not empty
                print(f"Running: ./xmlchange {line}")
                try:
                    result = subprocess.run(
                        ["./xmlchange" + " " + line],
                        capture_output=True,
                        text=True,
                    )

                    # Check if the command was successful
                    if result.returncode == 0:
                        print(f"Success: {result.stdout}")
                    else:
                        print(f"Error: {result.stderr}")
                except Exception as e:
                    print(f"Failed to run command './xmlchange {line}': {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the xmlchange script with arguments from a config file."
    )
    parser.add_argument("caseroot", help="Path to the CASEROOT directory")
    parser.add_argument("cfg_file", help="Path to the xmlconfig.cfg file")

    args = parser.parse_args()

    run_xmlchange(args.caseroot, args.cfg_file)
