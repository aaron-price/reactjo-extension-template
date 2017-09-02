import sys, os, shutil


ext_name = sys.argv[1]
fm_asset = open(os.getcwd() + '/unpack/file_manager.py', 'r').read()

# The usual format() won't work because of other dicts in the file.
fm_asset = fm_asset.replace("<%ext_name%>", "'" + ext_name + "'")

file = open(os.getcwd() + '/helpers/file_manager.py', 'w')
file.write(fm_asset)
file.close()

shutil.rmtree(os.getcwd() + '/unpack')
os.remove(os.getcwd() + '/unpack.py')
