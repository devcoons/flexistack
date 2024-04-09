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

from flexistack import *

#########################################################################################
# SAFE-IMPORTS                                                                          #
#########################################################################################

#########################################################################################
# CLASS                                                                                 #
#########################################################################################

@flexi_plugin("dummy-generator", '0.2', "This a better dummy data generator plugin")
class Plugin():

    # ###################################################################################
    # USER CODE SECTION 1 - START                                                       #
    # Use this section to define properties                                             #
    # ###################################################################################

    # ###################################################################################
    # USER CODE SECTION 1 - END                                                         #
    # ###################################################################################

    # ###################################################################################
    # USER CODE SECTION 2 - START                                                       #
    #      Use this section to define methods(functions)                                #
    # ###################################################################################

    def init(self,**kargs):
        print ("Dummy Data Generator Init")
        pass

    def random_string(self,length):
        return self.flexistack.helper.generate_random_string(length)

    def random_number(self,length):
        return self.flexistack.helper.generate_random_number(length)
    
    # ###################################################################################
    # USER CODE SECTION 2 - END                                                         #
    # ###################################################################################

#########################################################################################
# EOF                                                                                   #
#########################################################################################