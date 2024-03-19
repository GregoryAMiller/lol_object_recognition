from ultralytics import YOLO
import glob
from pathlib import Path
from IPython.display import Image
# from ultralyticsplus import render_result
# Load the trained model
model_version = '1.3'
conf = .4
model_path = Path.cwd().parent.parent / 'models/champion_detection_model' / f'version{model_version[0]}' / f'version{model_version}' / 'runs/detect/train/weights/best.pt'
model = YOLO(model_path)  # Path to the trained weights

# Specify the source directory containing images for detection
# source_dir = Path(f'{Path.cwd().parent}/final_train_test_val_dataset/version1.1/test/images')  # Update with your source path
source_dir = Path(f'{Path.cwd().parent.parent}/Ahri_Academia___Previsualizaci_n___League_of_Legends_frames')  # Update with your source path
# print(source_dir)
# # Results directory in the parent of script directory
# results_dir = Path.cwd().parent / 'results'

# # Create the results directory if it doesn't exist
# results_dir.mkdir(parents=True, exist_ok=True)

# Iterate over each image in the source directory
for image_path in source_dir.glob('*.jpg'):  # Adjust for different image formats as necessary
    # Perform prediction and save the output image
    model.predict(str(image_path), save=True, conf=conf) # , imgsz=320

    # print(f"Processed and saved results for {image_path.name} in {results_dir}")

