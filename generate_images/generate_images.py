import generate_images_functions
from pathlib import Path

def main():
    # Base directory for the league_object_detection_tracking folder
    base_directory = generate_images_functions.get_base_directory()
    # print(f"base_directory: {base_directory}")

    # Paths to the 'models' and 'images' directories
    models_directory = base_directory / 'models'

    output_dir = base_directory / 'images'
    # Print the models directory path for debugging
    # print(f"Models Directory: {models_directory}")

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Set a limit for the number of models to process
    models_limit = 18
    # Counter for models proccessed in loop
    models_processed = 0
    # Set a limit for the number of Tracks to process
    track_limit = 2
    # List of champions to process, leave empty to process all champions
    champions_to_process = ['Ahri']  # Add champion names like 'Ahri', 'Aatrox', etc.

    # Loop through each champion directory in the models directory
    for champion_dir in models_directory.iterdir():
        if models_processed >= models_limit:
            break  # Stop processing if the limit is reached
        if champion_dir.is_dir() and (not champions_to_process or champion_dir.name in champions_to_process):  # Ensure it is a directory
            champion_name = champion_dir.name  # Get the champion name
            # Loop through each skin directory within the champion's directory
            for skin_dir in champion_dir.iterdir():
                if skin_dir.is_dir():  # Ensure it is a directory
                    glb_file = skin_dir / f"{skin_dir.name}.glb"  # Construct the file path for the .glb file
                    skin_name = skin_dir.name  # Get the skin name
                    if glb_file.is_file():  # Check if the .glb file exists
                        # Clear the scene for each new model import
                        generate_images_functions.clear_scene()
                        
                        # Set up multiple cameras
                        generate_images_functions.setup_cameras()

                        # Try to import the GLB file
                        try:
                            bpy.ops.import_scene.gltf(filepath=str(glb_file))
                        except RuntimeError as e:
                            print(f"Failed to import {glb_file}: {e}")
                            generate_images_functions.log_failed_imports(champion_name, skin_name)
                            continue  # Skip to the next file

                        # Disable backface culling for all objects in the scene
                        for obj in bpy.data.objects:
                            generate_images_functions.disable_backface_culling(obj)

                        # Find the name of the object with animation data
                        animated_object_name = generate_images_functions.find_objects_with_animation()
                        if animated_object_name:
                            print(f"Found animated object: {animated_object_name}")

                            # Find untracked actions for the animated object
                            untracked_actions = generate_images_functions.find_untracked_actions(animated_object_name)
                            print(f"Untracked actions for '{animated_object_name}': {untracked_actions}")

                            # Move untracked actions to NLA tracks
                            for action_name in untracked_actions:
                                generate_images_functions.move_action_to_nla(animated_object_name, action_name)

                            # Process all NLA tracks for the animated object
                            generate_images_functions.process_all_tracks(animated_object_name, champion_name, skin_name, track_limit)
                            
                        else:
                            print("No animated objects found in this model.")
                    models_processed += 1  # Increment the counter after processing a model
                    if models_processed >= models_limit:
                        break  # Stop processing if the limit is reached

if __name__ == "__main__":
    main()