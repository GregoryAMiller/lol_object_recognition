import label_images_functions
from pathlib import Path

def main():
    conf = .2
    base_dir = Path.cwd().parent.parent

    data_version = '1.0'
    images_dir = base_dir / 'data/stage1' / f'version{data_version[0]}' / f'version{data_version}' / 'images'
    labels_dir = base_dir / 'data/stage1' / f'version{data_version[0]}' / f'version{data_version}' / 'labels'
    testing_dir = Path.cwd() / 'results'

    model_version = '1.1'
    model_dir = base_dir / 'models/data_labeling_model' / f'version{model_version[0]}' / f'version{model_version}' / 'runs/detect/train/weights/best.pt'

    # glb_dir = base_dir / 'data/3d_glb_files'

    # Load the skin name mapping
    mapping_file_path = base_dir / 'scripts/blank_image_labeling/skin_name_mapping.txt'  # Replace with actual path
    # Check if the mapping file exists, if not, generate it
    if not mapping_file_path.exists():
        print("Mapping file not found, generating new mapping...")
        skin_name_mapping = label_images_functions.generate_and_save_skin_name_mapping(images_dir, mapping_file_path)
    else:
        skin_name_mapping = label_images_functions.load_skin_name_mapping(mapping_file_path)

    # Load and configure the model
    model = label_images_functions.load_configure_model(model_dir)

    # Walk through the images directory structure
    for image_path in images_dir.rglob('*.png'):  # Using rglob to find .png files recursively
        label_images_functions.label_image(model, image_path, labels_dir, testing_dir, skin_name_mapping, conf, testing=True)

if __name__ == "__main__":
    main()