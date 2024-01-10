from ultralytics import YOLO
from pathlib import Path
import torch
# Check for GPU and use it if available for faster training
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Using {device} device for training.')

# Load the pre-trained model from Ultralytics and move it to the appropriate device
model = YOLO('ultralyticsplus/yolov8s.pt')
print('Loaded Model....')

# Define the base directory (ensure it's correct)
base_directory = Path.cwd()

print('Starting Training.....')
results = model.train(
    data=f"{base_directory}/dataset.yaml",
    epochs=10,
    batch=16,  # Use 'batch' instead of 'batch_size'
    imgsz=640,  # Image size
    device=device,  # Device to train on
    seed=42,
    plots=True
)  # train the model
print('Training Ended.....')

# Export the model to the working directory
print('Exporting Model')
model.export(export_dir=f'{base_directory}/')
print('Model Exported to {base_directory}/')

# Evaluate model performance on the validation set
print('Model Results:')
results = model.val(data=f"{base_directory}/dataset.yaml")  # Evaluate on validation set
print(results)  # print results