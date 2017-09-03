# If you want to create a new extension
## Create and publish


1. Clone the template
```bash
reactjo extend
# Name the extension
cd extension_name
```
(Note if you directly cloned it yourself, you'll need to edit ./helpers/extension_constants.py)
But reactjo extend does this automatically.

2. Make some changes.
3. Update this README.md.
  3a. Update the github uri in the json object below.
  3b. Document the commands you use under # Usage
4. Push the extension to a new github repo matching the uri you specified in 3a.

That's it! People can now use it as a Reactjo extension by adding that object to their config.json extensions array.

## Commands

To listen to a new reactjo command, edit extension_name_here/entry.py.
You should probably add a module for the command under extension_name_here/commands/

## Helpers
#### file_manager

automatically uses the path_manager helper. Use this for super simple file manipulation.
For example to copy your foobar.txt asset into your main output directory:
```
from helpers.file_manager import file_manager as f
f('$out/foobar.txt', 'w', '$assets/foobar.txt')
```
As you can see the basic syntax is f(output path, query type, optional input).
The $out and $assets are shortcuts courtesy of path_manager. Check it out to see more.
So in this case, it's saying "In the output file, write the input file."

Some other queries are:
a: append. Takes a string or dict
exists: Boolean check a path or file exists
w: write. Takes a string or dict
d: delete
f: format. Wrap text like <% this %>, and you can format it... because python's .format doesn't work as well when formatting python files with existing dicts. Takes a dict input like {'this': 'something else'}
p: prepend. Takes a string or dict.
r: read.

It gets crazier than that though! If your input is a dictionary, you can do some pretty advanced manipulations.

Let's say you want to append something to a dictionary, inside a list, inside another dictionary, in an existing file. You *could* just add an append line at the bottom, but that doesn't look nice, especially in a settings or config file.

```settings.py
OPTIONS = {
  'cool': 124,
  'my_list': [
    'asdfasdf',
    {
      'foo': {...}      # <- You need a new entry below foo
    }
  ]
}
```

Easy.
```

data = {
      'target': ['OPTIONS', 'my_list', 1],
      'content': "\n      'custom': 'something custom'"
  }
  f($out/settings.py, 'a', data)
```

New file will be:

```settings.py
OPTIONS = {
  'cool': 124,
  'my_list': [
    'asdfasdf',
    {
      'foo': {...},
      'custom': 'something custom'
    }
  ]
}
```
