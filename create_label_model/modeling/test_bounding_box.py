import cv2
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

def process_image(image_path, bbox_path):
    # Convert Path objects to string
    image_path_str = str(image_path)
    bbox_path_str = str(bbox_path)

    # Read image and get dimensions
    image = cv2.imread(image_path_str)
    img_height, img_width = image.shape[:2]

    # Read bounding box info and convert to absolute coordinates
    bbox_coordinates = read_bounding_box(bbox_path_str)
    x1, y1, x2, y2 = convert_to_absolute(bbox_coordinates, img_width, img_height)

    # Draw bounding box on image (optional)
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Display image (optional)
    cv2.imshow('Image with Bounding Box', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
base_directory = Path.cwd().parent
# images_dir = base_directory / 'labels'
image_path = base_directory / 'images' / 'Akali_Base_Attack1_to_Run.anm_Akali_Base_Attack1_to_Run.anm_Armature_frame33_camera1.png'
bbox_path = base_directory / 'labels' / 'Akali_Base_Attack1_to_Run.anm_Akali_Base_Attack1_to_Run.anm_Armature_frame33_camera1.txt'
process_image(image_path, bbox_path)