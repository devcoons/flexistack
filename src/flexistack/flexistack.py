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

#########################################################################################
# SAFE IMPORT (function)                                                                #
#########################################################################################

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
    import sys
    import importlib

    if package in sys.modules:
        module = sys.modules[package]
        if version:
            import importlib.metadata
            installed_version = importlib.metadata.version(package)
            if installed_version != version:
                subprocess.call([sys.executable, "-m", "pip", "install", f"{package}=={version}"])
                module = importlib.import_module(package) 
        if package_as:
            globals()[package_as] = module
        return

    try:
        module = importlib.import_module(package)
        if version:
            import importlib.metadata
            installed_version = importlib.metadata.version(package)
            if installed_version != version:
                subprocess.call([sys.executable, "-m", "pip", "install", f"{package}=={version}"])
                module = importlib.import_module(package) 
    except ImportError:
        install_cmd = [sys.executable, "-m", "pip", "install"]
        if version:
            install_cmd.append(f"{package}=={version}")
        else:
            install_cmd.append(package)
        import subprocess
        subprocess.call(install_cmd)
        module = importlib.import_module(package)

    if package_as:
        globals()[package_as] = module
    else:
        globals()[package] = module


#########################################################################################
# IMPORTS                                                                               #
#########################################################################################

import os
import sys
import uuid
import json
import time
import random
import string
import inspect
import argparse

from pathlib import Path
from genericpath import isdir
from os.path import isfile, join
from importlib.machinery import SourceFileLoader
from consolio import Consolio
from configvault import ConfigVault
from .helper import Helper

#########################################################################################
# CLASS                                                                                 #
#########################################################################################

class Plugin:
    """
    A class that wraps a loaded module object and its description.
    """
    m = None
    d = None
    c = None
    f = None
    
    # --------------------------------------------------------------------------------- #
    # --------------------------------------------------------------------------------- #

    def __init__(self, m, d, c, f):
        """
        Constructor method for the Module class.

        Args:
        - m: A reference to a loaded module object.
        - d: A string that describes the module.
        """
        self.m = m
        self.d = d
        self.c = c
        self.f = f        

    # --------------------------------------------------------------------------------- #
        
    def __call__(self, flexistack = None, as_module = False):
        """
        Returns the loaded module object when the Module instance 
        is called like a function.

        Returns:
        - The loaded module object.
        """
        _flexistack = flexistack if flexistack != None else self.f        
        return getattr(self.m,self.c)(_flexistack) if as_module == False else self.m

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

    # --------------------------------------------------------------------------------- #

    def __call__(self, flexistack = None, as_module = False):
        """
        Returns an object of the latest version of the module in the ModulePack.
        """    
        
        return self[self.versions()[0]](flexistack,as_module) 

    # --------------------------------------------------------------------------------- #

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

