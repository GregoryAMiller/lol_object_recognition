from PIL import Image
from pathlib import Path

def overlay_images(background_path, overlay_path, output_path):
    """
    Overlays overlay_image on top of background_image and saves the result.
    
    :param background_path: Path to the background image.
    :param overlay_path: Path to the overlay image.
    :param output_path: Path where the resulting image will be saved, including filename and extension.
    """
    # Open the background and overlay images
    background_image = Image.open(background_path)
    overlay_image = Image.open(overlay_path)
    
    # Resize overlay image to match the background image's size
    overlay_image = overlay_image.resize(background_image.size)
    
    # Paste the overlay image on top of the background image
    if overlay_image.mode == 'RGBA':
        background_image.paste(overlay_image, (0, 0), overlay_image)
    else:
        background_image.paste(overlay_image, (0, 0))
    
    # Save the result
    background_image.save(output_path)

# Example usage with updated output_path to include filename and extension
map_dir = Path.cwd().parent.parent.parent / 'data/league_map_images' / 'image_0.jpg'
overlay_path = Path.cwd().parent.parent.parent / 'data/stage1/version3.0/images/Annie/Annie' / 'annie_2012_dance_loop_annie_2012_dance_loop_model_frame1_camera0.png'
output_path = Path.cwd() / 'output_image.jpg'  # Ensure this path includes the filename and extension

overlay_images(map_dir, overlay_path, output_path)