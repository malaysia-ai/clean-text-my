import os
import json
import sys
import subprocess
import clean_text_my
from clean_text_my.logging import logger
from clean_text_my.utils import create_dir, slash, is_endwith_slash, platform_name
from datasets import Dataset, load_from_disk


def dir_format(path):
    if not is_endwith_slash(path):
        path = f"{path}{slash()}"

    return path


def jsonl_to_datasets(input_folder: str, output_folder: str) -> None:
    dir_format(input_folder)
    dir_format(output_folder)
    create_dir(output_folder)

    try:
        for root, _, files in os.walk(input_folder):
            for filename in files:
                if filename.endswith(".jsonl"):
                    file_path = os.path.join(root, filename)

                    dataset_name = os.path.splitext(filename)[0]
                    try:
                        with open(file_path) as file:
                            data = [json.loads(line) for line in file]

                        data_dict = {"text": [entry["text"] for entry in data]}

                        dataset = Dataset.from_dict(data_dict)

                        output_folder_path = os.path.join(output_folder, dataset_name)
                        dataset.save_to_disk(output_folder_path)

                        logger.info(f"Dataset saved to {output_folder_path}")
                    except Exception as e:
                        logger.error(
                            f"Error creating dataset for file {file_path}: {e}"
                        )
                        continue
    except Exception as e:
        logger.error(f"Error processing folder {input_folder}: {e}")


def data_deduplication(
    input_folder: str,
    output_folder: str,
    batch_size: int = 10000,
    threshold: float = 0.95,
    min_length: int = 1,
    local: bool = True,
) -> None:
    python_exe = sys.executable

    input_folder = dir_format(input_folder)
    output_folder = dir_format(output_folder)
    create_dir(output_folder)

    try:
        dataset_names = os.listdir(input_folder)
        for dataset_name in dataset_names:
            dataset_path = os.path.join(input_folder, dataset_name)

            if os.path.isdir(dataset_path):
                output_dataset_path = f"{output_folder}{dataset_name}"

                # Construct the command for running minhash.py
                if local:
                    command = f"{python_exe} -m clean_text_my.text_dedup.minhash \
                            --path '{dataset_path}' \
                            --split train \
                            --cache_dir ./cache \
                            --output '{output_dataset_path}' \
                            --column text \
                            --batch_size {str(batch_size)} \
                            --threshold {str(threshold)} \
                            --min_length {str(min_length)} \
                            --local"
                else:
                    command = f"{python_exe} -m clean_text_my.text_dedup.minhash \
                            --path '{dataset_path}' \
                            --split train \
                            --cache_dir ./cache \
                            --output '{output_dataset_path}' \
                            --column text \
                            --batch_size {str(batch_size)} \
                            --threshold {str(threshold)} \
                            --min_length {str(min_length)}"

                # Run the minhash.py script using subprocess
                subprocess.run(command, shell=True)

                logger.info(f"Deduplication completed for {dataset_name}")

    except Exception as e:
        logger.error(f"Error during deduplication: {e}")
