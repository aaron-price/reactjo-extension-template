from helpers.config_manager import get_cfg, set_cfg
from helpers.extension_constants import OUTPUT_HOME, RC_HOME
import os

# /                                                         $su
# /prj_name                                                 $prj
# /prj_name/reactjorc/                                      $rc
# /prj_name/reactjorc/extensions/RC_HOME                    $ext
# /prj_name/reactjorc/extensions/RC_HOME/assets             $assets
# /prj_name/output_name                                     $out

# USAGE:
# from file_manager import file_manager as f
# f('$assets/foo.txt', '$')    # Returns the foo.txt PATH as a string
# f('$assets/foo.txt', 'r')    # Returns the foo.txt FILE as a string

def parse_shortcuts(path):
    cfg = get_cfg()
    su_path = cfg['paths']['super_root']
    rc = os.path.join(su_path, 'reactjorc')
    prj_path = cfg['paths']['project_root']
    out_path = os.path.join(prj_path, OUTPUT_HOME)
    ext = os.path.join(rc, 'extensions', RC_HOME)
    assets = os.path.join(ext, 'assets')

    shortcuts = {
        '$su': su_path,
        '$project': prj_path,
        '$prj': prj_path,
        '$rc': rc,
        '$extension': ext,
        '$ext': ext,
        '$assets': assets,
        '$output': out_path,
        '$out': out_path,
    }

    parsed_string = path
    for key, value in shortcuts.items():
        parsed_string = os.path.join(parsed_string.replace(key, value))
    return parsed_string

def mkdir(path, name = None):
    path = parse_shortcuts(path)
    # Create directory
    if not os.path.exists(path):
        os.mkdir(path)

    # Create path entry in config
    cfg = get_cfg()
    if not name in cfg['paths'].keys() and name is not None:
        cfg['paths'][name] = path
        set_cfg(cfg)

def ls():
    print(" ")
    for name, path in get_cfg()['paths'].items():
        print(path, "\t|\tp(" + name + ")")
    print(" ")

def get_path(name):
    all_paths = get_cfg()['paths']
    path_names = all_paths.keys()
    ext_name = EXTENSION_NAME + "_" + name
    return ext_name if ext_name in all_paths else name
