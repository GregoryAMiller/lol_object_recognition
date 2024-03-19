import tkinter as tk
from annotation_gui_functions import AnnotationTool

# Main function to start the GUI
def main():

    root = tk.Tk()

    # Set as None if you want to hand label every image, Set as 'Example' string to have it auto label everything as that label
    default_label = 'Champion'
    version = 'version3.0'

    app = AnnotationTool(root, default_label, version)
    root.mainloop()

if __name__ == "__main__":
    main()