#########################################################################################
#                                                                                       #
# MIT License                                                                           #
#                                                                                       #
# Copyright (c) 2024 Ioannis D. (devcoons)                                              #
#                                                                                       #
# Permission is hereby granted, free of charge, to any person obtaining a copy          #
# of this software and associated documentation files (the "Software"), to deal         #
# in the Software without restriction, including without limitation the rights          #
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell             #
# copies of the Software, and to permit persons to whom the Software is                 #
# furnished to do so, subject to the following conditions:                              #
#                                                                                       #
# The above copyright notice and this permission notice shall be included in all        #
# copies or substantial portions of the Software.                                       #
#                                                                                       #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR            #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,              #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE           #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER                #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,         #
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE         #
# SOFTWARE.                                                                             #
#                                                                                       #
#########################################################################################

import os
import sys
import uuid
import json
import importlib
import subprocess
import argparse
from pathlib import Path
from os.path import isfile, join
from genericpath import isdir
from importlib.machinery import SourceFileLoader

def safe_import(package: str, version: str = None, package_as: str = None) -> None:
    """
    Import a Python package safely and efficiently by checking if the package is
    already installed in the system. If the package is not installed, it installs
    the package using the `pip` package manager.

    Parameters:
    -----------
    package: str
        Name of the package to be imported.
    version: str, optional
        Version of the package to be installed. If not specified, the latest version
        of the package will be installed.
    package_as: str, optional
        Rename the imported package. If not specified, the package will be imported
        with its original name.

    Returns:
    --------
    None
    """
    
    try:
        if version is None:
            importlib.import_module(package)
        else:
            import pkg_resources
            _version = pkg_resources.get_distribution(package).version
            if version == _version:
                importlib.import_module(package)
            else:
                subprocess.call([sys.executable, "-m", "pip", "uninstall","-y"
                             , package+"=="+_version])
                subprocess.call([sys.executable, "-m", "pip", "install"
                             , package+"=="+version])            
    except:      
        if version is None:
            subprocess.call([sys.executable, "-m", "pip", "install"
                             , package])
        else:
            subprocess.call([sys.executable, "-m", "pip", "install"
                             , package+"=="+version])
    finally:
        if package_as is None:
            globals()[package] = importlib.import_module(package)
        else:
            globals()[package_as] = importlib.import_module(package)

#########################################################################################
# CLASS                                                                                 #
#########################################################################################

class Plugin:
    """
    A class that wraps a loaded module object and its description.
    """
    m = None
    d = None

    def __init__(self, m, d):
        """
        Constructor method for the Module class.

        Args:
        - m: A reference to a loaded module object.
        - d: A string that describes the module.
        """
        self.m = m
        self.d = d

    def __call__(self):
        """
        Returns the loaded module object when the Module instance 
        is called like a function.

        Returns:
        - The loaded module object.
        """
        return self.m

#########################################################################################
# CLASS                                                                                 #
#########################################################################################

class PluginPack(dict):
    """
    A dictionary-like class that stores multiple versions of a 
    module under different version numbers as keys.
    """
    def __init__(self):
        """
        Constructor method for the ModulePack class.
        """
        pass

    def latest(self):
        """
        Returns the latest version of the module in the ModulePack.

        Returns:
        - The Module object with the latest version number.
        """
        return self[self.versions()[0]]

    def versions(self):
        """
        Returns a sorted list of version numbers for the module 
        in the ModulePack.

        Returns:
        - A list of version numbers as strings, sorted 
          in descending order.
        """
        return sorted(self.keys(), key=lambda version: 
                  (tuple(map(int, version.split('.')))), 
                  reverse=True)

#########################################################################################
# CLASS                                                                                 #
#########################################################################################

class Plugins(dict):
    """
    A dictionary-like class that stores multiple versions of a 
    module under different version numbers as keys.
    """
    def info(self):
        """
        Returns a list of all the module names in the Autoloader.

        Returns:
        - A list of module names as strings.
        """
        return list(self.keys())

    def details(self):
        """
        Returns a dictionary that maps each module name to a list of 
        its available versions.

        Returns:
        - A dictionary with module names as keys and lists of version 
          numbers as strings as values.
        """
        r = {}
        for key in self.keys():
            r[key] = list(self[key].keys())
        return r

    def exists(self, mod_names):
        """
        Returns True if all specified modules exist in the Autoloader, 
        and False otherwise.

        Args:
        - mod_names: A string or a list of strings representing 
          module names.

        Returns:
        - True if all specified modules exist in the Autoloader, 
          and False otherwise.
        """
        if isinstance(mod_names, list):
            for mod_name in mod_names:
                if self.get(mod_name) is None:
                    return False
            return True
        else:
            return True if self.get(mod_names) is not None else False


#########################################################################################
# CLASS                                                                                 #
#########################################################################################            

