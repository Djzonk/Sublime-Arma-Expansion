#!/usr/bin/env python3
import os
import re
import sys


def main():
    print("""
  ##########################
  # Parsing XEH_PREP files #
  ##########################
""")
    mod_path = input("Input Path to mod (do not suround in \"\"):")
    mod_name = os.path.basename(os.path.normpath(mod_path))
    if mod_name == "ACE3":
        mod_name = "ace"
    addons_path = os.path.join(mod_path, "addons")

    script_path = os.path.dirname(os.path.realpath(__file__))

    completions = []

    os.chdir(addons_path)

    # Discover all files with the name XEH_PREP.hpp
    for component_folder in os.listdir(addons_path):
        if os.path.isdir(component_folder):
            for file in os.listdir(component_folder):
                if file == "XEH_PREP.hpp":
                    prep_path = os.path.abspath(os.path.join(addons_path, component_folder, file))

                    # Make sure file gets closed after being iterated
                    with open(prep_path, "r") as prep_file:
                        lines = prep_file.readlines()

                    # Iterate each line
                    for line in lines:
                        match = re.search(r"^PREP\((\w.*)\)", line)
                        if match:
                            function = ("\"" + mod_name + "_"
                                        + component_folder
                                        + "_fnc_" + match.group(1) + "\"," + "\n")
                            completions.append(function)
    output_template = ("""\
{{
    "scope": "source.sqf",
	"completions": [
    {0}
    ]
}}
    """).format("".join(completions))


    os.chdir(script_path)
    os.chdir("..")
    # Generate the output file
    with open(str(mod_name + "-functions.sublime-completions"), "w") as output_file:
        output_file.seek(0)
        #output_file.writelines(completions)
        output_file.write(output_template)

    print("\n")
    print("Sublime-completions file generated in language directory")
    input("Press Enter to Exit...")
if __name__ == "__main__":
    sys.exit(int(main() or 0))
