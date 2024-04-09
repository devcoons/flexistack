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
# IMPORTS                                                                               #
#########################################################################################

import random
from flexistack import *

#########################################################################################
# SAFE-IMPORTS                                                                          #
#########################################################################################

#########################################################################################
# CLASS                                                                                 #
#########################################################################################

@flexi_action(None, 'Shuffle a given string')
class Action:

    # ###################################################################################
    # USER CODE SECTION 1 - START                                                       #
    # Use this section to define properties                                             #
    # ###################################################################################

    data = None
    
    # ###################################################################################
    # USER CODE SECTION 1 - END                                                         #
    # ###################################################################################

    # ###################################################################################
    # USER CODE SECTION 2 - START                                                       #
    #      Use this section to define methods(functions)                                #
    # ###################################################################################

    def set_optional_arguments(self, parser,modules):
        parser.add_argument('-d',
                            '--data', 
                            action='store', 
                            help="Input data")

    # --------------------------------------------------------------------------------- #
        
    def init(self,**kargs):
        try:
            args = kargs['pargs']
            if ('data' in args):
                self.data = args['data']
                return True
        except:
            pass
        return False          
     
    # --------------------------------------------------------------------------------- #

    def run(self,**kargs):
        char_list = list(self.data)    
        random.shuffle(char_list)
        print( ''.join(char_list))
        return True

    # ###################################################################################
    # USER CODE SECTION 2 - END                                                         #
    # ###################################################################################

#########################################################################################
# EOF                                                                                   #
#########################################################################################      