class Flexistack():
    """
    A dictionary-like class that loads modules from a specified 
    directory and caches them for future use.
    """

    uuid            = None
    actions         = {}
    plugins         = Plugins()

    # --------------------------------------------------------------------------------- #

    def __init__(self):
        """
        Constructor method for the Autoloader class.
        """
        self.uuid = uuid.uuid4().hex

    def load_plugins(self, dir_paths):
        """
        Loads all plugins from a specified directory and enlists them 
        in the Autoloader.

        Args:
        - dir_paths: A string or list of strings representing the path(s) to the directory(ies) 
          containing the plugins to load.  
        """  
        def _load(module_full_path):  
            try:    
                module = SourceFileLoader("module_candidate", module_full_path).load_module()
                if not hasattr(module,'Plugin'):
                    del module
                    return
                plugin = module.Plugin(None)
                if not hasattr(plugin,'autoload'):
                    del plugin, module
                    return     
                autoload_structure = {"name": str, "description": str, "version": str}
                if not all(key in plugin.autoload and isinstance(plugin.autoload[key], value_type)
                    for key, value_type in autoload_structure.items()):
                    del plugin, module
                    return  
                p_name = plugin.autoload['name']
                p_vers = plugin.autoload['version']
                p_desc = plugin.autoload['description']
                module.__spec__.name = p_name + "v" \
                                     + str(p_vers) \
                                     + "_" + uuid.uuid4().hex
                if self.plugins.get(p_name) is None:
                    self.plugins[p_name] = PluginPack()
                self.plugins[p_name][p_vers] = Plugin(module, p_desc)
            except:
                pass 

        if isinstance(dir_paths,str):
            dir_paths = [dir_paths]
        if not isinstance(dir_paths,list):    
             raise Exception("Error: Autoloader `dir_paths` required argument is not a type of list[str]")   
        for dir_path in dir_paths:
            dir_path = os.path.abspath(os.path.normpath(dir_path))          
            modules_paths = [str(path) for path in list(Path(dir_path).rglob("*.py")) ]
            for m_path in modules_paths:
                _load(m_path)              

    def load_actions(self, parser, dir_paths):  
        """
        Loads all actions from a specified directory and enlists them 
        in the Flexistack Actions.

        Args:
        - parser: argparser to be used
        - dir_paths: A string or list of strings representing the path(s) to the directory(ies) 
          containing the plugins to load.  
        """  
        def add_action(_app, _directory, _parser, _subparser):  
            try:
                elements = []
                for element in os.listdir(_directory):
                    if isdir(join(_directory, element)):
                        autoloader_filepath = os.path.abspath(os.path.normpath(os.path.join(_directory, element, ".autoloader")))
                        if not os.path.exists(autoloader_filepath):
                            continue    
                        with open(autoloader_filepath, 'r') as subparse_info_file:
                            subparse_data = json.load(subparse_info_file)
                            elements.append((subparse_data['z-index'],element,os.path.join(_directory, element),subparse_data['description']))                 
                    if isfile(join(_directory, element)) and ".py" in element and not ".pyc" in element and not "__init__" in element:
                        command  = element.replace(".py", "")
                        module = SourceFileLoader(command,os.path.join(_directory, element)).load_module()
                        if "set_parser" in list(module.Action.__dict__.keys()):
                            try:
                                _app[command] = module
                                if "get_arg_help" in list(_app[command].Action.__dict__.keys()):
                                    __subparser = _subparser.add_parser(command,help=_app[command].Action(None).get_arg_help())
                                    _app[command].Action(None).set_parser(__subparser, self)      
                                else:                        
                                    _app[command].Action(None).set_parser(_parser, self)      
                            except:
                                 print ("[core|"+os.path.basename(__file__)+"]: Issue with automatic action loading ("+command+"). Please check!") 
                elements.sort(key=lambda tup: tup[0])      
                for elm in elements:
                    __parser = _subparser.add_parser(elm[1], help=elm[3])
                    __subparser = __parser.add_subparsers(title='Available commands', dest=elm[1]+'_action')
                    _app = add_action(_app,elm[2],__parser,__subparser)
            except Exception as e:
                print ("[core|"+os.path.basename(__file__)+"]: Issue with automatic args loading. Please check!") 
            return _app

        subparsers  = parser.add_subparsers(title="Available action", dest='action') 

        if isinstance(dir_paths,str):
            dir_paths = [dir_paths]
        if not isinstance(dir_paths,list):    
             raise Exception("Error: Autoloader `dir_paths` required argument is not a type of list[str]")   
        for dir_path in dir_paths:
            dir_path = os.path.abspath(os.path.normpath(dir_path))          
            self.actions.update(add_action({},dir_path,parser,subparsers))

    def run(self, parsed_args, project_dir):
        try:
            if parsed_args['action'] == None:
                for opt_action in parsed_args:
                    if parsed_args[opt_action] == True:   
                        obj = self.actions[opt_action].Action(self)
                        if obj.init(project_dir=project_dir) == True:
                            return obj.run()
                        return False
            else:
                iterration = 0
                cur_act_level = parsed_args['action']
                while True:
                    iterration = iterration + 1
                    if iterration > 5:
                        print("Error: Commands depths cannot be achived (inf.loop.breaker)")
                        return False         
                    if (cur_act_level+"_action" in parsed_args) and parsed_args[cur_act_level+"_action"] == None:
                        print("Error: Incomplete command. Please use -h <--help> for more information")
                        return False
                    elif cur_act_level+"_action" in parsed_args:
                        cur_act_level = parsed_args[cur_act_level+"_action"]
                    else:    
                        obj = self.actions[cur_act_level].Action(self)
                        if obj.init(pargs=parsed_args,project_dir=project_dir) == True:
                            return obj.run()                 
                        return False 
        except Exception as e: 
            print(e)
            return False
#########################################################################################
# END OF FILE                                                                           #
#########################################################################################