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

def label_image(model, image_path, testing_dir, conf=.4, testing=True):
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

        # Save annotated image only if testing is True
        if testing:
            cv2.rectangle(image, (start_x, start_y), (end_x, end_y), (255, 0, 0), 2)
            result_file_path = testing_dir / f"{image_path.stem}_annotated.png"
            result_file_path.parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(result_file_path), image)
            print(f"Annotated image saved: {result_file_path}")
    else:
        print(f"No boxes found in {image_path}")

def main():
    
    base_dir = Path.cwd().parent.parent

    conf = .4
    data_version = '1.0'
    model_version = '1.3'

    testing_dir = Path.cwd() / 'results'
    model_dir = base_dir / 'models/data_labeling_model' / f'version{model_version[0]}' / f'version{model_version}' / 'runs/detect/train/weights/best.pt'
    # images_dir = base_dir / 'data/synthetic' / f'version{data_version[0]}' / f'version{data_version}' / 'images'

    images_dir = Path.cwd() / 'data/test' / 'images'



    # Load and configure the model
    model = load_configure_model(model_dir)

    # Walk through the images directory structure
    for image_path in images_dir.rglob('*.jpg'):  # Using rglob to find .png files recursively
        label_image(model, image_path, testing_dir, conf, testing=True)

if __name__ == "__main__":
    main()