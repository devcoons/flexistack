# FlexiStack Framework

[![PyPI - Version](https://img.shields.io/pypi/v/flexistack?style=for-the-badge)](https://pypi.org/project/flexistack)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flexistack?style=for-the-badge)
![GitHub License](https://img.shields.io/github/license/devcoons/flexistack?style=for-the-badge)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/flexistack?style=for-the-badge&color=%23F0F)


FlexiStack is a sophisticated Python framework designed to streamline the development of modular applications. It allows developers to efficiently manage the complexity associated with building applications by segmenting functionality into distinct, reusable components. FlexiStack provides a structured approach to developing software, offering significant benefits:

- <b>Modularity</b>: Promotes clean separation of concerns, enabling developers to organize code into manageable pieces.
- <b>Reusability</b>: Components such as actions and plugins can be reused across different projects, reducing development time.
- <b>Extensibility</b>: New functionalities can be easily added through plugins without altering the core application logic.
- <b>Simplicity</b>: Simplifies argument parsing and command-line interface creation, making it easier to build and maintain complex applications.

<b>Core Components of FlexiStack</b>

FlexiStack's architecture is built around three main components: `middleware`, `actions`, and `plugins`. Each serves a unique purpose within the framework, contributing to its flexibility and power.

# Installation

You can install FlexiStack using pip:

`pip install flexistack`

# How to use

Although FlexiStack can support various project structures, a recommended one is as follows:

```
/project_directory 
│ 
├── __main__.py 
├── /core 
│ └── ... 
├── /actions 
│ └── ... 
└── /plugins 
└── ...
```

## Main Flexistack application

A minimum setup in the `__main__.py` file to utilize FlexiStack:

```Python
import os
import flexistack

if __name__ == "__main__":
   
    # Create an instance of the Flexistack framework
    fstack = flexistack.Flexistack()

    # Load actions and plugins
    fstack.load(":core/", ":actions/",":plugins/")

    # Parse arguments
    _, unknown_args = fstack.parse_arguments()

    # Execute actions/plugins based on given args
    fstack.run()
    
    pass
```

## Flexistack Middleware

Middleware in FlexiStack serves as an intermediate layer that can process data or handle requests both before and after they reach the core action logic. Middleware can be employed for various purposes, such as logging, authentication, data preprocessing, or any other cross-cutting concern that should be applied consistently across different parts of your application.

FlexiStack utilizes the concept of middleware to provide a flexible way to insert these cross-cutting concerns without cluttering the business logic of actions and plugins. Middleware classes are automatically recognized and utilized by FlexiStack based on their structure and configuration.

#### Implementing Middleware

To implement middleware in FlexiStack, you have to define a Python class with the appropriate flexi decorator `flexi_middleware`. The class name is used automatically as a callable property within `flexistack.middleware`, making it readily available throughout your application. 

The key elements of a middleware class are:
- `class <name>`: The name of the class is used by the framework to access the functionalities of the middleware.
- `@flexi_middleware (decorator)`: describes the type of this class (middleware) and contains a short description of it.
- `init (method)`: Your init code (it is called automatically by the framework (once)).

<b>Example: Terminal Middleware</b>

```Python
from flexistack import *

@flexi_middleware(description="Simple colorful terminal")
class Terminal:

    def init(self):
        # Optional: Initialization code here
        pass

    # Example method for middleware
    def print(self, message):
        print(message)
```

#### Using Middleware

Once defined, middleware can be used throughout your application simply by accessing it through the flexistack.middleware property. For example, to use the Terminal middleware in an action to print a message, you would do the following:

```Python
self.flexistack.middleware.terminal.print("This is a message from an action using Terminal middleware.")
```

This approach to middleware allows FlexiStack applications to maintain clean separation of concerns and promotes the reuse of common functionalities across different parts of the application. By defining middleware like the Terminal example, developers can encapsulate specific behaviors (such as custom logging, output formatting, etc.) in a way that's easily accessible and reusable without coupling these behaviors to the core logic of actions or plugins.


### Flexistack Actions

Actions are central to FlexiStack's design, representing the tasks that your application can perform. They are defined as Python scripts and are categorized into two main types based on how they are invoked from the command line:

- Positional Actions: These are converted into positional arguments. The framework dynamically constructs the command-line interface based on the action scripts' names and their directory structure. For instance, an action placed directly under the actions directory becomes a first-level positional argument, while an action inside a subdirectory (like generate/random-number.py) becomes a nested positional argument (generate random-number).
- Optional Actions: These are used as optional arguments, typically providing utility functionalities such as displaying the version of the application.

#### Implementing Actions
To implement an action, create a Python script in the `/actions` directory or a subdirectory for nesting. The script should define a class with the aforementioned key elements.

The structure and behavior of actions are defined by several key elements:

- `File Name`: Determines the argument name used to invoke the action from the command line.
- `flexi_action (decorator)`: Contains metadata about the action, including its type and description.
- `set_optional_arguments (method)`: Defines additional CLI arguments that the action accepts.
- `init (method)`: Performs initial setup based on the provided command-line arguments.
- `run (method)`: Contains the main logic to be executed when the action is invoked.

#### Example: Positional Action

```Python
from flexistack import *

@flexi_action(None, 'Shuffle a given string')
class Action:

    def set_optional_arguments(self, parser, modules):
        parser.add_argument('--data', help="Input data to shuffle")

    def init(self, **kwargs):
        self.data = kwargs.get('data', None)
        return True

    def run(self, **kwargs):
        # Logic to shuffle the data
        pass
```

#### Example: Optional Action

```Python
from flexistack import *

@flexi_action('store_true', 'Shuffle a given string')
class Action:

    def init(self, **kwargs):
        return True

    def run(self, **kwargs):
        print("Application Version: 1.0.0")
```

#### Action Invocation and Structure

The framework auto-generates the command-line interface based on the action scripts' names and their placement within the directory structure. This structure allows for intuitive and organized access to the various functionalities of your application.

- A script named shuffle.py directly under actions is invoked as python app.py shuffle.
- A script named random-number.py inside a subdirectory generate is invoked as python app.py generate random-number.

<b>The `.flexistack` File</b>

For actions grouped under a directory (like generate), a .flexistack file within the directory provides additional metadata for the grouped actions, such as the order in which they appear and a short description. This file enhances the CLI's usability by organizing related actions under a common command namespace.

```
{
	"z-index": 105,
	"description": "Generate different data"
}
```

By carefully structuring actions and utilizing the .flexistack file for grouped actions, developers can create a rich, intuitive command-line interface for their applications using FlexiStack, enhancing both the development experience and the end user's interaction with the application.


## Flexistack Plugins

Plugins in FlexiStack are reusable components that extend the functionality of actions. They can be invoked by actions to perform specific tasks, such as generating data, interacting with databases, or integrating with external services. A notable feature of FlexiStack's plugin system is its support for versioning, allowing multiple versions of a plugin to coexist. This ensures that improvements or changes can be made to plugins without breaking existing functionality that depends on earlier versions.


### Key Elements of a Plugin

- `File Name`: Determines the argument name used to invoke the action from the command line.
- `flexi_plugin (decorator)`: Contains metadata about the plugin, including its name, version and description. This information is crucial for the framework to manage and utilize the plugin correctly.
- `Multiple Versions`: Plugins can have multiple versions, each residing in its own directory under the plugin's main directory. The version is specified in the `flexi_plugin` decorator
- `init (method-optional)`: Performs initial setup based on the provided command-line arguments.
- `run (method-optional)`: Contains the main logic to be executed when the action is invoked.

### Plugin Versioning

FlexiStack supports multiple versions of plugins, allowing developers to introduce enhancements or fixes without breaking existing functionality. Plugin versioning follows a structured approach, where each version is identified by a version number (e.g., `0.1`, `0.2`, etc.). When loading plugins, FlexiStack automatically selects the latest version available.

### Implementing a Plugin

To implement a plugin, create a directory under the plugins directory of your application, named after the plugin. Within this directory, create subdirectories for each version of the plugin, containing a Python script that defines the plugin's functionality.

#### Example: Dummy Data Generator Plugin (v0.2)

```Python
from flexistack import *

@flexi_plugin("dummy-generator", '0.2', "A plugin to generate dummy data for testing purposes")
class Plugin:

    def init(self,**kargs):
        print ("Dummy Data Generator Init")
        pass

    def random_string(self, length):
        # Example method to generate a random string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
```


### Using a Plugin within an Action

Actions as well as other plugins can utilize plugins by accessing them through the flexistack.plugins property. The framework ensures that actions can easily call upon plugin functionality while respecting versioning requirements.

#### Example: Generating a Random String in an Action

```Python
from flexistack import *

@flexi_action(None, 'Generate a random string')
class Action:

    length = None

    def set_optional_arguments(self, parser, modules):
        parser.add_argument('-l', '--length', type=int, help="Length of the random string")

     def init(self,**kargs):
        try:
            args = kargs['pargs']
            if ('length' in args):
                self.length = int(args['length'])
                return True
        except:
            pass
        return False

  def run(self, **kwargs):
        # Accessing the latest version of the dummy-generator plugin
        dummy_generator = self.flexistack.plugins['dummy-generator']()
        random_string = dummy_generator.random_string(self.length)
        print(f"Generated Random String: {random_string}")

```

In this example, the action generates a random string by utilizing the dummy-generator plugin. It specifies the length of the string through an optional argument. The action calls the random_string method of the latest version of the dummy-generator plugin, demonstrating how FlexiStack facilitates the interaction between actions and plugins while leveraging plugin versioning to ensure compatibility and flexibility.

## Conclusion

FlexiStack simplifies the development of modular Python applications by handling argument parsing and supporting multiple versions of plugins. Its intuitive design allows for quick setup and seamless integration into various project structures.
