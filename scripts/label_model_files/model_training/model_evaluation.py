from ultralytics import YOLO
import glob
from pathlib import Path
from IPython.display import Image
import shutil

# from ultralyticsplus import render_result
# Load the trained model
version = '1.0'
model_dir = Path.cwd().parent.parent.parent / f'models/data_labeling_model/version{version[0]}/version{version}/runs/detect/train/weights/best.pt'

model = YOLO(model_dir)  # Path to the trained weights

# Directories
source_dir = Path(f'{Path.cwd()}/data/test/images')  # Source directory for detection

test_dir = Path(f'{Path.cwd()}/data/test/images')  # Source directory for detection
train_dir = Path(f'{Path.cwd()}/data/train/images')  # Training images directory
val_dir = Path(f'{Path.cwd()}/data/val/images')  # Validation images directory

# Count the number of images in each directory
source_images = len(list(source_dir.glob('*.png')))

num_test_images = len(list(test_dir.glob('*.png')))
num_train_images = len(list(train_dir.glob('*.png')))
num_val_images = len(list(val_dir.glob('*.png')))
total_images = num_test_images + num_train_images + num_val_images

# Initialize prediction count
predictions_made = 0

# Iterate over each image in the source directory for detection
for image_path in source_dir.glob('*.png'):
    # Perform prediction
    results = model.predict(str(image_path), save=True, conf=0.4)  # conf and imgsz are optional parameters
    
    # Assuming results is a list where each element corresponds to detections for an image
    # and each detection is a dictionary or an object from which you can determine if there were any detections.
    # You would need to adapt this loop based on the actual structure of your results.
    for detection in results:
        if len(detection) > 0:  # Assuming detection is a list of detected objects
            predictions_made += 1
            break  # Assuming you only count once per image regardless of the number of detections

# Calculate the score
score = predictions_made / num_test_images if num_test_images > 0 else 0

# Prepare the information to be written to the file
info = f'''Number of source images: {source_images}\nScore (Predictions/Total Test Images): {predictions_made} / {source_images} = {score}\n'''

# Write the information to a text file
info_file_path = Path.cwd().parent.parent.parent / f'models/data_labeling_model/version{version[0]}/version{version}/runs/detect/train/count_info.txt'
with open(info_file_path, 'a') as f:
    f.write(info)

print(f"Info saved to {info_file_path}")

save_file_dir = Path.cwd().parent.parent.parent / f'models/data_labeling_model/version{version[0]}/version{version}'

# Define the base directory
base_directory = Path.cwd()
# Now we define source_directory here, before it's used
source_directory = base_directory / 'runs'

# Assuming the rest of your script is correct and above this block
val_directory = source_directory / 'detect' / 'predict'
# Create the target directory if it does not exist
save_file_dir.mkdir(parents=True, exist_ok=True)
new_val_directory = save_file_dir / 'runs' / 'detect'


# Check if the source 'val' directory exists
if val_directory.exists():
    # Ensure the target directory for 'val' does not have an old version
    if new_val_directory.exists():
        shutil.rmtree(new_val_directory)  # Remove the existing 'val' directory to avoid merge conflicts
    # Create parent directories for the new location of 'val' if they don't exist
    new_val_directory.parent.mkdir(parents=True, exist_ok=True)
    # Move the 'val' directory to the new location
    shutil.move(str(val_directory), str(new_val_directory))
    print(f"Moved {val_directory} to {new_val_directory}")
else:
    print(f"The directory {val_directory} does not exist.")

