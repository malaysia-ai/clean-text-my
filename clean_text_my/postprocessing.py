import os
import re
import json
import logging
from glob import glob
from clean_text_my.logging import logger
from clean_text_my.utils import create_dir, slash, is_endwith_slash, platform_name

http_errors = [
    "400 Bad Request",
    "401 Unauthorized",
    "402 Payment Required",
    "403 Forbidden",
    "404 Not Found",
    "405 Method Not Allowed",
    "406 Not Acceptable",
    "407 Proxy Authentication Required",
    "408 Request Timeout",
    "409 Conflict",
    "410 Gone",
    "411 Length Required",
    "412 Precondition Failed",
    "413 Payload Too Large",
    "414 URI Too Long",
    "415 Unsupported Media Type",
    "416 Range Not Satisfiable",
    "417 Expectation Failed",
    "418 I'm a teapot",
    "421 Misdirected Request",
    "422 Unprocessable Entity",
    "423 Locked",
    "424 Failed Dependency",
    "425 Too Early",
    "426 Upgrade Required",
    "428 Precondition Required",
    "429 Too Many Requests",
    "431 Request Header Fields Too Large",
    "451 Unavailable For Legal Reasons",
    "500 Internal Server Error",
    "501 Not Implemented",
    "502 Bad Gateway",
    "503 Service Unavailable",
    "504 Gateway Timeout",
    "505 HTTP Version Not Supported",
    "506 Variant Also Negotiates",
    "507 Insufficient Storage",
    "508 Loop Detected",
    "510 Not Extended",
    "511 Network Authentication Required",
]

rejected = [
    "Internal Server Error",
    "__NOEDITSECTION__",
    "enter your username and password",
    "forgotten your password",
    "cookies enabled",
    "enable JavaScript in your browser.",
    "The page cannot be displayed",
    "site or edit the error_page",
]


def replace(input_string: str) -> str:
    input_string = replace_multiple(input_string.replace("…", "."))
    input_string = replace_multiple(input_string, pattern=r"\.{6,}", replace="...")
    return input_string


def replace_multiple(input_string: str, pattern=r"\s{6,}", replace="   ") -> str:
    return re.sub(pattern, replace, input_string)


def reject(input_string: str) -> bool:
    rejected.extend(http_errors)
    if any([r in input_string for r in rejected]):
        return True
    return False


def process(input_folder: str):
    if not is_endwith_slash(input_folder):
        input_folder = f"{input_folder}{slash()}"

    FOLDER_POSTPROCESSING = os.path.join(input_folder, "postprocessing")
    FOLDER_POSTPROCESSING_DONE = os.path.join(input_folder, "postprocessing-done")

    create_dir(FOLDER_POSTPROCESSING)
    create_dir(FOLDER_POSTPROCESSING_DONE)

    files_lst = glob(f"{input_folder}*.jsonl")

    for f in files_lst:
        is_success = True

        directory, filename = os.path.split(f)
        filename_split = os.path.splitext(filename)
        new_done_dir = os.path.join(directory, "postprocessing-done")
        new_dir = os.path.join(directory, "postprocessing")

        new_f_done = os.path.join(new_done_dir, filename)
        new_f = os.path.join(new_dir, filename)

        if os.path.exists(new_f_done):
            logger.info(
                f"Postprocessing for {filename_split[0]} already done, skip ..."
            )
            continue

        with open(new_f, "w") as fopen_l:
            with open(f) as fopen:
                for l in fopen:
                    data = json.loads(l)

                    if "text" not in data:
                        logger.info(
                            f"Skip postprocessing for {filename_split[0]}, error (text) key not found in data"
                        )
                        os.remove(new_f)
                        is_success = False
                        break

                    if reject(data["text"]):
                        continue

                    data = replace(data["text"].strip())

                    if len(data) < 3:
                        continue

                    fopen_l.write(f"{json.dumps(data)}\n")
                    fopen_l.flush()

        if is_success:
            with open(new_f_done, "w") as fopen:
                fopen.write("done")

            logger.info(f"Postprocessing completed for {filename_split[0]}")
