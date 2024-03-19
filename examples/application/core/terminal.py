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

import os
import sys
import re
import json
import time
import string
import datetime
from threading import Lock
from flexistack import safe_import

#########################################################################################
# SAFE-IMPORTS                                                                          #
#########################################################################################

safe_import("colorama")
from colorama import just_fix_windows_console

#########################################################################################
# CLASS                                                                                 #
#########################################################################################

class Terminal:
    
    # FlexiStack middleware details required by the framework
    _flexi_ = { 'type'           : "middleware", 
                'description'    : "" }
    
    # Constructor
    #   Only core operations to ensure that the current module
    #   is set as a property in framework's middleware
    def __init__(self, middleware):
        setattr(middleware, self.__class__.__name__.lower(), self)
        if hasattr(self, 'init'):
            self.init()
        
    # ###################################################################################
    # USER CODE SECTION 1 - START                                                       #
    # Use this section to define properties                                             #
    # ###################################################################################

    C_RD        = "\033[31m"
    C_GR        = "\033[32m"           
    C_YW        = "\033[33m"     
    C_BL        = "\033[34m"  
    C_MG        = "\033[35m"  
    C_CB        = "\033[36m" 
    C_BB        = "\033[90m"
    C_BW        = "\033[97m"
    F_SU        = "\033[4m"
    F_EU        = "\033[24m"    
    RST         = "\033[0m"
    INV         = "\033[7m"
    NRM         = "\033[27m"

    # --------------------------------------------------------------------------------- #

    supports_ansi   = False
    max_columns     = 118

    current_mode    = -1
    loop_max_sz     = 8
    text_buff       = []
    lock_print      = None
    
    # ###################################################################################
    # USER CODE SECTION 1 - END                                                         #
    # ###################################################################################

    # ###################################################################################
    # USER CODE SECTION 2 - START                                                       #
    #      Use this section to define methods(functions)                                #
    # ###################################################################################
    
    def init(self):
        try:
            self.lock_print = Lock()
            if sys.platform.startswith("win"):
                just_fix_windows_console()
                import ctypes
                kernel32 = ctypes.windll.kernel32
                _mode = ctypes.c_uint32()
                kernel32.GetConsoleMode(kernel32.GetStdHandle(-11), 
                                        ctypes.byref(_mode))
                self.supports_ansi = _mode.value & 0x0004 != 0
            else:
                self.supports_ansi = True  
            print("",end="", flush=True)
            try:
                self.max_columns = os.get_terminal_size().columns-2
            except:
                self.max_columns = 118            
            return True
        except:
            return False

    # --------------------------------------------------------------------------------- #
        
    def set_mode(self):
        pass
        
    # --------------------------------------------------------------------------------- #
    
    def print(self, args):
        self.lock_print.acquire()
        print(args)
        self.lock_print.release()
        pass
        
    # ###################################################################################
    # USER CODE SECTION 2 - END                                                         #
    # ###################################################################################

#########################################################################################
# EOF                                                                                   #
#########################################################################################
