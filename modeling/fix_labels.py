# this fixes the label files (replaces SkinName in the label file with a number)
from pathlib import Path

def create_and_update_label_files(base_path):
    # Convert string path to Path object
    base_path = Path(base_path)

    # Check if the path is a directory
    if not base_path.is_dir():
        print("The provided path is not a directory.")
        return

    # Walk through the directory, looking for subdirectories two levels deep
    for sub_dir in base_path.glob('*/'):  # First level of subdirectories
        listing_content = []
        counter = 0  # Initialize a counter for the subdirectories
        # Now we look for the next level of subdirectories
        for label_dir in sub_dir.glob('*/'):  # Second level of subdirectories
            print(f'Processing directory: {label_dir.name}')
            listing_content.append(f"{label_dir.name} - {counter}")
            counter += 1  # Increment the counter for each subdirectory
            
            # Now update the .txt files within this second-level subdirectory
            for file_path in sorted(label_dir.glob('*.txt')):  # Only work with .txt files
                print(f'Updating file: {file_path.name}')
                # Read the content of the txt file
                with open(file_path, 'r') as file:
                    content = file.read()
                
                # Replace the folder name in the file's content with the counter
                updated_content = content.replace(label_dir.name, str(counter - 1))  # counter is already incremented
                
                # Write the updated content back to the file
                with open(file_path, 'w') as file:
                    file.write(updated_content)

        # Create listing.txt in the base directory of the current sub_dir
        listing_path = Path.cwd().parent / 'listing.txt'
        with open(listing_path, 'w') as listing_file:
            listing_file.write('\n'.join(listing_content))
        print(f'Created listing file at: {listing_path}')


def main():
    base_directory = Path.cwd().parent
    labels_dir = base_directory / 'labels'
    create_and_update_label_files(labels_dir)

if __name__ == '__main__':
    main()