import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from pathlib import Path

def display_image_with_bbox(image_path, label_path):
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
    
    plt.show() 

if __name__ == "__main__":

    base_dir = Path.cwd().parent.parent.parent

    version = 'version2.0'
    image_path = base_dir / 'data/sythestic/final_data' / version / 'images' / 'image_17_combined_42.jpg'  # Adjust to your image path
    label_path = base_dir / 'data/sythestic/final_data' / version / 'labels' / 'image_17_combined_42.txt'  # Adjust to your label file path

    display_image_with_bbox(image_path, label_path)