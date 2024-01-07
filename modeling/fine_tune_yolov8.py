from ultralytics import YOLO
from pathlib import Path


model = YOLO('ultralyticsplus/yolov8s.pt')
print('Loaded Model....')
base_directory = Path.cwd().parent
print('Starting Training.....')
results = model.train(data=f"{Path.cwd()}/dataset.yaml", epochs=10, seed=42, plots=True, save=True)  # train the model
print('Training Ended.....')
print('Exporting Model')
# Export the model
# model.export()
model.export(export_dir=f'{Path.cwd()}/', name='ahri_small_test1.pt')
print('Model Results:')
results = model.val()  # evaluate model performance on the validation set
print(results) # print results

