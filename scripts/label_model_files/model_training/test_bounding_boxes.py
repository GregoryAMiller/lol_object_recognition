import cv2
import os
from pathlib import Path

def read_bounding_box(file_path):
    with open(file_path, 'r') as file:
        data = file.readline().strip().split()
    # Skip the first value (object ID) and return the remaining four values as coordinates
    return [float(i) for i in data[1:]]

def convert_to_absolute(coordinates, img_width, img_height):
    x_center, y_center, width, height = coordinates
    x1 = int((x_center - width / 2) * img_width)
    y1 = int((y_center - height / 2) * img_height)
    x2 = int((x_center + width / 2) * img_width)
    y2 = int((y_center + height / 2) * img_height)
    return x1, y1, x2, y2

def process_image(image_path, bbox_path, output_dir):
    # Read image and get dimensions
    image = cv2.imread(str(image_path))
    img_height, img_width = image.shape[:2]

    # Read bounding box info and convert to absolute coordinates
    bbox_coordinates = read_bounding_box(str(bbox_path))
    x1, y1, x2, y2 = convert_to_absolute(bbox_coordinates, img_width, img_height)

    # Draw bounding box on image
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Save the image with bounding box
    cv2.imwrite(str(output_dir / image_path.name), image)

def main():
    base_path = Path.cwd()
    images_base_directory = base_path / 'data/images'
    labels_base_directory = base_path / 'data/labels'
    output_directory = base_path / 'test_boxes'
    
    # Create output directory if it doesn't exist
    output_directory.mkdir(exist_ok=True)

    # Iterate through all images in the images directory
    for image_path in images_base_directory.iterdir():
        if image_path.is_file() and image_path.suffix in ['.jpg', '.png', '.jpeg']:
            # Assume label file has same name but different directory and extension
            label_path = labels_base_directory / (image_path.stem + '.txt')
            if label_path.exists():
                process_image(image_path, label_path, output_directory)
            else:
                print(f"No corresponding label found for {image_path.name}")

if __name__ == '__main__':
    main()