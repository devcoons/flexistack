
`# FlexiStack Framework

[![PyPI - Version](https://img.shields.io/pypi/v/flexistack.svg)](https://pypi.org/project/flexistack)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flexistack.svg)](https://pypi.org/project/flexistack)
[![License: MIT](https://img.shields.io/badge/license-MIT-C06524)](https://github.com/devcoons/flexistack/blob/main/LICENSE.txt)

FlexiStack is a Python package designed to facilitate the rapid development of modular Python applications. This framework consists of two main entities: actions and plugins. Actions are user-performed tasks exposed as application arguments, while plugins are functional components that users can consume within their actions. It simplifies the complexity of argument parsing and supports multiple versions of plugins.

## Installation

You can install FlexiStack using pip:` 

`pip install flexistack`

## Getting Started

Although FlexiStack supports various project structures, a recommended one is as follows:` 

```
/project_directory 
│ 
├── __main__.py 
├── /actions 
│ └── ... 
└── /plugins 
└── ...
```


A minimum setup in the `__main__.py` file to utilize FlexiStack:

```Python
import os
import flexistack

project_dir = os.path.dirname(__file__)

if __name__ == "__main__":
   
    # Create an instance of the Flexistack framework
    fstack = flexistack.Flexistack()

    # Load actions and plugins
    fstack.load(os.path.join(project_dir, "actions"), 
                os.path.join(project_dir, "plugins"))

    # Parse arguments
    _, unknown_args = fstack.parse_arguments()

    # Execute actions/plugins based on given args
    fstack.run(project_dir)
    
    pass
```

## Plugins in FlexiStack

FlexiStack supports plugins, which are functional components that users can consume within their actions. Plugins enhance the capabilities of the framework by providing reusable functionality for various tasks. Here's how developers can work with plugins in FlexiStack:

1.  **Create Plugin Classes**: Define Python classes for each plugin version within the `plugins` directory of your project. Each plugin class should contain methods for initialization and the functionality it provides.
    
2.  **Specify Plugin Details**: In each plugin class, define the `autoload` attribute with details about the plugin, such as its name, version, and description. This information helps FlexiStack manage and identify plugins effectively.
    
3.  **Implement Plugin Functionality**: Inside the plugin class, implement the functionality that the plugin offers. This could include data generation, external API integration, or any other task that the plugin is designed for.
    

### Plugin Versioning

FlexiStack supports multiple versions of plugins, allowing developers to introduce enhancements or fixes without breaking existing functionality. Plugin versioning follows a structured approach, where each version is identified by a version number (e.g., `0.1`, `0.2`, etc.). When loading plugins, FlexiStack automatically selects the latest version available.

### Example

Suppose you want to create a plugin called `data-generator` for generating random data. Here's how you can do it:

1.  **Define Plugin Class**: Create a new Python file named `data_generator.py` within the `plugins` directory of your project.
    
2.  **Specify Plugin Details**: Inside `data_generator.py`, define a class named `Plugin` and specify the plugin details using the `autoload` attribute. For example:
    
```Python
class Plugin:
        autoload = {
            "name": "data-generator",
            "version": "0.1",
            "description": "Plugin for generating random data"
        }
```

3.  **Implement Plugin Functionality**: Add methods to the `Plugin` class for initialization and the functionality it provides. For instance:
   

```Python
class Plugin:
        autoload = {
            "name": "data-generator",
            "version": "0.1",
            "description": "Plugin for generating random data"
        }
    
        def init(self, **kargs):
            # Initialization logic
            pass
    
        def generate_random_data(self):
            # Functionality to generate random data
            pass           
```

By following this approach, you can effectively integrate plugins into your FlexiStack-based application, extending its functionality and enhancing its capabilities as needed.

## Actions in FlexiStack

Actions in FlexiStack are user-performed tasks exposed as application arguments. They allow developers to define specific functionality that users can invoke from the command line. Here's how developers can create and use actions in FlexiStack:

1.  **Create Action Classes**: Define Python classes for each action within the `actions` directory of your project. Each action class should contain methods for initialization and the functionality it provides.
    
2.  **Specify Action Details**: In each action class, define the `autoload` attribute with details about the action, such as its description. This information helps FlexiStack manage and identify actions effectively.
    
3.  **Implement Action Functionality**: Inside the action class, implement the functionality that the action offers. This could include data manipulation, file operations, or any other task that the action is designed for.
    

### Example

Suppose you want to create an action called `shuffle` for shuffling a given string. Here's how you can do it:

1.  **Define Action Class**: Create a new Python file named `shuffle.py` within the `actions` directory of your project.
    
2.  **Specify Action Details**: Inside `shuffle.py`, define a class named `Action` and specify the action details using the `autoload` attribute. For example:
    
```Python
   class Action:
        autoload = {
            "description": 'Shuffle a given string'
        }
```
    
3.  **Implement Action Functionality**: Add methods to the `Action` class for initialization and the functionality it provides. For instance:
    

```Python
class Action:
        autoload = {
            "description": 'Shuffle a given string'
        }
    
        def init(self, **kargs):
            # Initialization logic
            pass
    
        def run(self, **kargs):
            # Functionality to shuffle the string
            pass
```

### Calling Plugins in Your Code

Once you've defined a plugin, you can call its functionality from your actions. Here's how to do it:

1.  **Loading Plugins**: In your main application code, load the plugins using the `load` method of the FlexiStack framework.
    
2.  **Accessing Plugin Functionality**: Once loaded, you can access the functionality provided by a plugin by instantiating the plugin class and calling its methods. For example:
    
    
```Python
    # Access plugin functionality
    data_generator_plugin = fstack.plugins['data-generator'].latest(fstack)
    random_data = data_generator_plugin.generate_random_data()` 
```  

## Significance of .flexistack file in actions

The `.flexistack` file is a configuration file used by FlexiStack to provide additional metadata about actions. This metadata includes information such as the index of the actions family in the command-line argument list and a description of the actions family. By including this file in the actions directory, developers can enhance the usability of their applications by providing more context about each actions family.  

## Conclusion

FlexiStack simplifies the development of modular Python applications by handling argument parsing and supporting multiple versions of plugins. Its intuitive design allows for quick setup and seamless integration into various project structures.
