import tkinter as tk
from annotation_gui_functions import AnnotationTool
# Main function to start the GUI
def main():
    root = tk.Tk()
    # root.geometry("1000x800")  # Set the size of the window
    default_label = 'Champion' # Set as None if you want to hand label every image, Set as 'Example' string to have it auto label everything as that label
    app = AnnotationTool(root, default_label)
    root.mainloop()
# # Run the main function in a separate thread
# thread = threading.Thread(target=main)
# thread.start()


if __name__ == "__main__":
    main()