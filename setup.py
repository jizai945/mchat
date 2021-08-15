import sys
import os
from cx_Freeze import setup, Executable

# ADD FILES
files = ['icon.ico', 'settings.json', 'gui/']

# TARGET
target = Executable(
    script="main.py",
    base="Win32GUI",
    icon="icon.ico"
)

# SETUP CX FREEZE
setup(
    name = "mchat",
    version = "0.0.0",
    description = "mini chat",
    author = "Timo",
    options = {'build_exe' : {'include_files' : files}},
    executables = [target]
    
)
