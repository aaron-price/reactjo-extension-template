from commands.new import new
import sys

cmd = sys.argv[1]
if cmd in ['new']:
	new()
elif cmd in ['-v', '--version']:
	print('extension_name_here', 'v0.0.1')
