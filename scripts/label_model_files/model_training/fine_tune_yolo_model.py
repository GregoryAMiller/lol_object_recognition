from ultralytics import YOLO
from pathlib import Path
import torch
import time
import shutil
import pandas as pd
import json

# change where the model is saved 
version = '1.4'

# Check for GPU and use it if available for faster training
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Using {device} device for training.')

# Define the target directory for the model
# model = 'yolov9c'
model = 'yolov8s'
model_directory = Path.cwd().parent.parent.parent / 'models' / 'base_yolo_models' / f'base_{model}_model'
model_name = f'{model}.pt'
model_path = model_directory / model_name

# Ensure the target directory exists
model_directory.mkdir(parents=True, exist_ok=True)

# Download the model to the specified directory if it does not already exist
if not model_path.exists():
    model = YOLO(model_name)  # This will trigger the download to the current directory
    model_path = Path.cwd() / model_name  # Temporary path where the model is downloaded
    model_path.rename(model_directory / model_name)  # Move the model to the target directory

# Load the pre-trained model from the specified directory and move it to the appropriate device
model = YOLO(str(model_directory / model_name))
model.to(device)
print('Loaded Model....')

# Define the base directory
base_directory = Path.cwd()
# Start the training process and measure time
epochs = 60
patience = 0
batch= 16
lr0=0.0001
lrf=0.0001
weight_decay=0.0005
close_mosaic=0
dropout=0.0
label_smoothing=0.0
seed=42
box = 20 # 7.5 is default
print('Starting Training.....')
start_time = time.time()
results = model.train(
    data=f"{base_directory}/dataset.yaml",
    epochs=epochs,
    patience=patience,  # Set patience for early stopping
    batch=batch,  # Adjust batch size if needed
    box=box, #
    lr0=lr0,  # Initial learning rate
    lrf=lrf,  # Final learning rate
    weight_decay=weight_decay,  # Regularization
    rect=True,  # Rectangular training
    cos_lr=False,  # Cosine learning rate scheduler
    close_mosaic=close_mosaic,  # Disable mosaic augmentation for final epochs
    dropout=dropout,  # Use dropout if applicable
    label_smoothing=label_smoothing,  # Label smoothing
    seed=seed,
    plots=True,
    save=True
)  # train the model
# More parameters that can be passed into model.train
    # resume = False/True # resume training from last checkpoint rather than training over again
end_time = time.time()
training_duration = end_time - start_time
print('Training Ended.....') 

# Evaluate model performance on the validation set
print('Model Results:')
val_results = model.val(data=f"{base_directory}/dataset.yaml")  # Evaluate on validation set
# print(val_results)

# Now we define source_directory here, before it's used
source_directory = base_directory / 'runs'

# Assuming the rest of your script is correct and above this block
# val_directory = source_directory / 'detect' / 'val'
# The new target directory for 'val' is alongside 'train' in the save_file_dir

# Define the path to the count_info.txt file
info_file_path = base_directory / 'runs' / 'detect' / 'train' / 'model_info.json'


test_dir = Path(f'{Path.cwd()}/data/test/images')  # Source directory for detection
train_dir = Path(f'{Path.cwd()}/data/train/images')  # Training images directory
val_dir = Path(f'{Path.cwd()}/data/val/images')  # Validation images directory

num_test_images = len(list(test_dir.glob('*.png')))
num_train_images = len(list(train_dir.glob('*.png')))
num_val_images = len(list(val_dir.glob('*.png')))
total_images = num_test_images + num_train_images + num_val_images

# Open the count_info.txt file to append model, training duration, and last epoch metrics
data = {
    "Model": model_name,
    "Training Duration": f"{training_duration} seconds",
    "Number of test images": num_test_images,
    "Number of train images": num_train_images,
    "Number of val images": num_val_images,
    "Total number of images": total_images,
    "Epochs": epochs,
    "Patience": patience,
    "Batch": batch,
    "Initial Learning Rate": lr0,
    "Final Learning Rate": lrf,
    "Weight Decay": weight_decay,
    "Close Mosaic": close_mosaic,
    "Dropout": dropout,
    "Label Smoothing": label_smoothing,
    "Seed": seed,
    "Box": box
}

# Define the path to the results.csv file
results_file_path = base_directory / 'runs/detect' / 'train' / 'results.csv'

# Check if the results.csv exists
if results_file_path.exists():
    # Read the results.csv file
    results_df = pd.read_csv(results_file_path)

    # Drop rows where all selected metric columns are NA
    results_df.dropna(subset=results_df.columns[1:11], how='all', inplace=True)

    # Ensure there is at least one row left after dropping NA rows
    if not results_df.empty:
        # Get the last row with data
        last_epoch_metrics = results_df.iloc[-1]

        # Select the 2nd to the 11th columns by their index positions
        selected_metrics = last_epoch_metrics.iloc[1:11].to_dict()

        # Clean up column names and add to data dictionary
        for column_name, value in selected_metrics.items():
            clean_column_name = column_name.strip().replace('/', ' / ').title()
            data[clean_column_name] = value

        print(f"Metrics from the last epoch have been added to {info_file_path}")
    else:
        print("The DataFrame is empty after dropping rows with NA values.")
else:
    print(f"The file {results_file_path} does not exist, could not write last epoch metrics.")

# Write data to JSON file
with open(info_file_path, 'w') as json_file:
    json.dump(data, json_file, indent=4)

# Versioning and save file directory setup

save_file_dir = Path.cwd().parent.parent.parent / f'models/data_labeling_model/version{version[0]}/version{version}'

# Create the target directory if it does not exist
save_file_dir.mkdir(parents=True, exist_ok=True)
# new_val_directory = save_file_dir / 'runs' / 'detect' / 'val'
# Define the source directory (runs folder)
source_directory = base_directory / 'runs'

# Move the runs directory to the save_file_dir
if source_directory.exists():
    target_directory = save_file_dir / 'runs'
    if target_directory.exists():
        shutil.rmtree(target_directory)  # Remove the target if it exists to avoid merge conflicts
    shutil.move(str(source_directory), str(save_file_dir))
    print(f"Moved {source_directory} to {save_file_dir}")
else:
    print(f"The directory {source_directory} does not exist.")