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
    patience=10,  # Set patience for early stopping
    batch=16,  # Adjust batch size if needed
    lr0=0.01,  # Initial learning rate
    lrf=0.01,  # Final learning rate
    weight_decay=0.0005,  # Regularization
    rect=True,  # Rectangular training
    cos_lr=False,  # Cosine learning rate scheduler
    close_mosaic=10,  # Disable mosaic augmentation for final epochs
    dropout=0.0,  # Use dropout if applicable
    label_smoothing=0.0,  # Label smoothing
    seed=42,
    plots=True,
    save=True
)  # train the model
# More parameters that can be passed into model.train
    # resume = False/True # resume training from last checkpoint rather than training over again
print('Training Ended.....')  

# Export the model to the working directory
# print('Exporting Model')
# model.export(export_dir=f'{base_directory}/')
# print('Model Exported to {base_directory}/')

# Evaluate model performance on the validation set
print('Model Results:')
results = model.val(data=f"{base_directory}/dataset.yaml")  # Evaluate on validation set
print(results)  # print results