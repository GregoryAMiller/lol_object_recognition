import tkinter as tk
from tkinter import simpledialog, filedialog
from PIL import Image, ImageTk
import cv2
# import os
from pathlib import Path
import csv
import tkinter.ttk as ttk
# import threading
import random


class AnnotationTool:
    def __init__(self, root, default_label=None):
        self.root = root
        self.default_label = default_label
        self.root.title("Annotation Tool")

        # Frame for buttons
        button_frame = tk.Frame(root, bg='gray')
        button_frame.pack(side="bottom", fill="x")

        # Styling buttons
        button_style = {'bg': 'lightblue', 'fg': 'black'}

        # Pack buttons and entry inside the button frame
        self.goto_image_entry = tk.Entry(button_frame, width=10)
        self.goto_image_entry.configure(state='normal')
        self.goto_image_entry.pack(side="left")

        # Add a label to show the current image index
        self.current_image_label = tk.Label(button_frame, text="", bg='gray', fg='white')
        self.current_image_label.pack(side="left", fill="x")

        self.goto_button = tk.Button(button_frame, text="Go To", command=self.goto_image, **button_style)
        self.goto_button.pack(side="left")

        self.previous_button = tk.Button(button_frame, text="Previous", command=self.previous_image, **button_style)
        self.previous_button.pack(side="left")

        self.skip_button = tk.Button(button_frame, text="Skip", command=self.skip_current_image, **button_style)
        self.skip_button.pack(side="left")

        # Confirm, Delete, Reset buttons
        
        self.delete_button = tk.Button(button_frame, text="Delete", command=self.delete_current_image, **button_style)
        self.delete_button.pack(side="left")
        # Reset Current Box button
        self.reset_current_button = tk.Button(button_frame, text="Reset Current Box", command=self.reset_current_box, **button_style)
        self.reset_current_button.pack(side="left")

        # Reset Previous Box button
        self.reset_previous_button = tk.Button(button_frame, text="Reset Previous Box", command=self.reset_previous_box, **button_style)
        self.reset_previous_button.pack(side="left")

        # Reset All Boxes button
        self.reset_all_button = tk.Button(button_frame, text="Reset All Boxes", command=self.reset_all_boxes, **button_style)
        self.reset_all_button.pack(side="left")

        self.confirm_button = tk.Button(button_frame, text="Confirm", command=self.confirm_annotations, **button_style)
        self.confirm_button.pack(side="left")

        # Set fixed size and background for the canvas
        self.canvas = tk.Canvas(root, width=1200, height=900, bg='black', cursor="cross")
        self.canvas.pack()

        # Rest of the initialization code
        self.image_dir = filedialog.askdirectory(title="Select Image Directory")
        self.images = []
        self.current_image_index = 0
        self.current_image = None
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.rect_label = None
        self.annotations = []
        self.load_images()
        self.display_next_image()
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        # Initialize the current image label
        self.update_image_label()

    def previous_image(self):
        # Check if there is a previous image
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.display_next_image()
        else:
            print("No previous images.")

    def update_image_label(self):
        # Correct the displayed index to be 1-based and in sync with the actual image
        text = f"Image {self.current_image_index + 1} of {len(self.images)}"
        self.current_image_label.config(text=text)

    def goto_image(self):
        try:
            image_number = int(self.goto_image_entry.get()) - 1
            if 0 <= image_number < len(self.images):
                self.current_image_index = image_number - 1  # Set to one less since display_next_image increments
                self.display_next_image()
            else:
                print("Invalid image number. Please enter a number between 1 and", len(self.images))
        except ValueError:
            print("Please enter a valid number.")

    def skip_current_image(self):
        # Increment the index by one and then display the next image
        if self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            self.display_next_image()
        else:
            print("No more images to skip.")

    def reset_current_box(self):
        # Delete the current rectangle and reset start coordinates
        if self.rect:
            self.canvas.delete(self.rect)
            self.rect = None
            self.start_x = None
            self.start_y = None
    
    def reset_previous_box(self):
        # Delete the last drawn rectangle and its annotation
        if self.annotations:
            last_annotation = self.annotations.pop()
            self.canvas.delete(last_annotation['rect_id'])
            if 'label_id' in last_annotation:
                self.canvas.delete(last_annotation['label_id'])

    def reset_all_boxes(self):
        # Delete all rectangles and their annotations
        for annotation in self.annotations:
            self.canvas.delete(annotation['rect_id'])
            if 'label_id' in annotation:
                self.canvas.delete(annotation['label_id'])
        self.annotations.clear()

    def load_images(self):
        # Use pathlib to list image files
        image_dir = Path(self.image_dir)
        self.images = [str(f) for f in image_dir.glob('*') if f.suffix.lower() in ['.png', '.jpg', '.jpeg']]

    def display_next_image(self):
        # Update the label before displaying the image
        self.update_image_label()

        canvas_width = 1200
        canvas_height = 1000

        if self.current_image_index < len(self.images):
            self.canvas.delete("all")  # Clear the previous image and box

            image_dir = Path(self.image_dir)
            original_image = Image.open(image_path)

            # Calculate the new size maintaining aspect ratio
            ratio = min(canvas_width / original_image.width, canvas_height / original_image.height)
            new_width = int(original_image.width * ratio)
            new_height = int(original_image.height * ratio)

            # Resize the image for display
            display_image = original_image.resize((new_width, new_height), Image.ANTIALIAS)
            self.current_image = ImageTk.PhotoImage(display_image)

            # Calculate position to center the image
            x = (canvas_width - new_width) // 2
            y = (canvas_height - new_height) // 2
            self.canvas.create_image(x, y, anchor='nw', image=self.current_image)

        else:
            print("No more images.")
            self.root.quit()
    
    def delete_current_image(self):
        if self.current_image_index > 0:
            current_image_path = Path(self.images[self.current_image_index - 1])
            try:
                current_image_path.unlink()  # Delete the current image file
                print(f"Deleted: {current_image_path}")
            except OSError as e:
                print(f"Error: {e.strerror}")
            
            # Remove the deleted image from the list and adjust the index
            del self.images[self.current_image_index - 1]
            self.current_image_index -= 1
        
        self.display_next_image()  # Display the next image

    def on_button_press(self, event):
        # Start drawing the bounding box
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline='red')
        # Bind the motion event to dynamically update the bounding box
        self.canvas.bind("<Motion>", self.on_mouse_move)

    def on_mouse_move(self, event):
        # Update the size of the rectangle as the mouse is moving
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)
    
    def on_button_release(self, event):
        # Unbind the motion event
        self.canvas.unbind("<Motion>")

        # Finalize the size of the rectangle
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

        # Use the given default label if it's not None, otherwise prompt for a label
        label = self.default_label if self.default_label is not None else simpledialog.askstring("Label", "Enter the label:")
        if label:
            color = self.get_unique_color()
            self.canvas.itemconfig(self.rect, outline=color)

            # Create and store the label text element
            label_x = event.x + 10
            label_y = event.y - 20
            self.rect_label = self.canvas.create_text(label_x, label_y, text=label, anchor='nw', fill=color)

            # Calculate normalized coordinates
            x_center = (self.start_x + event.x) / 2
            y_center = (self.start_y + event.y) / 2
            width = abs(event.x - self.start_x)
            height = abs(event.y - self.start_y)

            # Append annotation to the list
            self.annotations.append({
                'image': self.images[self.current_image_index - 1],
                'bbox': [self.start_x, self.start_y, event.x, event.y],
                'label': label,
                'rect_id': self.rect,  # Store rectangle ID
                'label_id': self.rect_label  # Store label ID
            })
        else:
            # Delete the rectangle if labeling is canceled
            self.reset_current_box()

    def reset_current_box(self):
        # Check if there is a current rectangle
        if self.rect:
            # Delete the rectangle from the canvas
            self.canvas.delete(self.rect)
            self.rect = None

            # Also delete the associated label, if any
            if self.rect_label:
                self.canvas.delete(self.rect_label)
                self.rect_label = None

            # Remove the last added annotation for the current image
            # Assuming the last annotation added corresponds to the current box
            if self.annotations and self.annotations[-1]['image'] == self.images[self.current_image_index - 1]:
                self.annotations.pop()

    def get_unique_color(self):
        # Function to generate a unique color for each box
        # This can be as simple or complex as needed
        r = lambda: random.randint(0,255)
        return f'#{r():02x}{r():02x}{r():02x}'

    def save_annotations(self):
        label_dir = Path.cwd() / 'labels'
        label_dir.mkdir(exist_ok=True)

        if self.current_image_index < len(self.images):
            current_image_path = Path(self.images[self.current_image_index - 1])
            current_image_annotations = [ann for ann in self.annotations if ann['image'] == str(current_image_path)]

            print(f"Saving annotations for: {current_image_path}")  # Debugging
            print(f"Annotations: {current_image_annotations}")  # Debugging

            with Image.open(current_image_path) as img:
                img_width, img_height = img.size

            # Use Path.stem to get the file name without the suffix
            file_name = f"{current_image_path.stem}.txt"
            file_path = label_dir / file_name
            print(f"Saving file: {file_path}")

            with file_path.open('w') as file:
                for ann in current_image_annotations:
                    # Normalize coordinates
                    x_center = (ann['bbox'][0] + ann['bbox'][2]) / 2 / img_width
                    y_center = (ann['bbox'][1] + ann['bbox'][3]) / 2 / img_height
                    width = abs(ann['bbox'][2] - ann['bbox'][0]) / img_width
                    height = abs(ann['bbox'][3] - ann['bbox'][1]) / img_height

                    # Use the label provided by the user for each bounding box
                    file.write(f"{ann['label']} {x_center} {y_center} {width} {height}\n")

    def confirm_annotations(self):
        # Save annotations for the current image
        self.save_annotations()

        # Clear annotations for the current image
        self.annotations = [ann for ann in self.annotations if ann['image'] != self.images[self.current_image_index - 1]]

        # Check if there are more images and display the next one
        if self.current_image_index < len(self.images) - 1:
            self.canvas.delete("all")  # Clear the canvas for the next image
            self.current_image_index += 1  # Increment the index to move to the next image
            self.display_next_image()
        else:
            print("No more images.")
            self.root.quit()

# Main function to start the GUI
def main():
    root = tk.Tk()
    # root.geometry("1000x800")  # Set the size of the window
    default_label = 'Champion' # Set as None if you want to hand label every image
    app = AnnotationTool(root, default_label)
    root.mainloop()
# # Run the main function in a separate thread
# thread = threading.Thread(target=main)
# thread.start()