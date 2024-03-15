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
# CLASS
#########################################################################################

class Plugin():

    # FlexiStack plugin details
    # required from autoloader
    autoload = {
        "name": "dummy-generator",
        "version": "0.1.0",
        "description": "This a dummy data generator plugin"
    }

    # Dynamically loaded modules 
    # Do not modify (auto-populated)
    flexistack = None

    # Required modules list 
    #   Modify this list according to the
    #   needs of this module
    req_plugins = []

    # Constructor
    #   Only core operations to ensure that
    #   the current module has all the
    #   dependencies
    def __init__(self, flexistack = None):
        try:        
            self.flexistack = flexistack
            if len(self.req_plugins) == 0 or flexistack == None:
                return
            if (set(self.req_plugins) - self.flexistack.plugins.keys()):
                print(self.autoload['name']+" - [warn] missing required modules")
        except:
            print(self.autoload['name']+" - [error] module could not be initialized")

    # ###################################################################################
    # USER CODE SECTION 1 - START                                   
    # Use this section to define properties
    # ################################################################################### 


    # ###################################################################################
    # USER CODE SECTION 1 - END                                     
    # ###################################################################################

    # ###################################################################################
    # USER CODE SECTION 2 - START                                   
    #      Use this section to define methods(functions)
    # ###################################################################################

    def init(self,**kargs):
        print ("Dummy Data Generator Init")
        pass

    def random_string(self,length):
        return self.flexistack.helper.generate_random_string(length)

    # ##################################################################
    # USER CODE SECTION 2 - END                                     
    # ##################################################################                                   