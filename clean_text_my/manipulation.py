import os
import json
from glob import glob
from tqdm import tqdm
from clean_text_my.logging import logger
from clean_text_my.utils import write_to_json, is_additional_slash, create_dir


def data_flattening(
    output_folder: str,
    input_folder: str = None,
    input_filename: str = None,
    custom_key: list = None,
):
    suggested_keys = [
        "p",
        "text",
        "article_text",
        "article_body",
        "text",
        "content",
        "contents",
        "body",
        "articleBody",
        "data",
        "title",
    ]

    output_folder = is_additional_slash(output_folder)
    create_dir(output_folder)

    if input_filename and input_folder:
        raise Exception(
            f"please choose only one option: input_filename or input_folder"
        )

    if custom_key:
        suggested_keys = list(set(suggested_keys + custom_key))

    if input_folder:
        input_folder = is_additional_slash(input_folder)
        files_lst = glob(f"{input_folder}*.jsonl")
    elif input_filename:
        print(input_filename)
        if input_filename.endswith("jsonl"):
            files_lst = [input_filename]
        else:
            raise Exception(f"input_filename is not .jsonl format")
    else:
        raise Exception(f"input_folder and input_filename is none")

    txt_lst = []

    for f in files_lst:
        with open(f) as fopen:
            data = [json.loads(line) for line in fopen]

        try:
            key_data = [key for key, _ in data[0].items()]
            logger.info(f"availble key - {key_data}")
        except AttributeError:
            logger.error(f"dataset not in standard format, assumed got nested array.")
            continue

        if not any(key in key_data for key in suggested_keys):
            logger.error(
                f"dataset not in standard key-value. must have ({' | '.join(suggested_keys)})"
            )
            continue

        for i in tqdm(data):
            str_lst = []
            for key in i.keys():
                if key in suggested_keys:
                    str_lst.append(str(i[key]))
                else:
                    continue

            if None in str_lst:
                str_lst = ["None" if v is None else v for v in str_lst]

            str_data = "\n\n".join(str_lst)
            txt_lst.append({"text": f"{str_data}"})

        _, filename = os.path.split(f)
        write_to_json(txt_lst, f"{output_folder}{filename}")

        logger.info(f"Data flattening completed for {filename}")
