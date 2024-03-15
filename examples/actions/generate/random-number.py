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

class Action:

    # FlexiStack action details
    # required from autoloader
    autoload = {
        "description": 'Generate a random number'
    }

    # Dynamically loaded modules 
    # Do not modify (auto-populated)
    flexistack = None

    # Required modules list 
    #   Modify this list according to the
    #   need of this module
    req_plugins = []

    def __init__(self, flexistack):
        try:
            self.flexistack = flexistack
            if len(self.req_plugins) == 0 or flexistack == None:
                return
            if (set(self.req_plugins) - self.flexistack.plugins.keys()):
                print(str(self.__class__)+" - [warn] missing required modules")
        except:
            print(str(self.__class__)+" - [errn] action could not be loaded")

    # ##################################################################
    # USER CODE SECTION 1 - START                                   
    # ##################################################################
    # Use this section to define properties

    length = None

    # ##################################################################
    # USER CODE SECTION 1 - END                                     
    # ##################################################################

    # ##################################################################
    # USER CODE SECTION 2 - START                                   
    # ##################################################################
    # Use this section to define methods(functions)
  
    def set_optional_arguments(self, parser,modules):
        parser.add_argument('-l','--length', action='store', help="Requested number length")

    # --------------------------------------------------------------------------------- #
        
    def init(self,**kargs):
        try:
            args = kargs['pargs']
            if ('length' in args):
                self.length = int(args['length'])
                return True
        except:
            pass
        return False         

    # --------------------------------------------------------------------------------- #

    def run(self,**kargs):
        dummy_generator = self.flexistack.plugins['dummy-generator'].latest(self.flexistack)
        print(dummy_generator.random_number(self.length))
        return True

    # ##################################################################
    # USER CODE SECTION 2 - END                                     
    # ##################################################################


    
#########################################################################################
# EOF
#########################################################################################         