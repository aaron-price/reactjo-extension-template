from tests.config_mock import setup_config, teardown_config
from helpers.path_manager import get_path, mkdir, ls
import os

def test_mkdir():
    setup_config()
    mkdir('tests/sandbox/path_manager', 'pm')
    assert(os.path.exists('tests/sandbox/path_manager'))

    from helpers.config_manager import get_cfg
    assert('pm' in get_cfg()['paths'].keys())

teardown_config()
