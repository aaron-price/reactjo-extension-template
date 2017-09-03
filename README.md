# Start with this if you haven't already

```bash
virtualenv venv
source venv/bin/activate
pip install reactjo
```

# If you want to create a new extension

1. Clone the template
```bash
reactjo extend
cd template
```
(Note if you directly cloned it yourself, you'll need to run:
`python path/to/unpack.py your_extension_name`)
But reactjo extend does this automatically.

2. Make some changes
3. Remove the existing remote origin with `git remote rm origin`
4. Make a new repo on github
5. Set it as the new remote origin `git remote add origin https://github.com/your_name/you_repo.git`
6. Push the template to the new repo
That's it! People can now use it as a Reactjo extension.

# If you want to install a new extension into a project

1. Initialize reactjo if you haven't already
```bash
reactjo init
```

2. In reactjorc/config.json, add this to the extensions array:

```
{
    "output_home": "your_extension_title_NO_SPACES_ALLOWED",
    "rc_home": "path/starting/at/project/root",
    "uri": "https://github.com/your-name/your-extensions-repo.git",
    "branch": "master",
    "serve": "command to run the server"
}
```
Note that branch, home, and serve, are all optional.
Branch will default to master
Home will default to your extension name
Serve will only be used if you add it.

3. Back in your terminal, run:
```
reactjo update
```

# Usage

```bash
reactjo new # prints "hello world"
```

# Configure
The extension object you add to config.json can be configured easily.

### output_home
Refers to super_root/project_name/output_home_goes_here/

If you use the file_manager helper, you can get a shortcut to it with $out
For example, if output_home = 'foo', then:
`file_manager('$out/assets')`
will return the path 'super_root/project_name/foo/'

### rc_home
Refers to super_root/reactjorc/extensions/rc_home_goes_here

If you use the file_manager helper, you can get a shortcut to it with $rc
For example, if rc_home = 'foo', then:
`file_manager('$rc/assets')`
will return the path '/super_root/reactjorc/foo/assets/'

### uri
The link to you extension's repo.
When the user runs `reactjo init` or `reactjo update`, it'll clone the repo into super_root/reactjorc/extensions/rc_home where rc_home is whatever you call it.

### branch (optional)
Default: master
If you want people to only use a specific branch in your repo, enter it here.

### serve (optional)
If your extension has a server, you can give the script to run it here.
When a user of your extension runs `reactjo server`, reactjo will go through each of the extensions. For each one with a serve field, it will cd into their output_home and run the serve command as a subprocess.
