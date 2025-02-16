import os
import PIL
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def delete_files_in_directory(directory_path):
    if os.path.exists(directory_path):
        for file in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    else:
        logging.info("Path doesn't exist")


def get_list_of_files(directory_path):
    files = []
    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path):
            files.append(file_path)
    return files


def cleanup(directories_to_cleanup: list[os.PathLike]):
    for directory in directories_to_cleanup:
        delete_files_in_directory(directory)


def copy_image_to_subdirectory(image_asset: PIL.Image, subdirectory):
    filename = os.path.join(subdirectory, "00.jpg")
    if not os.path.exists(subdirectory):
        logging.info("Path doesn't exist. Creating...")
        os.makedirs(subdirectory)
    logging.debug(filename)
    image_asset.save(filename)
    return filename
