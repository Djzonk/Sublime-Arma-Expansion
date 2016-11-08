"""Automaticaly Generates a new sqf function and add it to the XEH_PREP file"""
#pylint: disable=w0401,c0301,c0111
#pylint: disable=e0401


import os
import textwrap
import sublime
import sublime_plugin
from .mod import Mod

FUNCTION_HEADER = textwrap.dedent("""\
/*
 * Author: [Name of Author(s)]
 * [Description]
 *
 * Arguments:
 * 0: Argument Name <TYPE>
 *
 * Return Value:
 * Return Name <TYPE>
 *
 * Example:
 * ["example"] call {0}_{1}_{2}
 *
 * Public: [Yes/No]
 */
#include "script_component.hpp"

""")

def append_prep_file(component_path, input_function_name):
    """Find the XEH_PREP file and append the new function to it"""

    prep_path = os.path.join(component_path, "XEH_PREP.hpp")
    if os.path.exists(prep_path):
        with open(prep_path, "a") as prep_file:
            prep_file.write(("PREP({0});\n".format(input_function_name)))
        return True

    elif sublime.ok_cancel_dialog("Prep file dose not exist. Would you like me to create it for you"):
        with open(prep_path, "a") as prep_file:
            prep_file.write(("PREP({0});\n".format(input_function_name)))
        return True

    else:
        return False

def create_function(prefix, component, function_name_no_extension):
    """Creates the function file"""
    with open(function_name_no_extension + ".sqf", "w") as function_file:
        function_file.write(FUNCTION_HEADER.format(prefix, component, function_name_no_extension))

class NewSqfFunctionCommand(sublime_plugin.WindowCommand):
    def run(self):

        def on_enter_filename(input_function_name):
            mod = Mod(self.window.project_data())
            function_name_no_extension = "fnc_" + input_function_name
            function_name_full = function_name_no_extension + ".sqf"

            def on_component_select(index):
                mod.select_component(index)


                print((os.path.join(mod.functions_path, function_name_full)))
                # Check if function alread exists
                if os.path.isfile(os.path.join(mod.functions_path, function_name_full)):
                    # Error if it dose
                    sublime.error_message("Function already exists")
                else:
                    if append_prep_file(mod.component_path, input_function_name):
                        if os.path.exists(mod.functions_path):
                            os.chdir(mod.functions_path)
                            create_function(mod.name, mod.component, function_name_no_extension)
                            self.window.open_file(os.path.join(mod.functions_path, function_name_full))

            self.window.show_quick_panel(mod.components, on_component_select)
        self.window.show_input_panel("Enter function name: fnc_", "", on_enter_filename, None, None)
