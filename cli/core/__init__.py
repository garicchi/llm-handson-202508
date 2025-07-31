from pathlib import Path
import os


def get_root_path() -> Path:
    return Path(__file__).resolve().parent.parent.parent

def get_venv_path() -> Path:
    return get_root_path() / 'venv'

def get_venv_bin_dir() -> Path:
    venv_dir = get_venv_path()
    if os.name == 'nt':
        return venv_dir / 'Scripts'
    return venv_dir / 'bin'

def get_pip_path() -> Path:
    if os.name == 'nt':
        return get_venv_bin_dir() / 'pip.exe'
    return get_venv_bin_dir() / 'pip3'

def get_venv_python_path() -> Path:
    if os.name == 'nt':
        return get_venv_bin_dir() / 'python.exe'
    return get_venv_bin_dir() / 'python3'

def get_root_python_path() -> Path:
    if os.name == 'nt':
        return 'python.exe'
    return 'python3'