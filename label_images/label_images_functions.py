# Function used in labeling images using YOLOV8 

from pathlib import Path
# from ultralyticsplus import YOLO
from ultralytics import YOLO
import cv2

# Function to load and configure the YOLO model
def load_configure_model():
    # Load model C:\Users\Grego\Documents\1_projects\lol_object_recognition\create_label_model\modeling\runs\detect\train3\weights\best.pt
    # model = YOLO(f'{Path.cwd().parent}/create_label_model/modeling/runs/detect/train3/weights/best.pt')
    model = YOLO(f'{Path.cwd()}/best.pt')
    # print(f'{Path.cwd().parent}/create_label_model/modeling/runs/detect/train3/weights/best.pt')
    # print(model)
    # Set model parameters
    # model.overrides['conf'] = 0.25  # NMS confidence threshold
    # model.overrides['iou'] = 0.45  # NMS IoU threshold
    # model.overrides['agnostic_nms'] = False  # NMS class-agnostic
    # model.overrides['max_det'] = 1  # Maximum number of detections per image
    print('returning model')
    return model

def label_image(model, image_path, labels_dir, results_dir, testing=True):
    # Extract the label name from the folder structure
    champion_name = image_path.parent.parent.name
    skin_name = image_path.parent.name
    print(f'champion_name: {champion_name}')
    print(f'skin_name: {skin_name}')

    # Read the image
    image = cv2.imread(str(image_path))
    image_height, image_width = image.shape[:2]

    # Perform inference
    results = model.predict(image, save=True, conf=.25)
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

        # Save label data
        label_data = f'{skin_name} {x_center/image_width} {y_center/image_height} {width/image_width} {height/image_height}'
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
            result_file_path = results_dir / champion_name / skin_name / f"{image_path.stem}_annotated.jpg"
            result_file_path.parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(result_file_path), image)
            print(f"Annotated image saved: {result_file_path}")
    else:
        print(f"No boxes found in {image_path}")