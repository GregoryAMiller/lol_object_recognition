# Function used in labeling images using YOLOV8 

from pathlib import Path
# from ultralyticsplus import YOLO
from ultralytics import YOLO
import cv2

# Function to load and configure the YOLO model
def load_configure_model(model_dir):
    # Load model 
    model = YOLO(model_dir)
    # Set model parameters
    # model.overrides['conf'] = 0.25  # NMS confidence threshold
    # model.overrides['iou'] = 0.45  # NMS IoU threshold
    # model.overrides['agnostic_nms'] = False  # NMS class-agnostic
    # model.overrides['max_det'] = 1  # Maximum number of detections per image
    print('returning model')
    return model

def label_image(model, image_path, labels_dir, testing_dir, skin_name_mapping, conf=.4, testing=False):
    # Extract the label name from the folder structure
    champion_name = image_path.parent.parent.name
    skin_name = image_path.parent.name
    full_skin_name = f'{champion_name}/{skin_name}'
    label_number = skin_name_mapping.get(full_skin_name, -1)  # Use -1 if skin not found in mapping
    print(f'champion_name: {champion_name}')
    print(f'skin_name: {skin_name}, label_number: {label_number}')

    # Read the image
    image = cv2.imread(str(image_path))
    image_height, image_width = image.shape[:2]

    # Perform inference
    results = model.predict(image, save=True, conf=conf)
    boxes = results[0].boxes

    if boxes:
        # Process the first box
        box = boxes[0]
        x_center, y_center, width, height = box.xywhn[0]

        # Transform normalized coordinates to pixel values
        x_center *= image_width
        y_center *= image_height
        width *= image_width
        height *= image_height

        # Calculate start and end points
        start_x = int(x_center - width / 2)
        start_y = int(y_center - height / 2)
        end_x = int(x_center + width / 2)
        end_y = int(y_center + height / 2)

        # Save label data with the number instead of skin_name
        label_data = f'{label_number} {x_center/image_width} {y_center/image_height} {width/image_width} {height/image_height}'
        label_file_dir = labels_dir / champion_name / skin_name
        label_file_dir.mkdir(parents=True, exist_ok=True)
        label_file_name = f"{image_path.stem}.txt"
        label_file_path = label_file_dir / label_file_name
        with open(label_file_path, 'w') as f:
            f.write(label_data)
        print(f"Label file created: {label_file_path}")

        # Save annotated image only if testing is True
        if testing:
            cv2.rectangle(image, (start_x, start_y), (end_x, end_y), (255, 0, 0), 2)
            result_file_path = testing_dir / champion_name / f"{image_path.stem}_annotated.png"
            result_file_path.parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(result_file_path), image)
            print(f"Annotated image saved: {result_file_path}")
    else:
        print(f"No boxes found in {image_path}")


def load_skin_name_mapping(mapping_file_path):
    mapping = {}
    with open(mapping_file_path, 'r') as f:
        for line in f:
            parts = line.strip().split(' - ')
            mapping[parts[0]] = int(parts[1])
    return mapping

def generate_and_save_skin_name_mapping(images_dir, mapping_file_path):
    mapping = {}
    counter = 0  # Initialize a counter to assign unique numbers to each skin
    for champion_dir in sorted(images_dir.iterdir(), key=lambda x: x.name):
        for skin_dir in sorted(champion_dir.iterdir(), key=lambda x: x.name):
            if skin_dir.is_dir():
                mapping[f"{champion_dir.name}/{skin_dir.name}"] = counter
                counter += 1  # Increment the counter for each skin
    with open(mapping_file_path, 'w') as file:
        for full_skin_name, number in mapping.items():
            file.write(f"{full_skin_name} - {number}\n")
    return mapping