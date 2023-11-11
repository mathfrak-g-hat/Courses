## Python file I/O
## AJ Zerouali 2021/05/30
## Description: Basic *.txt file manipulations.

# Working directory and filename constants
dirAddress = 'C:\\Users\\zaj20\\Documents\\Python\\First steps' # Double backslash to avoid conflict with special char
txtFileName = 'IO_Example_0.txt'

# First way of opening files 
myFile = open(dirAddress+'\\'+txtFileName, 'r') # Read mode.
myFile.read() # Will print a long string of contents