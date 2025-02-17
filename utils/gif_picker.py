import os
import random
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

def pick_random_file(directory: os.PathLike) -> os.PathLike:
    if not os.path.isdir(directory):
        raise ValueError(f"Invalid directory: {directory}")
    
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    if not files:
        raise FileNotFoundError("No files found in the specified directory.")
    
    return os.path.join(directory, random.choice(files))

if __name__ == "__main__":
    assets_path = "media/gif_assets"
    for effect in os.listdir(assets_path):
        effect_path = os.path.join(assets_path, effect)
        if os.path.isdir(effect_path) and effect_path not in [".", ".."]:
            logging.debug(effect_path)
            filename = pick_random_file(effect_path)
            logging.debug(filename)
