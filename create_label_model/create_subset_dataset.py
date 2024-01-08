import random
import shutil
from pathlib import Path
import zipfile

def copy_random_images(base_directory, current_directory, num_images=500):
    # Path to the base directory containing images
    base_path = Path(base_directory)

    # Create a list to store all image paths
    all_images = []

    # Walk through the directory structure
    for path in base_path.rglob('*.png'):
        all_images.append(path)

    # Randomly select 500 images
    selected_images = random.sample(all_images, min(num_images, len(all_images)))

    # Destination directory
    dest_directory = Path(current_directory) / 'images'
    dest_directory.mkdir(parents=True, exist_ok=True)

    # Copy the selected images to the current directory
    for image in selected_images:
        shutil.copy(image, dest_directory)

    return dest_directory

def zip_directory(folder_path, zip_name):
    # Create a zip file for the folder
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for path in Path(folder_path).rglob('*'):
            zipf.write(path, path.relative_to(folder_path.parent))

def main():
    # base_directory = Path.cwd().parent
    base_directory = "d:\\lol_champion_model_images\\"
    current_directory = Path.cwd()
    images_directory = copy_random_images(base_directory, current_directory)

    # Zip the images directory
    zip_directory(images_directory, current_directory / 'images.zip')

if __name__ == "__main__":
    main()