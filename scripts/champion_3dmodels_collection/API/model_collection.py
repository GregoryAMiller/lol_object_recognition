import model_collection_functions
from pathlib import Path

def main():
    cloudfront_url = 'https://d39h8efa1lafbi.cloudfront.net/export'
    current_dir = Path.cwd()
    yaml_file_path = current_dir / 'champion_3dmodels_collection' / 'champion_skin_mapping.yaml'
    last_run_file_path = current_dir / 'champion_3dmodels_collection' / 'yaml_file_last_updated.txt'
    save_directory = current_dir / 'API' / 'data/3d_glb_files'

    model_collection_functions.update_yaml_file_if_needed(yaml_file_path, last_run_file_path)

    champions_data = model_collection_functions.load_yaml_file(yaml_file_path)

    champions_list = []  # Add champion names as needed, or leave empty to download all models.
    model_limit = None  # Set to None to download all models

    model_collection_functions.get_many_models(cloudfront_url, champions_data, save_directory, champions_list, model_limit)

if __name__ == "__main__":
    main()