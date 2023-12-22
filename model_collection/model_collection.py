import model_collection_functions
from pathlib import Path

# Main execution
def main():
    """
    Main function to orchestrate the model downloading process.
    """
    cloudfront_url = 'https://d39h8efa1lafbi.cloudfront.net/export'  # Replace with actual Cloudfront URL if different
    yaml_file_path = Path('champion_skin_mapping.yaml')  # Path to the YAML file using pathlib
    # Get the current working directory (where the Jupyter Notebook is located)
    current_directory = Path.cwd()

    # Assuming the 'models' directory is outside the current notebook directory,
    # navigate to the 'models' directory accordingly.
    # Adjust the path as necessary based on your directory structure.
    save_directory = current_directory.parent / 'models'

    model_collection_functions.update_yaml_file_if_needed(yaml_file_path)

    champions_data = model_collection_functions.load_yaml_file(yaml_file_path)

    # Specify the champions you want to download models for
    champions_list = ['Akshan']  # Add champion names like 'Ahri', 'Aatrox', etc. Leave empty to download all models.
    model_limit = 1 # Set the maximum number of models to download (None for all models)

    # Pass the champions_list to the get_many_models function
    model_collection_functions.get_many_models(cloudfront_url, champions_data, save_directory, champions_list, model_limit)

if __name__ == "__main__":
    main()