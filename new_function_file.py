#pylint: disable=c0111,e0401

import os
import textwrap
import json
import sublime, sublime_plugin


NEW_FUNCTION_NAME = ""
# FUNCTION_HEADER = textwrap.dedent("""\
# /*
#  * Author: [Name of Author(s)]
#  * [Description]
#  *
#  * Arguments:
#  * 0: Argument Name <TYPE>
#  *
#  * Return Value:
#  * Return Name <TYPE>
#  *
#  * Example:
#  * ["example"] call {0}_{1}_{2}
#  *
#  * Public: [Yes/No]
#  */
# #include "script_component.hpp"


# """).format(prefix, component, function_name)

# def get_prefix():
#     open()
#     prefix = ""
#     return prefix

class NewSqfFunctionCommand(sublime_plugin.WindowCommand):
    def run(self):
        # Gets json project file
        project = self.window.project_file_name()

        def funcname(function_name):
            full_function_name = "fnc_" + function_name
            self.window.status_message("Generated New Function: " + full_function_name)

        #self.window.show_input_panel("Enter function name: fnc_", "", funcname, None, None)
        with open(project, "r") as f:
            project_file = json.loads(f)
            print(project_file)
        #os.chdir()
