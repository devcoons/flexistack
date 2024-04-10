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
import hashlib
import platform
import random
import string
import psutil
import pyaes
import base64

#########################################################################################
# CLASS                                                                                 #
#########################################################################################

class Helper:
    """
    A collection of commonly used helper functions.
    """ 
    
    def resolve_path(path):
        """ 
        Resolves the given path, resolving any symbolic links if present.
        """
        y = os.path.normpath(os.path.abspath(path)).split("\\")
        p=""
        for i in y:
            if i.endswith(":"):
                i=i+"/"
            p = os.path.normpath(os.path.join(p,i))
            if os.path.exists(p) == False:
                if os.path.exists(p+".lnk") == True:
                    p = Helper.shortcut_resolver(p+".lnk")
        return p

    # --------------------------------------------------------------------------------- #

    def shortcut_resolver(item):
        """
        Resolves the given shortcut item to its target path, considering the operating system.
        """
        system = platform.system()
        if system == "Linux":
            return os.path.realpath(item)
        elif system == "Windows":
            import win32com.client
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(item)
            return shortcut.TargetPath
        else:
            return None

    # --------------------------------------------------------------------------------- #
        
    def get_total_cpu():
        """
        Returns the total number of CPU cores, including logical and physical cores.
        """
        return [psutil.cpu_count(logical=False), psutil.cpu_count()]

    # --------------------------------------------------------------------------------- #

    def generate_random_string(length):
        """
        Generates a random string of specified length using ASCII letters and digits.
        """
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string

    # --------------------------------------------------------------------------------- #

    def generate_random_number(length):
        """
        Generates a random string of specified length using ASCII letters and digits.
        """
        characters =  string.digits
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string
    
    # --------------------------------------------------------------------------------- #

    def get_total_mem():
        """
        Returns the total virtual and swap memory in gigabytes.
        """
        virtual = round(psutil.virtual_memory().total / (1024*1024*1024), 1)
        swap = round(psutil.swap_memory().total / (1024*1024*1024), 1)
        return [virtual, swap]

    # --------------------------------------------------------------------------------- #

    def filehash_md5(fname):
        """
        Computes the MD5 hash of the specified file.
        """
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    # --------------------------------------------------------------------------------- #

    def filehash_sha256(fname):
        """
        Computes the SHA-256 hash of the specified file.
        """
        hash_256 = hashlib.sha256()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4*65536), b""):
                hash_256.update(chunk)
        return hash_256.hexdigest()

    # --------------------------------------------------------------------------------- #

    def encrypt(key, plaintext):
        """
        Encrypts the plaintext using AES algorithm with the provided key.
        """
        hash_256 = hashlib.sha256()
        hash_256.update(key.encode('utf-8'))
        key = hash_256.digest()
        aes = pyaes.AESModeOfOperationCTR(key)
        ciphertext = aes.encrypt(plaintext)
        return base64.b64encode(ciphertext).decode('ascii')

    # --------------------------------------------------------------------------------- #

    def decrypt(key, ciphertextb64):
        """
        Decrypts the base64 encoded ciphertext using AES algorithm with the provided key.
        """
        hash_256 = hashlib.sha256()
        hash_256.update(key.encode('utf-8'))
        key = hash_256.digest()
        aes = pyaes.AESModeOfOperationCTR(key)
        ciphertext = base64.b64decode(ciphertextb64)
        return aes.decrypt(ciphertext).decode('utf-8')

    # --------------------------------------------------------------------------------- #

    def split_into_slices(A, slices):
        """
        Splits the given list into slices as per the provided slices parameter.
        """
        r = []
        num_elements = len(A)
        if num_elements == slices:
            return A.copy()
        if num_elements > slices:
            sl = num_elements // slices
            nb = 0
            for _ in range(slices):
                v = 0
                for _ in range(sl):
                    v |= A[nb] << (8 // sl) * (sl - 1)
                    nb += 1
                r.append(v)
            return r
        if num_elements < slices:
            sl = slices // num_elements
            mb = 8 // sl
            am = (1 << mb) - 1
            for e in A:
                for _ in range(sl):
                    r.append((e & (am << (8 - mb))) >> (8 - mb))
            return r
        return None  
    
#########################################################################################
# END OF FILE                                                                           #
#########################################################################################