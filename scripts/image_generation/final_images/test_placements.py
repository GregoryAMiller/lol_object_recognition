import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from pathlib import Path
import os

def display_image_with_bbox_and_save(image_path, label_path, save_path):
    # Load the image
    image = Image.open(image_path)
    image_width, image_height = image.size
    
    # Prepare the plot
    fig, ax = plt.subplots()
    ax.imshow(image)
    
    # Read the label file and extract bounding box coordinates
    with open(label_path, 'r') as file:
        for line in file:
            data = line.strip().split()
            if len(data) == 5:  # Correct format for YOLOv8 label
                class_id, x_center, y_center, bbox_width, bbox_height = map(float, data)
                
                # Convert normalized coordinates to absolute coordinates
                box_width = bbox_width * image_width
                box_height = bbox_height * image_height
                box_x = (x_center * image_width) - (box_width / 2)
                box_y = (y_center * image_height) - (box_height / 2)
                
                # Create and add a rectangle patch for the bounding box
                rect = patches.Rectangle((box_x, box_y), box_width, box_height, linewidth=1, edgecolor='r', facecolor='none')
                ax.add_patch(rect)
            else:
                print(f"Invalid line format in {label_path}: '{line.strip()}'")
    
    plt.axis('off')  # Remove axes for saving
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
    plt.close()  # Close the figure to free memory

def label_all_images(image_dir, label_dir, example_dir):
    # Ensure example directory exists
    example_dir_path = Path(example_dir)
    example_dir_path.mkdir(parents=True, exist_ok=True)
    
    for image_path in image_dir.glob('*.jpg'):  # Adjust glob pattern as needed
        label_file_name = image_path.with_suffix('.txt').name
        label_path = label_dir / label_file_name
        
        # Skip processing if label file doesn't exist
        if not label_path.exists():
            print(f"Label file for {image_path.name} not found. Skipping...")
            continue
        
        # Define save path
        save_path = example_dir_path / f"labeled_{image_path.name}"
        
        # Display image with bounding boxes and save
        display_image_with_bbox_and_save(image_path, label_path, save_path)
        print(f"Processed and saved {save_path}")

if __name__ == "__main__":
    
    base_dir = Path.cwd().parent.parent.parent

    version = 'version2.0'
    image_dir = base_dir / 'data/sythestic/final_data' / version / 'images'  # Adjust to your images directory
    label_dir = base_dir / 'data/sythestic/final_data' / version / 'labels'  # Adjust to your labels directory

    example_dir = Path.cwd() / 'samples'  # Folder where labeled images will be saved
    
    label_all_images(image_dir, label_dir, example_dir)
