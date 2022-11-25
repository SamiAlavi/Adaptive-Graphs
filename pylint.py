import os
import glob

os.system('cmd /c')

for fileName in  glob.glob('./**/*.py', recursive=True):
    print(f'========== {fileName} ==========')
    os.system(f'\"pylint "{fileName}"\"')

os.system('cmd /k')
