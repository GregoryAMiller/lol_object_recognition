import re
from pathlib import Path

def replace_label_number_in_files(start_directory, old_number, new_number):
    # Compile a regular expression to match lines with the specified format
    # where the label starts with old_number
    pattern = re.compile(rf'^{old_number}\s')
    
    # Convert start_directory to a Path object for easier path manipulations
    start_directory = Path(start_directory)

    # Walk through the directory, including all subdirectories
    for filepath in start_directory.rglob('*.txt'):
        # Read the content of each .txt file
        with open(filepath, 'r') as file:
            lines = file.readlines()

        # Replace old_number with new_number in lines that match the pattern
        with open(filepath, 'w') as file:
            for line in lines:
                new_line = pattern.sub(f'{new_number} ', line)
                file.write(new_line)

def main():
    # Example usage
    base_directory = Path.cwd().parent
    version = 'version1.1'
    start_directory = base_directory / 'final_train_test_val_dataset' / version  # Change this to your directory path
    old_number = '6'  # old number
    new_number = '2'  # new number
    
    replace_label_number_in_files(start_directory, old_number, new_number)
    print(f"Finished replacing labels in files under {start_directory}")

if __name__ == "__main__":
    main()
