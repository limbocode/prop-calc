#!/usr/bin/env python
import subprocess
    
    
    
def git_default():
    subprocess.call(['git','add','.'])
    subprocess.call(['git','commit','-m','update'])
    subprocess.call(['git','push','origin','master'])
    
def git_options():
    str1 = raw_input("Input message: ")
    subprocess.call(['git','add','.'])
    subprocess.call(['git','commit','-m',str1])
    subprocess.call(['git','push','origin','master'])
    
    
def input():
    str1 = "Press enter to continue with default settings.\n\
Type 1 and press enter to use your own settings."
    x = raw_input(str1)
    if x=='1':
        git_options()
    else:
        git_default()
        
        
        
if __name__ == "__main__":
    input()
    