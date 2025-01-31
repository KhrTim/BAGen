import os
import subprocess
import PIL
from .common import copy_image_to_subdirectory, get_list_of_files
from .download_weights import download_weights_to_file

STYLEID_DIR = os.path.join("submodules", "StyleID")


def perform_styleid_styletransfer(
    content_image: PIL.Image.Image, style_image: PIL.Image.Image
) -> os.PathLike:
    WEIGHTS_URL = "https://huggingface.co/CompVis/stable-diffusion-v-1-4-original/resolve/main/sd-v1-4.ckpt"
    weights_filename = os.path.join(
        STYLEID_DIR, "models", "ldm", "stable-diffusion-v1", "model.ckpt"
    )
    if not os.path.exists(weights_filename):
        print("weights haven't been found.")
        print(f"Loading weights to {weights_filename} ...")
        download_weights_to_file(WEIGHTS_URL, weights_filename)

    style_id_content_dir = os.path.join(STYLEID_DIR, "data", "cnt")
    style_id_style_dir = os.path.join(STYLEID_DIR, "data", "sty")

    os.makedirs(style_id_content_dir, exist_ok=True)
    os.makedirs(style_id_style_dir, exist_ok=True)

    copy_image_to_subdirectory(content_image, style_id_content_dir)
    copy_image_to_subdirectory(style_image, style_id_style_dir)

    subprocess.call(["python", "run_styleid.py"], cwd="./submodules/StyleID/")

    visualization_dir = os.path.join(STYLEID_DIR, "output")
    style_transfer_image_filename = get_list_of_files(visualization_dir)[0]

    return style_transfer_image_filename
