from pathlib import Path
import random
import shutil

def get_all_files(base_dir, ext):
    files = [file for file in base_dir.glob(f'*{ext}') if file.is_file()]
    print(f"Found {len(files)} '{ext}' files in {base_dir}")
    return files

def match_files(image_files, label_files, image_dir, label_dir):
    matched_files = []
    label_files_set = set(label_files)
    for image_file in image_files:
        label_file = label_dir / image_file.relative_to(image_dir).with_suffix('.txt')
        if label_file in label_files_set:
            matched_files.append((image_file, label_file))
    print(f"Matched {len(matched_files)} file pairs.")
    return matched_files

def create_dirs_and_copy_files(file_pairs, start_idx, end_idx, data_type, base_path):
    image_folder_path = base_path / data_type / 'images'
    label_folder_path = base_path / data_type / 'labels'
    
    image_folder_path.mkdir(parents=True, exist_ok=True)
    label_folder_path.mkdir(parents=True, exist_ok=True)
    
    for image_file, label_file in file_pairs[start_idx:end_idx]:
        shutil.copy(image_file, image_folder_path / image_file.name)
        shutil.copy(label_file, label_folder_path / label_file.name)
        print(f"Copied {image_file.name} and {label_file.name} to {data_type}.")

def main():
    train_ratio = 0.7
    val_ratio = 0.15
    test_ratio = 0.15

    base_path = Path.cwd() / 'data'
    images_dir = base_path / 'images'
    labels_dir = base_path / 'labels'

    image_files = get_all_files(images_dir, '.png')
    label_files = get_all_files(labels_dir, '.txt')

    matched_files = match_files(image_files, label_files, images_dir, labels_dir)
    random.shuffle(matched_files)

    total_pairs = len(matched_files)
    train_end = int(total_pairs * train_ratio)
    val_end = train_end + int(total_pairs * val_ratio)

    create_dirs_and_copy_files(matched_files, 0, train_end, 'train', base_path)
    create_dirs_and_copy_files(matched_files, train_end, val_end, 'val', base_path)
    create_dirs_and_copy_files(matched_files, val_end, total_pairs, 'test', base_path)

    print("Files have been successfully split and copied into train, test, and val directories.")

if __name__ == '__main__':
    main()
