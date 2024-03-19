from pathlib import Path

# Define the list of labels to delete
labels_to_delete = ['2', '3', '4', '5', '7', '8', '9', '10']  # Update this list as needed
# Define supported image file extensions
image_extensions = ['.jpg', '.png', '.jpeg']

def delete_files_with_labels(start_path):
    start_path = Path(start_path)
    # Keep track of deleted files for troubleshooting
    deleted_labels = []
    deleted_images = []
    
    # Recursively search for .txt files
    for label_file_path in start_path.rglob('*.txt'):
        delete_current_file = False
        with label_file_path.open('r') as file:
            for line in file:
                label_name = line.split()[0].strip()  # Assuming label_name is the first element
                if label_name in labels_to_delete:
                    delete_current_file = True
                    break  # No need to read further if we're going to delete the file

        if delete_current_file:
            print(f"Deleting label file: {label_file_path}")
            label_file_path.unlink()  # Delete the label file
            deleted_labels.append(label_file_path)

            # Delete the corresponding image file
            for ext in image_extensions:
                image_file_path = label_file_path.with_suffix(ext)
                if image_file_path.exists():
                    print(f"Deleting corresponding image file: {image_file_path}")
                    image_file_path.unlink()
                    deleted_images.append(image_file_path)
                    break  # Found and deleted the image, no need to continue
                
    return deleted_labels, deleted_images

# Example usage
base_directory = Path.cwd().parent
base_path = base_directory / 'final_train_test_val_dataset/version1.1'  # Update this to your actual base directory
deleted_labels, deleted_images = delete_files_with_labels(base_path)

print(f"Deleted {len(deleted_labels)} label files and {len(deleted_images)} image files.")
