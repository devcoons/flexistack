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
import sys
import copy
import time
import json
import datetime
import importlib
import subprocess
import argparse

from os import listdir
from os.path import abspath, dirname, isfile, join
from genericpath import isdir

#########################################################################################
# CLASS
#########################################################################################

class Action:

    # FlexiStack action details
    # required from autoloader
    autoload = {
        "description": 'Display the application version',
        "as_optional": 'store_true'
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

    # ##################################################################
    # USER CODE SECTION 1 - END                                     
    # ##################################################################

    # ##################################################################
    # USER CODE SECTION 2 - START                                   
    # ##################################################################
    # Use this section to define methods(functions)

    def init(self,**kargs):
        return True         

    # --------------------------------------------------------------------------------- #

    def run(self,**kargs):
        print("Application - Testing application")
        print(" - Available actions: "+str(len(self.flexistack.actions)))
        for action in self.flexistack.actions:
            if self.flexistack.actions[action].Action.autoload.get("as_optional") == None:
                print("  - "+action+": "+self.flexistack.actions[action].Action.autoload.get("description"))
            else:
                print("  - --"+action+": "+self.flexistack.actions[action].Action.autoload.get("description"))    
        print(" - Available plugins: "+str(len(self.flexistack.plugins)))   
        for plugin in self.flexistack.plugins:
            versions = self.flexistack.plugins[plugin].versions()
            versions.sort(reverse=False)
            for v in versions:
                rv = self.flexistack.plugins[plugin][v].d
                if rv == None or rv == "":
                    rv = "No available description"
                print("  - "+plugin+" ("+str(v)+"): "+rv)

        return True

    # ##################################################################
    # USER CODE SECTION 2 - END                                     
    # ##################################################################

#########################################################################################
# EOF
#########################################################################################         