import sys 
import os
from cx_Freeze import setup, Executable

# ADD FILES
files = ['icon.ico','themes/']

# TARGET
target = Executable(
    script="main.py",
    icon="icon.ico"
)

# SETUP CX FREEZE
setup(
    name = "FastAz",
    version = "1.0",
    description = "Phần Mềm Quản Lý Bán Hàng",
    author = "QuangBlue",
    options = {'build_exe' : {'include_files' : files},
                'bdist_mac' : {'iconfile' : 'icon.ico'}
    },
    executables = [target]
)