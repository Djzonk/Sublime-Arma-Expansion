"""Mod path methods"""
import os

class Mod(object):
    """Gneral Info for the mod"""
    def __init__(self, data):
        # TODO: change to arma project
        #self.path = data["arma-project"]["mod-path"]
        self.path = data["folders"][0]["path"]
        self.name = os.path.basename(self.path).lower()
        self.addons = os.path.join(self.path, "addons")
        self.components = []
        self.get_components()
        self.component = ""
        self.component_path = ""
        self.functions_path = ""

    def get_components(self):
        """Gets the components of the mod"""
        os.chdir(self.addons)
        for component in os.listdir(self.addons):
            if os.path.isdir(component):
                self.components.append(component)

    def select_component(self, index):
        """Gets the path to the component folder"""
        self.component = self.components[index]
        self.component_path = os.path.join(self.addons, self.component)
        self.get_functions()

    def get_functions(self):
        """Gets path to functions folder"""
        self.functions_path = os.path.join(self.component_path, "functions")
