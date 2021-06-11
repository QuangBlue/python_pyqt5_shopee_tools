from setuptools import setup

APP = ['main.py']

DATA_FILES = ['icon.ico']

OPTIONS = {'iconfile' : 'icon.ico'}

setup (
    app = APP,
    data_files = DATA_FILES,
    options = {'py2app' : OPTIONS},
    setup_requires = ['py2app'],

)
