import label_images_functions
from pathlib import Path

# Main function to process directories
def main():

    base_directory = Path.cwd().parent
    images_dir = base_directory / 'images'
    labels_dir = base_directory / 'labels'
    results_dir = Path.cwd() / 'results'

    # Load and configure the model
    model = label_images_functions.load_configure_model()

    # Walk through the images directory structure
    for image_path in images_dir.rglob('*.jpg'):  # Using rglob to find .png files recursively
        label_images_functions.label_image(model, image_path, labels_dir, results_dir)


if __name__ == "__main__":
    main()