class Action(dict):
    """
    A class that wraps a loaded module object and its description.
    """
    m = None
    d = None
    p = None

    # --------------------------------------------------------------------------------- #
    # --------------------------------------------------------------------------------- #

    def __init__(self, m, d, p):
        """
        Constructor method for the Module class.

        Args:
        - m: A reference to a loaded module object.
        - d: A string that describes the module.
        """
        self.m = m
        self.d = d
        self.p = p

    # --------------------------------------------------------------------------------- #
        
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

    # --------------------------------------------------------------------------------- #

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

    # --------------------------------------------------------------------------------- #

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
    Main class for managing plugins, actions, middleware, and configuration storage.
    
    Attributes:
        project_dir (str): The directory path where the project files are located. 
            Defaults to the current working directory.
        uuid (str): A unique identifier for this instance of Flexistack, generated upon initialization.
        actions (dict): Stores available actions, allowing command-line invocation and execution 
            of specific functions within the project.
        plugins (Plugins): An instance of the Plugins class, acting as a container for 
            various plugins loaded within the project.
        middleware (object): A generic container object for middleware components. Middleware 
            can be dynamically loaded and assigned as properties within this object.
        debug (bool): Flag indicating whether debug mode is active. When True, additional 
            debugging information is printed to the console.
        console (Consolio): An instance of the Consolio class, used for printing 
            progress and status updates to the console.
        config_vault (ConfigVault): An instance of the ConfigVault class, used to securely store 
            and retrieve configuration data within the project.
    """

    project_dir     = None
    uuid            = None
    actions         = {}
    plugins         = Plugins()
    middleware      = type('', (), {})()
    parser          = None
    parsed_args     = None
    debug           = False    
    console         = None
    config_vault    = None
    chrono          = False
    
    # --------------------------------------------------------------------------------- #
    # --------------------------------------------------------------------------------- #

    def __init__(self, project_dir = None, debug = False, configs_vault_dir = None, config_vault_key = None):
        """
        Constructor method for the Autoloader class.
        """
        if len(sys.argv) > 1 and '--' in sys.argv:
            _spidx = sys.argv[1:].index('--')
            _internal_args = sys.argv[1:][_spidx+1:]
            sys.argv = sys.argv[:_spidx+1]
        else:
            _internal_args = []

        self.debug = True if '--debug' in _internal_args else debug
        self.chrono = True if '--chrono' in _internal_args else False
        self.console = Consolio(spinner_type='dots')
        self.dprint(0,"inf","Flexistack:init()")
        self.parser = argparse.ArgumentParser()
        if project_dir == None:
            self.dprint(1,"wrn","project_dir: not given")                        
            try:
                self.project_dir = os.path.dirname(inspect.stack()[1].filename)
            except:
                self.project_dir = os.getcwd()
        else:
            self.project_dir = os.path.abspath(os.path.normpath(project_dir))
        self.dprint(1,"cmp","project_dir: "+ self.project_dir) 
       
        _uuid_file = os.path.join(self.project_dir, ".uuid")
        if os.path.exists(_uuid_file):
            with open(_uuid_file, 'r') as read_uuid_file:
                self.uuid = read_uuid_file.readline()
        else:
            self.dprint(1,"wrn","uuid: will be generated")    
            self.uuid   = uuid.uuid4().hex
            with open(_uuid_file, 'w') as read_uuid_file:
                read_uuid_file.write(self.uuid)
         
        self.dprint(1,"cmp","uuid: "+ self.uuid)

        if config_vault_key == None:
            config_vault_key = self.uuid
            self.dprint(1,"wrn","config_vault_key: not given")
        self.dprint(1,"cmp","config_vault_key: "+config_vault_key)

        if configs_vault_dir == None:
            configs_vault_dir = ".configs"
            self.dprint(1,"wrn","configs_vault_dir: not given")
        self.dprint(1,"cmp","configs_vault_dir: "+os.path.join(self.project_dir, configs_vault_dir))
        self.config_vault = ConfigVault(os.path.join(self.project_dir, configs_vault_dir),config_vault_key)

    # --------------------------------------------------------------------------------- #

    def dprint(self,indent,status="str",message=''):
        if self.debug == False:
            return
        self.console.print(indent,status,message)    
                          
    # --------------------------------------------------------------------------------- #
        
    @property    
    def helper(self):
        return Helper
    
    # --------------------------------------------------------------------------------- #
        
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
                for class_name,_class in inspect.getmembers(module,inspect.isclass):                   
                    if hasattr(_class,'_flexi_'):
                        if _class._flexi_.get('type') == "plugin":                
                            autoload_structure = {"type":str, "name": str, "description": str, "version": str}
                            if not all(key in  _class._flexi_ and isinstance(_class._flexi_[key], value_type)
                                for key, value_type in autoload_structure.items()):
                                continue                   
                            p_name = _class._flexi_['name']
                            p_vers = _class._flexi_['version']
                            p_desc = _class._flexi_['description']
                            module_rnd = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
                            if self.plugins.get(p_name) is None:
                                self.plugins[p_name] = PluginPack()  
                            self.plugins[p_name][p_vers] = Plugin(SourceFileLoader( p_name + "v" \
                                                 + str(p_vers) + "_" + module_rnd, 
                                                 module_full_path).load_module(), p_desc,class_name, self)  
                            self.dprint(1,"cmp","Loaded!")
                        else:
                            self.dprint(1,"wrn","Skipped.")      
                    else:
                        self.dprint(1,"wrn","Skipped.")                            
            except  Exception as e:
                self.dprint(1,"err","Exception: "+ str(e))              
                pass 
            if 'module_candidate' in sys.modules:
                del sys.modules['module_candidate']
        self.dprint(0,"inf","Flexistack:load_plugins()")        
        if dir_paths == None:
            self.dprint(1,"wrn","dir_paths: not given")
            return
        if isinstance(dir_paths,str):
            dir_paths = [dir_paths]
        if not isinstance(dir_paths,list):    
             raise Exception("Error: Flexistack `dir_paths` required argument is not a type of list[str]")   
        for dir_path in dir_paths:
            dir_path = self.get_filepath(dir_path)                    
            modules_paths = [str(path) for path in list(Path(dir_path).rglob("*.py")) ]
            for m_path in modules_paths:
                self.dprint(1,"wip","Start loading: "+m_path)          
                _load(m_path)              

    # --------------------------------------------------------------------------------- #

    def load_middleware(self, dir_paths): 
        """
        Loads middleware from a specified directory and enlists them 
        in the Flexistack middleware as properties.

        Args:
        - dir_paths: A string or list of strings representing the path(s) to the directory(ies) 
          containing the middlewares to load.  
        """      
        def _load(module_full_path):  
            try:    
                module = SourceFileLoader("module_candidate", module_full_path).load_module()
                classes = inspect.getmembers(module,inspect.isclass)
                for class_name,_class in classes:
                    if class_name == "Flexistack":
                        continue
                    self.dprint(2,"wip","Loading class: "+class_name)                
                    if hasattr(_class,'_flexi_'):
                        if _class._flexi_.get('type') == "middleware":
                            _class(self.middleware)
                            self.dprint(2,"cmp","Loaded!")
                        else:
                            self.dprint(2,"wrn","Skipped.") 
                    else:
                        self.dprint(2,"wrn","Skipped.")                                                      
                del module
            except  Exception as e:
                self.dprint(1,"err","Exception: "+ str(e))
                pass 
            if 'module_candidate' in sys.modules:
                del sys.modules['module_candidate']
        self.dprint(0,"inf","Flexistack:load_middleware()")         
        if dir_paths == None:
            self.dprint(1,"wrn","dir_paths: not given")
            return
        if isinstance(dir_paths,str):
            dir_paths = [dir_paths]
        if not isinstance(dir_paths,list):    
             raise Exception("Error: Flexistack `dir_paths` required argument is not a type of list[str]")   
        for dir_path in dir_paths:     
            dir_path = self.get_filepath(dir_path)         
            modules_paths = [str(path) for path in list(Path(dir_path).rglob("*.py")) ]
            for m_path in modules_paths:
                self.dprint(1,"wip","Start loading: "+m_path)                
                _load(m_path) 
                
    # --------------------------------------------------------------------------------- #
    
    def load_actions(self, dir_paths):  
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
                    self.dprint(2,"wip","Start loading: "+element)                 
                    if isdir(join(_directory, element)):
                        self.dprint(3,"wip","Try to load as intermediate positional argument.")                      
                        flexiarg_filepath = os.path.abspath(os.path.normpath(os.path.join(_directory, element, ".flexistack")))
                        if not os.path.exists(flexiarg_filepath):
                            self.dprint(3,"wrn","Skipped.")                           
                            continue    
                        with open(flexiarg_filepath, 'r') as subparse_info_file:
                            self.dprint(3,"wip","Try to load pos.arg special details.")                         
                            subparse_data = json.load(subparse_info_file)
                            elements.append((subparse_data['z-index'],element,os.path.join(_directory, element),subparse_data['description']))   
                        self.dprint(3,"cmp","Loaded!")                  
                    elif isfile(join(_directory, element)) and ".py" in element and not ".pyc" in element and not "__init__" in element:
                        self.dprint(3,"wip","Try to load as leaf positional argument.")
                        relative_action = os.path.relpath(_directory, dir_path)
                        if relative_action == ".":
                            relative_action = ""
                        else:
                            relative_action = relative_action+"/"                      
                        command  = element.replace(".py", "")
                        action_name = relative_action + command
                        module = SourceFileLoader(action_name,os.path.join(_directory, element)).load_module()
                        if not hasattr(module,'Action'):
                            del module
                            self.dprint(3,"wrn","Skipped.")                            
                            continue
                        action = module.Action(None)
                        if not hasattr(action,'_flexi_'):
                            del action, module
                            self.dprint(3,"wrn","Skipped.")                           
                            continue 
                        autoload_structure = {"type":str, "description": str}
                        if not all(key in action._flexi_ and isinstance(action._flexi_[key], value_type)
                            for key, value_type in autoload_structure.items()):
                            del action, module
                            self.dprint(3,"wrn","Skipped.")                           
                            return  
                        if action._flexi_.get("type") != "action":
                            del action, module
                            self.dprint(3,"wrn","Skipped.")                            
                            return                          
                        as_optional = action._flexi_.get('as_optional')
                        description = action._flexi_.get('description')
                        if description != None and as_optional == None and "set_optional_arguments" in list(module.Action.__dict__.keys()):
                            _app[action_name] = module
                            __subparser = _subparser.add_parser(command,help=description)
                            _app[action_name].Action(None).set_optional_arguments(__subparser, self)
                            self.dprint(3,"cmp","Loaded!")                            
                        elif description != None and as_optional != None:
                            _app[action_name] = module
                            _parser.add_argument('-'+command[0],'--'+command, action=as_optional, help=description)
                            self.dprint(3,"cmp","Loaded!")                            
                        else:
                            pass
                    else:
                        self.dprint(3,"wrn","Skipped.")                                                
                elements.sort(key=lambda tup: tup[0])      
                for elm in elements:
                    __parser = _subparser.add_parser(elm[1], help=elm[3])
                    __subparser = __parser.add_subparsers(title='Available commands', dest=elm[1]+'_action')
                    _app = add_action(_app,elm[2],__parser,__subparser)
            except Exception as e:
                raise Exception("Error: Flexistack `dir_paths` actions loading failed " + str(e))
            return _app

        self.dprint(0,"inf","Flexistack:load_action()")
        if dir_paths == None:
            self.dprint(1,"wrn","dir_paths: not given")
            return
        
        subparsers  = self.parser.add_subparsers(title="Available actions", dest='action') 
        if isinstance(dir_paths,str):
            dir_paths = [dir_paths]
        if not isinstance(dir_paths,list):
             raise Exception("Error: Flexistack `dir_paths` required argument is not a type of list[str]")   
        for dir_path in dir_paths:
            dir_path = self.get_filepath(dir_path) 
            self.dprint(1,"wip","Start loading from: "+dir_path)                   
            self.actions.update(add_action({},dir_path, self.parser, subparsers))
        pass
    
    # --------------------------------------------------------------------------------- #

    def load(self, middleware_dirs, actions_dirs, plugins_dirs):      
        self.load_middleware(middleware_dirs)     
        self.load_plugins(plugins_dirs)    
        self.load_actions(actions_dirs)

    # --------------------------------------------------------------------------------- #

    def parse_arguments(self):
        try:
            args, unknown = self.parser.parse_known_args()
            self.parsed_args = vars(args)       
        except Exception as e: 
            print(e)
            print("Error: Invalid arguments")
            exit() 
        return self.parsed_args, unknown   

    # --------------------------------------------------------------------------------- #

    def run(self, project_dir = None, parsed_args = None):
        """
        Executes actions based on parsed arguments and project directory.

        Args:
            self: The instance of the class.
            parsed_args (dict): Parsed arguments containing action information.
            project_dir (str): Directory path of the project.

        Returns:
            bool: True if action execution is successful, False otherwise.
        """
        if project_dir == None:
            project_dir = self.project_dir
        
        if parsed_args == None:
            parsed_args = self.parsed_args

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
                appender = ""
                while True:
                    iterration = iterration + 1
                    if iterration > 5:
                        self.dprint(0,"err","Commands depths cannot be achived (inf.loop.breaker)")
                        return False         
                    if (cur_act_level+"_action" in parsed_args) and parsed_args[cur_act_level+"_action"] == None:
                        self.dprint(0,"err","Incomplete command. Please use -h <--help> for more information")
                        return False
                    elif cur_act_level+"_action" in parsed_args:
                        appender = appender + cur_act_level+"/"
                        cur_act_level = parsed_args[cur_act_level+"_action"]
                    else:
                        obj = self.actions[appender+cur_act_level].Action(self)
                        if obj.init(pargs=parsed_args,project_dir=project_dir) == True:
                            return obj.run()                 
                        return False 
        except Exception as e: 
            print(e)
            return False

    # --------------------------------------------------------------------------------- #
    # --------------------------------------------------------------------------------- #

    def get_filepath(self, paths, project_dir = None):
        _results = []
        _project_dir = project_dir if project_dir != None else self.project_dir
        _paths = [paths] if isinstance(paths,str) else paths
        for path in _paths:
            if path.startswith("::"):
                path = path[2:]
                path = path[1:] if path.startswith("/") else path
                path = path[1:] if path.startswith("\\") else path
                _results.append(Helper.resolve_path(os.path.normpath(os.path.join(os.getcwd(),path))))
            elif path.startswith(":"):
                path = path[1:]
                path = path[1:] if path.startswith("/") else path
                path = path[1:] if path.startswith("\\") else path
                _results.append(Helper.resolve_path(os.path.normpath(os.path.join(_project_dir,path))))
            else:
                _results.append(Helper.resolve_path(os.path.normpath(path)))
        return _results[0] if isinstance(paths,str) else _results
        
#########################################################################################
# CLASS DECORATOR                                                                       #
######################################################################################### 

def flexi_action(as_optional, description):
    
    def class_decorator(cls):
        cls._flexi_ = {'type':'action',
                       'as_optional' : as_optional,
                       'description':description}      

        def action_init(self, flexistack=None):
            self.basename = os.path.basename(sys.modules[cls.__module__].__file__)
            self.flexistack = flexistack 
            try:
                if hasattr(self, 'req_plugins'):
                    if self.flexistack != None and self.req_plugins != None:
                        if len(self.req_plugins) == 0:
                            return
                        if (set(self.req_plugins) - self.flexistack.plugins.keys()):
                            self.flexistack.dprint(0,"wrn",str(self.__class__)+" missing required plugins")
            except:
                self.flexistack.dprint(0,"wrn",str(self.__class__)+" plugins could not be loaded")
        
        cls.__init__ = action_init
        return cls
 
    return class_decorator

#########################################################################################
# CLASS DECORATOR                                                                       #
######################################################################################### 

def flexi_middleware(description):
    
    def class_decorator(cls):
        cls._flexi_ = {'type':'middleware',
                       'description':description}      

        def middleware_init(self, middleware):
            self.basename = os.path.basename(sys.modules[cls.__module__].__file__)
            setattr(middleware, self.__class__.__name__.lower(), self)
            if hasattr(self, 'init'):
                self.init()       
        
        cls.__init__ = middleware_init
        return cls
 
    return class_decorator

#########################################################################################
# CLASS DECORATOR                                                                       #
#########################################################################################         
   
def flexi_plugin(name,version,description):
    
    def class_decorator(cls):
        cls._flexi_ = {'type':'plugin',
                       'name': name,
                       'version':version,
                       'description':description}      

        def plugin_init(self, flexistack=None):
            self.basename = os.path.basename(sys.modules[cls.__module__].__file__)
            self.flexistack = flexistack 
            try:
                if hasattr(self, 'req_plugins'):
                    if self.flexistack != None and self.req_plugins != None:
                        if len(self.req_plugins) == 0:
                            return
                        if (set(self.req_plugins) - self.flexistack.plugins.keys()):
                            self.flexistack.dprint(0,"wrn",str(self.__class__)+" missing required plugins")
            except:
                self.flexistack.dprint(0,"wrn",str(self.__class__)+" plugins could not be loaded")        
        
        cls.__init__ = plugin_init
        return cls
 
    return class_decorator

#########################################################################################
# EOF                                                                                   #
#########################################################################################