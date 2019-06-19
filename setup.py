from setuptools import setup, find_packages
#import os
#import sys
#import shutil

print("Done downloading linkBudget project from git!")
setup(
   name = "linkBudget",
   version = '1.0',
   url = 'https://github.com/adriankaisinclair/linkBudget',
   license = 'BSD 3',
   author = "Adrian Sinclair",
   author_email = "aksincla@asu.edu",
   packages = [],
   package_data = {
   '' : ['*.py','*.md','*.pdf'],
   },
   install_requires=['numpy', 'matplotlib','SchemDraw']
   ,
   description = "Link budget calculator for cascaded microwave systems"
)
