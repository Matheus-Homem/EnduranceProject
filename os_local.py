import os
from typing import List

def get_absolute_path(path: str) -> str:
    return os.path.abspath(path)

def get_environment_variable(var: str, default: str=None) -> str:
    return os.environ.get(var, default)

def join_paths(*paths) -> str:
    return os.path.join(*paths)

def list_directory_contents(path: str) -> List[str]:
    return os.listdir(path)

def is_path_valid(path: str) -> bool:
    return os.path.exists(path)

def is_file(path: str) -> bool:
    return os.path.isfile(path)

def is_directory(path: str) -> bool:
    return os.path.isdir(path)