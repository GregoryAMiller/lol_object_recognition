from ultralytics import YOLO
import glob
from pathlib import Path
from IPython.display import Image
# from ultralyticsplus import render_result
# Load the trained model
model = YOLO(f'{Path.cwd()}/runs/detect/train/weights/best.pt')  # Path to the trained weights

# Specify the source directory containing images for detection
source_dir = Path(f'{Path.cwd().parent}/test/images')  # Update with your source path

# # Results directory in the parent of script directory
# results_dir = Path.cwd().parent / 'results'

# # Create the results directory if it doesn't exist
# results_dir.mkdir(parents=True, exist_ok=True)

# Iterate over each image in the source directory
for image_path in source_dir.glob('*.png'):  # Adjust for different image formats as necessary
    # Perform prediction and save the output image
    model.predict(str(image_path), save=True, conf=0.4) # , imgsz=320

    # print(f"Processed and saved results for {image_path.name} in {results_dir}")
