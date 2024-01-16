from ultralytics import YOLO
from pathlib import Path


model = YOLO('ultralyticsplus/yolov8s.pt')
print('Loaded Model....')
base_directory = Path.cwd().parent
print('Starting Training.....')
results = model.train(
    data=f"{Path.cwd()}/dataset.yaml",
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
)
#     imgsz=640,  # Image size
print('Training Ended.....')
# print('Exporting Model')
# # Export the model
# # model.export()
# model.export(export_dir=f'{Path.cwd()}/', name='ahri_small_test1.pt')
print('Model Results:')
results = model.val()  # evaluate model performance on the validation set
print(results) # print results

