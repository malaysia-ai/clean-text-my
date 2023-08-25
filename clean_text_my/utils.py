import os
import re
import json
import subprocess
from tqdm import tqdm
from pathlib import Path
from sys import platform


def platform_name() -> str:
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        return "linux"
    elif platform == "win32":
        return "windows"


def is_dir(path: str) -> bool:
    return os.path.isdir(path)


def is_endwith_slash(path: str) -> bool:
    if platform_name() == "windows":
        return path.endswith("\\")
    elif platform_name() == "linux":
        return path.endswith("/")


def slash() -> str:
    if platform_name() == "windows":
        return "\\"
    elif platform_name() == "linux":
        return "/"


def is_additional_slash(path) -> str:
    if not is_endwith_slash(path):
        path = f"{path}{slash()}"

    return path


def create_dir(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)


def write_to_json(data_list: list, filename: str) -> None:
    with open(filename, "w+") as file:
        for item in tqdm(data_list):
            x = json.dumps(item, ensure_ascii=False)
            file.write(x + "\n")
