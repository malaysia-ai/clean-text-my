import os
import json
import requests
from clean_text_my.logging import logger
from clean_text_my.utils import create_dir, is_endwith_slash, slash


def json_download(url: list, output_folder: str):
    if not is_endwith_slash(output_folder):
        output_folder = f"{output_folder}{slash()}"

    create_dir(output_folder)

    if not isinstance(url, list):
        raise Exception("url must in list")

    for l in url:
        response = requests.get(l)
        save_to = os.path.join(output_folder, l.rsplit("/", 1)[-1])

        open(save_to, "wb").write(response.content)
        logger.info(f"Download completed for {l}")
