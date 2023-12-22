import requests
import yaml
from pathlib import Path
import re
import yaml_functions

def sanitize_filename(filename):
    """
    Sanitize the file name by replacing invalid characters with underscores.

    Args:
    filename (str): The original file name.

    Returns:
    str: The sanitized file name.
    """
    return re.sub(r'[\\/*?:"<>|]', '_', filename)

def load_yaml_file(file_path):
    """
    Load data from a YAML file.

    Args:
    file_path (str): The path to the YAML file.

    Returns:
    dict: Loaded data from the YAML file.
    """
    with open(file_path, 'r') as yaml_file:
        return yaml.safe_load(yaml_file)

def get_download_url(cloudfront_url, champion_skin_id):
    """
    Construct the download URL for a champion's skin model.

    Args:
    cloudfront_url (str): The base URL for downloading models.
    champion_skin_id (int): The combined ID of the champion and the skin.

    Returns:
    str: The complete URL to download the model.
    """
    champion_id = str(champion_skin_id)[:-3]
    skin_id = str(champion_skin_id)[-3:].lstrip('0') or '0'
    return f"{cloudfront_url}/{champion_id}/skin{skin_id}.glb.gz"  


def download_model(url, file_path):
    """
    Download a model from the given URL and save it to the specified path.

    Args:
    url (str): URL to download the model.
    file_path (Path): The path where the model will be saved.

    Returns:
    bool: True if download succeeds, False otherwise.
    """
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        return True
    else:
        print(f"Failed to download: {url}")
        return False

def get_many_models(cloudfront_url, champions_data, save_directory, champions_list=None, limit=None):
    """
    Download models for each champion's skin, up to a specified limit.
    If champions_list is provided, only download models for those champions.
    If no limit is specified, download all models.

    Args:
    cloudfront_url (str): The base URL for downloading models.
    champions_data (list): List of champions and their skin data.
    save_directory (Path): The base directory to save the models.
    champions_list (list, optional): List of champions to download models for. Default is None, which means all champions.
    limit (int, optional): Maximum number of models to download. Default is None, which means no limit.
    """
    download_count = 0
    for champion in champions_data:
        if champions_list is not None and champion['name'] not in champions_list:
            continue  # Skip champions not in the list
        champion_name = champion['name']
        print(f"Processing champion: {champion_name}")
        for skin in champion.get('skins_data', []):
            skin_name = sanitize_filename(skin['name'])
            print(f"Loading skin: {skin_name} for champion: {champion_name}")
            if limit is not None and download_count >= limit:
                print(f"Reached download limit of {limit}.")
                break  # Stop if the limit is reached
            skin_id = skin['id']
            model_url = get_download_url(cloudfront_url, skin_id)
            skin_folder = Path(save_directory) / champion_name / skin_name
            skin_folder.mkdir(parents=True, exist_ok=True)
            file_path = skin_folder / f"{skin_name}.glb"
            if download_model(model_url, file_path):
                download_count += 1  # Increment counter after successful download
                print(f"Downloaded {skin_name}.glb for champion: {champion_name}")
            else:
                print(f"Failed to download {skin_name}.glb for champion: {champion_name}")
            if limit is not None and download_count >= limit:
                print(f"Reached download limit of {limit}. Exiting.")
                return  # Exit the function if the limit is reached

def update_yaml_file_if_needed(yaml_file_path):
    """
    Check if the YAML file needs to be updated and update it if necessary.
    """
    current_champions_data = yaml_functions.get_champions_data()
    existing_data = load_yaml_file(yaml_file_path)

    if current_champions_data != existing_data:
        champions_data_with_skins = yaml_functions.add_skin_data(current_champions_data)
        yaml_functions.save_champion_skin_mapping(champions_data_with_skins, yaml_file_path)
        print("YAML file updated with the latest champions data.")
    else:
        print("No updates required for the YAML file.")