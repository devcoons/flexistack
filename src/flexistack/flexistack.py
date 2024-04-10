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
import random
import string
import inspect
import argparse
import importlib
import subprocess

from pathlib import Path
from genericpath import isdir
from os.path import isfile, join
from importlib.machinery import SourceFileLoader

from .helper import Helper

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
    c = None
    
    # --------------------------------------------------------------------------------- #
    # --------------------------------------------------------------------------------- #

    def __init__(self, m, d, c):
        """
        Constructor method for the Module class.

        Args:
        - m: A reference to a loaded module object.
        - d: A string that describes the module.
        """
        self.m = m
        self.d = d
        self.c = c

    # --------------------------------------------------------------------------------- #
        
    def __call__(self, flexistack = None):
        """
        Returns the loaded module object when the Module instance 
        is called like a function.

        Returns:
        - The loaded module object.
        """
        return getattr(self.m,self.c)(flexistack) if flexistack != None else self.m

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

    def __call__(self, flexistack = None):
        """
        Constructor method for the ModulePack class.
        """
        return self.latest(flexistack=flexistack)

    # --------------------------------------------------------------------------------- #

    def latest(self, flexistack = None):
        """
        Returns the latest version of the module in the ModulePack.

        Returns:
        - The Module object with the latest version number.
        """
        return self[self.versions()[0]](flexistack) if flexistack != None else self[self.versions()[0]]

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
    A dictionary-like class that loads modules from a specified 
    directory and caches them for future use.
    """
    project_dir     = None
    uuid            = None
    actions         = {}
    plugins         = Plugins()
    middleware      = type('', (), {})()
    parser          = None
    parsed_args     = None

    # --------------------------------------------------------------------------------- #
    # --------------------------------------------------------------------------------- #

    def __init__(self, project_dir = None):
        """
        Constructor method for the Autoloader class.
        """
        self.uuid   = uuid.uuid4().hex
        self.parser = argparse.ArgumentParser()

        if project_dir == None:
            try:
                self.project_dir = os.path.dirname(inspect.stack()[1].filename)
            except:
                self.project_dir = os.getcwd()
        else:
            self.project_dir = os.path.abspath(os.path.normpath(project_dir))

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
                                                 + str(p_vers) \
                                                 + "_" + module_rnd, module_full_path).load_module(), p_desc,class_name)   
            except  Exception as e:
                pass 
            if 'module_candidate' in sys.modules:
                del sys.modules['module_candidate']
                
        if dir_paths == None:
            return
        if isinstance(dir_paths,str):
            dir_paths = [dir_paths]
        if not isinstance(dir_paths,list):    
             raise Exception("Error: Flexistack `dir_paths` required argument is not a type of list[str]")   
        for dir_path in dir_paths:
            dir_path = os.path.abspath(os.path.normpath(dir_path))          
            modules_paths = [str(path) for path in list(Path(dir_path).rglob("*.py")) ]
            for m_path in modules_paths:
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
                    if hasattr(_class,'_flexi_'):
                        if _class._flexi_.get('type') == "middleware":
                            _class(self.middleware)
                del module
            except  Exception as e:
                pass 
            if 'module_candidate' in sys.modules:
                del sys.modules['module_candidate']
                
        if dir_paths == None:
            return
        if isinstance(dir_paths,str):
            dir_paths = [dir_paths]
        if not isinstance(dir_paths,list):    
             raise Exception("Error: Flexistack `dir_paths` required argument is not a type of list[str]")   
        for dir_path in dir_paths:
            dir_path = os.path.abspath(os.path.normpath(dir_path))          
            modules_paths = [str(path) for path in list(Path(dir_path).rglob("*.py")) ]
            for m_path in modules_paths:
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
                    if isdir(join(_directory, element)):
                        flexiarg_filepath = os.path.abspath(os.path.normpath(os.path.join(_directory, element, ".flexistack")))
                        if not os.path.exists(flexiarg_filepath):
                            continue    
                        with open(flexiarg_filepath, 'r') as subparse_info_file:
                            subparse_data = json.load(subparse_info_file)
                            elements.append((subparse_data['z-index'],element,os.path.join(_directory, element),subparse_data['description']))                 
                    if isfile(join(_directory, element)) and ".py" in element and not ".pyc" in element and not "__init__" in element:
                        command  = element.replace(".py", "")
                        module = SourceFileLoader(command,os.path.join(_directory, element)).load_module()
                        if not hasattr(module,'Action'):
                            del module
                            continue
                        action = module.Action(None)
                        if not hasattr(action,'_flexi_'):
                            del action, module
                            continue 
                        autoload_structure = {"type":str, "description": str}
                        if not all(key in action._flexi_ and isinstance(action._flexi_[key], value_type)
                            for key, value_type in autoload_structure.items()):
                            del action, module
                            return  
                        if action._flexi_.get("type") != "action":
                            del action, module
                            return                          
                        as_optional = action._flexi_.get('as_optional')
                        description = action._flexi_.get('description')
                        if description != None and as_optional == None and "set_optional_arguments" in list(module.Action.__dict__.keys()):
                            _app[command] = module
                            __subparser = _subparser.add_parser(command,help=description)
                            _app[command].Action(None).set_optional_arguments(__subparser, self)
                        elif description != None and as_optional != None:
                            _app[command] = module
                            _parser.add_argument('-'+command[0],'--'+command, action=as_optional, help=description)
                        else:
                            pass
                elements.sort(key=lambda tup: tup[0])      
                for elm in elements:
                    __parser = _subparser.add_parser(elm[1], help=elm[3])
                    __subparser = __parser.add_subparsers(title='Available commands', dest=elm[1]+'_action')
                    _app = add_action(_app,elm[2],__parser,__subparser)
            except Exception as e:
                raise Exception("Error: Flexistack `dir_paths` actions loading failed")
            return _app

        if dir_paths == None:
            return
        
        subparsers  = self.parser.add_subparsers(title="Available actions", dest='action') 
        if isinstance(dir_paths,str):
            dir_paths = [dir_paths]
        if not isinstance(dir_paths,list):
             raise Exception("Error: Flexistack `dir_paths` required argument is not a type of list[str]")   
        for dir_path in dir_paths:
            dir_path = os.path.abspath(os.path.normpath(dir_path))          
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

    def run(self, project_dir, parsed_args = None):
        """
        Executes actions based on parsed arguments and project directory.

        Args:
            self: The instance of the class.
            parsed_args (dict): Parsed arguments containing action information.
            project_dir (str): Directory path of the project.

        Returns:
            bool: True if action execution is successful, False otherwise.
        """
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

    # --------------------------------------------------------------------------------- #
    # --------------------------------------------------------------------------------- #

    def get_filepath(self, path, project_dir = None):
        _project_dir = project_dir if project_dir != None else self.project_dir
        if path.startswith("::"):
            path = path[2:]
            path = path[1:] if path.startswith("/") else path
            path = path[1:] if path.startswith("\\") else path
            return Helper.resolve_path(os.path.normpath(os.path.join(os.getcwd(),path)))
        if path.startswith(":"):
            path = path[1:]
            path = path[1:] if path.startswith("/") else path
            path = path[1:] if path.startswith("\\") else path
            return Helper.resolve_path(os.path.normpath(os.path.join(_project_dir,path)))
        return Helper.resolve_path(os.path.normpath(path))
        
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
                            print(str(self.__class__)+" - [warn] missing required plugins")
            except:
                print(str(self.__class__)+" - [warn] plugins could not be loaded")        
        
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
                            print(str(self.__class__)+" - [warn] missing required plugins")
            except:
                print(str(self.__class__)+" - [warn] plugins could not be loaded")        
        
        cls.__init__ = plugin_init
        return cls
 
    return class_decorator

#########################################################################################
# EOF                                                                                   #
#########################################################################################