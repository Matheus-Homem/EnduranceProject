import os
import shutil
from typing import List, Iterator, Tuple

def get_absolute_path(path: str) -> str:
    return os.path.abspath(path)

def get_environment_variable(var: str, default: str=None) -> str:
    return os.environ.get(var, default)

def join_paths(*paths) -> str:
    return os.path.join(*paths)

def list_directory_contents(path: str) -> List[str]:
    return os.listdir(path)

def explore_directory(base_path: str) -> Iterator[Tuple[str, List[str], List[str]]]:
    return os.walk(base_path)

def is_path_valid(path: str) -> bool:
    return os.path.exists(path)

def is_file(path: str) -> bool:
    return os.path.isfile(path)

def is_directory(path: str) -> bool:
    return os.path.isdir(path)

def extract_basename(path:str) -> str:
    return os.path.basename(path)

def remove_path_if_exists(path: str) -> None:
    if os.path.exists(path):
        shutil.rmtree(path)