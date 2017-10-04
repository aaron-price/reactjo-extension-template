# If you want to create a new extension
## Create and publish


1. Clone the template
```bash
reactjo extend
# Name the extension
cd extension_name
```
(Note if you directly cloned it yourself, you'll need to edit ./helpers/extension_constants.py)
But `reactjo extend` does this automatically.

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
**file_manager(
    <string> output_file_or_path,
    <string> query,
    [<string/dict> input_file_or_path]
)**
Use this for super simple file manipulation.

Example:
Suppose your project is called "project", and your extension creates an app called "app"
The file structure might look like this:
/venv
/project
    /app
        /index.html
        ...
/reactjorc
    /config.json
    /extensions/
        /your_extension_name
            /assets
                /foo.txt

But what if you want to copy your foobar.txt asset into your app directory right beside index.html? This is VERY common problem when scaffolding. Here's the solution.

Open up commands/new.py and put this in your function.

``` python
from helpers.file_manager import file_manager as f
f('$out/foobar.txt', 'w', '$assets/foobar.txt')
```

Now when the end user runs `reactjo new`, the foobar.txt file will be in project/app/

You're probably wondering about '$out' and '$assets'. Those are just shortcuts courtesy of helpers/path_manager.py. Check it out to see more. You can add your own shortcuts there.

The second argument, 'w', is the query, and it's short for 'write'.

So in this case, it's saying "In the output file (/path/to/app/foobar.txt), write the input file (/path/to/reactjorc/extensions/your_extension/assets/foobar.txt)". Since the output file doesn't exist, it creates it. You could have named it anything you wanted.

Some other queries are:
**append**: f(path, 'a', <string|dict>) Adds the input to the end of the input file
**exists**: f(path, 'exists') Returns true or false. Checks both files and directories
**write**: f(path, 'w', <string|dict>) Creates or overwrites the output file with the input
**delete**: f(path, 'd') Deletes the file
**prepend**: f(path, 'p', <string|dict>) Adds the input to the beginning of the input file
**read**: f(path, 'r') Returns the file as a string
**path**: f(path, '$') Returns the absolute path, even when you give it a shortcut path.
**format**: f(path, 'f', <dict>) *

* Formatting: Wrap text like <% this %>, and you can replace it... because python's string.format() doesn't work as well when formatting python files with existing dicts. Takes a dict input like {'this': 'something else'}

It gets crazier than that though! If your input is a dictionary, you can do some pretty advanced manipulations.

Example settings.py
```python
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

You *could* just add an append line at the bottom of the file, but that doesn't look nice, especially in a settings or config file. Here's a better solution.

```python
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

Note the comma was added automatically. You might not know whether a trailing comma exists, so file_manager checks for you and adds it if necessary. You do need to add your own newline and indentation though.

You're also not limited to a particular filetype. The same would work in settings.js etc.

A similar effect can be achieved with 'w', to overwrite just a single line! One common example from reactjo-nextjs:
```javascript
import React from 'react'

const items = []      // <= You need that to say const items = ['name', 'email']

const Component = (props) => {
  ...
}
```

Okie dokes, here we go:

```python
  data = {
      'target': 'const items',
      'content': "const items = ['name', 'email']"
  }
  f($out/component.js, 'w', data)
```
File manager looks for the first line that starts with data['target'], and replaces that entire line with the string in data['content']

#### config_manager
Intelligently finds the nearest reactjorc/config.json file so you can access it from pretty much anywhere.

```python
from helpers.config_manager import get_cfg, set_cfg
# loads the config file as a dict
cfg = get_cfg()

cfg['new_key'] = 'new value'
project_name = cfg['project_name']

# Updates the config file. This may affect other extensions, so be careful.
set_cfg(cfg)
```

#### ui
Provides type specific inputs.
The first argument is the question to ask the end user.

Adding a secondary argument makes it optional, and uses the second argument as the default.

The exception is the options_input which takes a list of options as the second argument, and the optional default as the third.

```python
from helpers.ui import string_input, boolean_input, options_input
# prints What's your name?:
mandatory_string = string_input('What\'s your name?')

# prints 'What's the best colour ever? (default Neon Green):'
optional_string = string_input('What\'s the best colour ever?', 'Neon Green')

# prints 'Are you an admin (y/n):'
mandatory_boolean = boolean_input('Are you an admin?')

# prints 'Do you like python? (y/n default y):'
optional_boolean = boolean_input('Do you like python?', 'y')

# prints:
# red
# green
# blue
# Pick a colour:
mandatory_options = options_input('Pick a colour', ['red','green','blue'])

# prints:
# red
# green
# blue
# Pick a colour (default red):
optional_options = options_input('Pick a colour', ['red','green','blue'], 'red')
```

#### worklist
Pass a string to worklist describing what your code just did.

When the current `reactjo <cmd>` finishes running, reactjo core prints a friendly list of everything that just happened.

```
from helpers.worklist import worklist as wl
# Do something awesome
...

wl('Did something really cool!')
```
