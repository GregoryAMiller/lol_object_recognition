import random
import shutil
from pathlib import Path
import zipfile

def copy_images_to_directory(base_dir, current_dir, num_images=50):
    version = '1.0'
    images_path = base_dir / 'data/stage1' / f'version{version}' / 'images'

    # Dictionary to hold images paths categorized by skin directories
    skin_images = {}

    # Walk through the directory structure and categorize images
    for path in images_path.rglob('*.png'):
        skin_dir = path.parent.relative_to(images_path)
        if skin_dir not in skin_images:
            skin_images[skin_dir] = []
        skin_images[skin_dir].append(path)

    # Calculate the number of images to select from each skin directory
    num_skins = len(skin_images)
    images_per_skin = max(1, min(num_images // num_skins, num_images))

    selected_images = []
    for skin, images in skin_images.items():
        selected_images.extend(random.sample(images, min(images_per_skin, len(images))))

        # Adjust the total number of images if there aren't enough in current skin
        if len(selected_images) >= num_images:
            break

    # Destination directory for copying files
    images_directory = current_dir / 'model_training/data/images'
    images_directory.mkdir(parents=True, exist_ok=True)

    # Copy files to the destination directory with the same names as the original files
    for image_path in selected_images:
        destination_path = images_directory / image_path.name  # Use the original file name
        shutil.copy(image_path, destination_path)

    return images_directory

def zip_directory(folder_path, zip_name):
    # Create a zip file for the folder
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for path in Path(folder_path).rglob('*'):
            zipf.write(path, path.relative_to(folder_path.parent))

def main():
    base_dir = Path.cwd().parent.parent
    current_dir = Path.cwd()
    images_directory = copy_images_to_directory(base_dir, current_dir, num_images=50)

    # Zip the images directory
    # zip_directory(images_directory, current_dir / 'images.zip')

if __name__ == "__main__":
    main()