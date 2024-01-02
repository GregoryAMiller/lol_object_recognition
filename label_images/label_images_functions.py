# Function used in labeling images using YOLOV8 

from pathlib import Path
from ultralyticsplus import YOLO
import cv2

# Function to load and configure the YOLO model
def load_configure_model():
    # Load model
    model = YOLO('ultralyticsplus/yolov8s')

    # Set model parameters
    model.overrides['conf'] = 0.25  # NMS confidence threshold
    model.overrides['iou'] = 0.45  # NMS IoU threshold
    model.overrides['agnostic_nms'] = False  # NMS class-agnostic
    model.overrides['max_det'] = 1  # Maximum number of detections per image
    print('returning model')
    return model

# Function to label the image
def label_image(model, image_path, labels_dir):
    # Extract the label name from the folder structure
    champion_name = image_path.parent.parent.name
    skin_name = image_path.parent.name
    print(f'champion_name: {champion_name}')
    print(f'skin_name: {skin_name}')
    # Read the image
    image = cv2.imread(str(image_path))
    
    # Perform inference
    results = model.predict(image)
    boxes = results[0].boxes
    
    if boxes:
        # Create a labels directory mirroring the images directory structure
        label_file_dir = labels_dir / champion_name / skin_name
        label_file_dir.mkdir(parents=True, exist_ok=True)
        # Only take the first box and move it to CPU and convert to numpy array if it's a tensor
        box = boxes[0]
        # print(box)
        # Only take the first box
        x_center, y_center, width, height = box.xyxy[0]
        
        # Format the label data
        label_data = f'{skin_name} {x_center} {y_center} {width} {height}'
        # print(label_data)
        
        # Write label data to a text file
        label_file_name = f"{image_path.stem}.txt"
        label_file_path = label_file_dir / label_file_name
        print(label_file_path)
        with open(label_file_path, 'w') as f:
            f.write(label_data)
        print(f"Label file created: {label_file_path}")
    else:
        print(f"No boxes found in {image_path}")