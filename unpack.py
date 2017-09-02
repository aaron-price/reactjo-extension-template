import sys
import os
import shutil

ext_name = sys.argv[1]
template_path = os.getcwd() + '/' + ext_name
fm_asset = open(template_path + '/unpack/file_manager.py', 'r').read().format(
    ext_name=ext_name,
)
file = open(template_path + '/helpers/file_manager.py', 'w')
file.write(fm_asset)
file.close()

shutil.rmtree(template_path + '/unpack')
