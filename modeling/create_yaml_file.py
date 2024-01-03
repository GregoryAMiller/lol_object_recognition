# creates the yaml file needed for yolov8 fine-tuning
# yaml file format
'''
train: /content/drive/My Drive/train
val: /content/drive/My Drive/valid
test: /content/drive/My Drive/test

nc: 12
names: ['Annie', 'Fizz', 'aBase', 'aInhib', 'aKripp', 'aTower', 'amumu', 'eBase', 'eInhib', 'eKripp', 'eTower', 'Akshan']
'''

import yaml
from pathlib import Path

def create_yaml_from_listing(listing_path, yaml_filename, base_directory):
    # Read the listing.txt file
    with open(listing_path, 'r') as file:
        lines = file.readlines()
    
    # Parse the listing content to extract names and remove the part after the dash
    names = [line.split(' - ')[0].strip() for line in lines if line.strip() != '']

    # Manually format the names list as a string to resemble a JSON array
    names_str = '[' + ', '.join(f"'{name}'" for name in names) + ']'

    # Prepare the data dictionary for YAML without the names key
    data = {
        'train': str(base_directory / 'train'),
        'val': str(base_directory / 'val'),
        'test': str(base_directory / 'test'),
        'nc': len(names)
    }

    # Write the data to a yaml file
    with open(yaml_filename, 'w') as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False)
        # Manually write the names list as a formatted string
        yaml_file.write(f"names: {names_str}\n")

def main():
    base_directory = Path.cwd().parent
    # Define the paths
    listing_path = base_directory / 'listing.txt'
    yaml_filename = base_directory / 'dataset.yaml'
    # Call the function to create the YAML file
    create_yaml_from_listing(listing_path, yaml_filename, base_directory)

if __name__ == '__main__':
    main()