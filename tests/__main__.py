import os
import flexistack
import argparse


project_dir = os.path.dirname(__file__)

if __name__=="__main__":
   
    # Create an arguments parser
    parser = argparse.ArgumentParser()

    # Create an instance of the Flexistack framework
    fstack = flexistack.Flexistack()

    # Loads plugins
    fstack.load_plugins(os.path.join(project_dir, "plugins"))

    # Loads actions
    fstack.load_actions(parser, os.path.join(project_dir, "actions"))

    # Identify the positional arguments and select the appropriate app_route
    # to be executed 


    try:
        args, unknown = parser.parse_known_args()
        parsed_args = vars(args)
        
    except Exception as e: 
        print(e)
        print("Error: Invalid arguments")
        exit()

    fstack.run(parsed_args, project_dir)
    
    pass
