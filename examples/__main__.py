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
import flexistack
import argparse

#########################################################################################
# MAIN                                                                                 #
#########################################################################################

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

#########################################################################################
# END OF FILE                                                                           #
#########################################################################################
