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
(Note if you directly cloned it yourself, you'll need to edit ./helpers/extension_constants.py)
But reactjo extend does this automatically.

2. Make some changes
3. Update this readme.md
  3a. Fill in the json object below.
  3b. Remove this whole "If you want to create a new extension" section after you finish reading it.
4. Push it to a new github repo

That's it! People can now use it as a Reactjo extension.

# If you want to install a new extension into a project

1. Initialize reactjo if you haven't already
```bash
reactjo init
```

2. In reactjorc/config.json, add this to the extensions array:

```
{
    "uri": "https://github.com/your-name/your-extensions-repo.git",
    "rc_home": "extension_name_here"
    "branch": "master"
}
```
Note that branch is optional and defaults to master.

3. Back in your terminal, run:
```
reactjo update
```

# Usage

```bash
reactjo new # prints "hello world"
```
