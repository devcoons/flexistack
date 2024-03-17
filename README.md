# FlexiStack Framework

[![PyPI - Version](https://img.shields.io/pypi/v/flexistack.svg)](https://pypi.org/project/flexistack)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flexistack.svg)](https://pypi.org/project/flexistack)
[![License: MIT](https://img.shields.io/badge/license-MIT-C06524)](https://github.com/devcoons/flexistack/blob/main/LICENSE.txt)

FlexiStack is a Python package designed to facilitate the rapid development of modular Python applications. This framework consists of two main entities: actions and plugins. Actions are user-performed tasks exposed as application arguments, while plugins are functional components that users can consume within their actions. It simplifies the complexity of argument parsing and supports multiple versions of plugins.

Installation
You can install FlexiStack using pip:

```
pip install flexistack
```

## Getting Started

Although FlexiStack supports various project structures, a recommended one is as follows:

```
/project_directory
│
├── __main__.py
├── /actions
│   └── ...
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

## Example

For a simple example, please refer to the /examples directory within the FlexiStack package.


## Conclusion

FlexiStack simplifies the development of modular Python applications by handling argument parsing and supporting multiple versions of plugins. Its intuitive design allows for quick setup and seamless integration into various project structures.
