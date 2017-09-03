from helpers.config_manager import get_cfg

def mkdir(path, name):
    # Create directory
    if not os.path.exists(path):
        os.mkdir(path)

    # Create path entry in config
    cfg = get_cfg()
    if not name in cfg['paths'].keys():
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
