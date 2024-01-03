# splits the images and corresponding label files into test, train, val folders (only places files with a labels file and image files)
from pathlib import Path
import random
import shutil

def get_all_files(base_dir):
    return [file for file in base_dir.rglob('*') if file.is_file()]

def match_files(image_files, label_files, image_dir, label_dir):
    matched_files = []
    label_files_set = set(label_files)
    for image_file in image_files:
        label_file = label_dir / image_file.relative_to(image_dir).with_suffix('.txt')
        if label_file in label_files_set:
            matched_files.append((image_file, label_file))
    return matched_files

def create_dirs_and_copy(file_pairs, start_idx, end_idx, data_type, base_path, image_dir, label_dir):
    for image_file, label_file in file_pairs[start_idx:end_idx]:
        image_folder_path = base_path / data_type / 'images'
        label_folder_path = base_path / data_type / 'labels'
        
        image_folder_path.mkdir(parents=True, exist_ok=True)
        label_folder_path.mkdir(parents=True, exist_ok=True)
        
        shutil.copy(image_file, image_folder_path / image_file.name)
        shutil.copy(label_file, label_folder_path / label_file.name)

def main():
    # Define the split ratios
    train_ratio = 0.7
    val_ratio = 0.15
    test_ratio = 0.15

    # Base path where train, test, and val directories will be created
    base_path = Path.cwd().parent

    # Paths to the image and label folders
    image_dir = base_path / 'images'
    label_dir = base_path / 'labels'

    # Get all file paths from both directories
    image_files = get_all_files(image_dir)
    label_files = get_all_files(label_dir)

    # Shuffle the file list
    matched_files = match_files(image_files, label_files, image_dir, label_dir)
    random.shuffle(matched_files)

    # Calculate split indices
    total_pairs = len(matched_files)
    train_end = int(total_pairs * train_ratio)
    val_end = train_end + int(total_pairs * val_ratio)

    # Split and copy files
    create_dirs_and_copy(matched_files, 0, train_end, 'train', base_path, image_dir, label_dir)
    create_dirs_and_copy(matched_files, train_end, val_end, 'val', base_path, image_dir, label_dir)
    create_dirs_and_copy(matched_files, val_end, total_pairs, 'test', base_path, image_dir, label_dir)

    print("Files have been successfully split and copied into train, test, and val directories.")

if __name__ == '__main__':
    main()