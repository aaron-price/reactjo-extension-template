import os
import subprocess
from helpers.file_manager import get_path as p

def npm(args):
	os.chdir(p('package.json'))
	subprocess.call(['npm'] + args)

def manage(args):
	os.chdir(p('manage.py'))
	subprocess.call(['python', 'manage.py'] + args)

def pip(args):
	subprocess.call(['pip'] + args)

def startproject(name):
	os.chdir(p('super_root'))
	subprocess.call(['django-admin', 'startproject', name])
