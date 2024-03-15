# FlexiStack Framework

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
import argparse

project_dir = os.path.dirname(__file__)

if __name__ == "__main__":
   
    # Create an argument parser
    parser = argparse.ArgumentParser()

    # Create an instance of the FlexiStack framework
    fstack = flexistack.FlexiStack()

    # Load plugins
    fstack.load_plugins(os.path.join(project_dir, "plugins"))

    # Load actions
    fstack.load_actions(parser, os.path.join(project_dir, "actions"))

    # Identify the positional arguments and select the appropriate app_route to be executed
    try:
        args, unknown = parser.parse_known_args()
        parsed_args = vars(args)       
    except Exception as e: 
        print(e)
        print("Error: Invalid arguments")
        exit()

    fstack.run(parsed_args, project_dir)
```    

## Example

For a simple example, please refer to the /examples directory within the FlexiStack package.


## Conclusion

FlexiStack simplifies the development of modular Python applications by handling argument parsing and supporting multiple versions of plugins. Its intuitive design allows for quick setup and seamless integration into various project structures.
