import sys
import os
import shutil
project_name = sys.argv[1]
ext_name = sys.argv[2]

fm_asset = open(os.getcwd() + '/unpack/file_manager.py', 'r').read().format(
    ext_name=ext_name
)
file = open(os.getcwd() + '/helpers/file_manager.py', 'w')
file.write(fm_asset)
file.close()

shutil.rmtree(os.getcwd() + '/unpack')
