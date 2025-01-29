import wget
import os
import logging


WEIGHTS_URL = "https://huggingface.co/CompVis/stable-diffusion-v-1-4-original/resolve/main/sd-v1-4.ckpt"


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def download_weights_to_file(weights_url, filename):
    try:
        output_directory = os.path.dirname(os.path.abspath(filename))
        os.makedirs(output_directory, exist_ok=True)
        logging.info(f"Output directory: {output_directory}")

        logging.info(f"Downloading from {weights_url}...")
        downloaded_file_path = wget.download(weights_url, out=output_directory)
        logging.info(f"Downloaded file: {downloaded_file_path}")

        final_file_path = os.path.abspath(filename)
        os.rename(downloaded_file_path, final_file_path)
        logging.info(f"File saved to: {final_file_path}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise


if __name__ == "__main__":
    download_weights_to_file(
        WEIGHTS_URL,
        "/userHome/userhome1/timur/NurseVRGen/submodules/StyleID/models/ldm/stable-diffusion-v1/model.ckpt",
    )
