import sys, os, shutil


ext_name = sys.argv[1]
fm_file = open(os.getcwd() + '/helpers/file_manager.py', 'r').read()

# The usual format() won't work because of other dicts in the file.
fm_asset = fm_asset.replace("your_extension_name", ext_name)

file = open(os.getcwd() + '/helpers/file_manager.py', 'w')
file.write(fm_asset)
file.close()
