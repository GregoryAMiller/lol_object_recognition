from pathlib import Path
from PIL import Image

def convert_png_to_jpeg(directory):
    # jpeg_files = []
    # Navigate through each subdirectory within the given directory
    for subdirectory in directory.iterdir():
        if subdirectory.is_dir():
            # Navigate through each sub-subdirectory (skin folder)
            for skin_folder in subdirectory.iterdir():
                if skin_folder.is_dir():
                    # Convert each PNG image within the skin folder
                    for png_file in skin_folder.glob('*.png'):
                        jpeg_file_path = png_file.with_suffix('.jpeg')
                        with Image.open(png_file) as image:
                            image = image.convert('RGB')
                            image.save(jpeg_file_path, 'JPEG')
                            # jpeg_files.append(jpeg_file_path)
                            # remove the original PNG file
                            png_file.unlink()
    # return jpeg_files

def main():
    # Define the base directory as the current working directory
    base_directory = Path.cwd().parent
    # Define the images directory path
    images_dir = base_directory / 'images'

    # Convert the PNG files to JPEG
    convert_png_to_jpeg(images_dir)
    # jpeg_files = convert_png_to_jpeg(images_dir)
    
    # Print the list of converted JPEG files
    # for jpeg_file in jpeg_files:
    #     print(f"Converted {jpeg_file}")

if __name__ == '__main__':
    main()