# this fixes the label files (replaces SkinName in the label file with a number)
from pathlib import Path

def update_label_files(image_path):
    image_path = Path(image_path)

    if not image_path.is_dir():
        print("The provided path is not a directory.")
        return

    # Process the .txt files directly in the images directory
    for file_path in sorted(image_path.glob('*.txt')):
        print(f'Updating file: {file_path.name}')
        
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Replace 'Champion' with '0'
        updated_content = content.replace('Champion', '0')

        with open(file_path, 'w') as file:
            file.write(updated_content)

def main():
    base_directory = Path.cwd().parent
    images_dir = base_directory / 'labels'
    update_label_files(images_dir)

if __name__ == '__main__':
    main()