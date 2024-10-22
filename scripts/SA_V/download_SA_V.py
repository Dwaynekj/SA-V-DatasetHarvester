# Automatically download the SA-V dataset
# by Stéphane Vujasinovic, Dwayne Jones


# - IMPORTS ---
import os
import yaml


# - FUNCTIONS ---
def read_yaml(path_to_yaml: str):
    with open(path_to_yaml, "r") as file:
        sav_link_collection = yaml.safe_load(file)
    return sav_link_collection


def download_datachunk(filename: str, url: str, work_dir: str):
    os.system(f' wget -O {work_dir}/{filename} "{url}"')


def extract_datachunk(filename: str, work_dir: str, file_destination: str):
    os.system(f' tar -xf {work_dir}/{filename} -C {file_destination}')


def clean_tar_chunk(filename: str, work_dir: str):
    os.system(f' rm {work_dir}/{filename}')


def download_and_extract_data_split(
    sav_link_collection: dict, 
    file_destination_dir: str, 
    tmp_dir: str,
    split: str
):
    sav_urls_split = sav_link_collection[split]
    for chunk_name, chunk_url in sav_urls_split.items():
        print(f"\n-- Downloading {chunk_name} from {chunk_url} --")
        download_datachunk(chunk_name, chunk_url, tmp_dir)
        print(f"\n-- Extracting {chunk_name} --")
        extract_datachunk(chunk_name, tmp_dir, file_destination_dir)
        print("\n-- Removing tmp file --")
        clean_tar_chunk(chunk_name, tmp_dir)

    print(f"\n-- Downloaded and Extracted SA-V {split} --")


# - CONSTANTS ---
PATH_TO_YAML = "download_SA_V.yaml"
TMP_DIR = "/home/sagemaker-user/user-default-efs/data/tmp"
DESTINATION_DIR = "/home/sagemaker-user/user-default-efs/data/SA-V/"


# - MAIN ---
def main():
    sav_link_collection = read_yaml(PATH_TO_YAML)

    # Extract the SA-V dataset
    splits = ["train", "val", "test", "check_sum"]
    for split in splits:
        download_and_extract_data_split(
            sav_link_collection,
            DESTINATION_DIR,
            TMP_DIR,
            split
        )


# - RUN ---
if __name__ == "__main__":
    main()
