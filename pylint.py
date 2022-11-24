import os
import glob

os.system('cmd /c')

for fileName in  glob.glob('./**/*.py', recursive=True):
    os.system(f'\"pylint "{fileName}"\"')

os.system('cmd /k')
