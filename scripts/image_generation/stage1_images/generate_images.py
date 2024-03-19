import generate_images_functions
from pathlib import Path
import bpy

def main():
    # Base directory for the league_object_detection_tracking folder
    base_directory = generate_images_functions.get_base_directory()
    # print(f"base_directory: {base_directory}")

    # Paths to the 'models' and 'images' directories
    models_directory = base_directory / 'data/3d_glb_files'
    # print(f"Models Directory: {models_directory}")

    version = '1.0'
    output_dir = base_directory / 'data/stage1' / f'version{version[0]}' / f'version{version}' / 'images'
    # print(f"output_dir: {output_dir}")
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Set a limit for the number of Tracks to process
    # track_limit = None # set to a integer to limit the number of tracks processed ex. track_limit = 10
    # List of champions to process, leave empty to process all champions
    champions_to_process = ['Ahri']  # Add champion names like 'Ahri', 'Aatrox', etc.
    skins_to_process = ['Academy Ahri']  # Add skin names to process, leave empty to process all skins for the specified champions
    max_images = None # set to number or none for auto interval

    # Loop through each champion directory in the models directory
    for champion_dir in models_directory.iterdir():
        if champion_dir.is_dir() and (not champions_to_process or champion_dir.name in champions_to_process):  # Ensure it is a directory

            champion_name = champion_dir.name  # Get the champion name

            # Loop through each skin directory within the champion's directory
            for skin_dir in champion_dir.iterdir():
                if skin_dir.is_dir() and (not skins_to_process or skin_dir.name in skins_to_process):  # Ensure it is a directory and check if the skin should be processed
                    # Attempt to find a GLB file in the directory
                    glb_files = list(skin_dir.glob('*.glb'))
                    if glb_files:
                        # Assuming there's only one GLB file per directory, get the first one
                        original_glb_path = glb_files[0]
                        # Construct new GLB file name to match the skin directory name, with '.glb' extension
                        new_glb_path = skin_dir / (skin_dir.name + ".glb")

                        # Rename the GLB file if it doesn't already have the desired name
                        if original_glb_path != new_glb_path:
                            print(f"Renaming GLB file from {original_glb_path} to {new_glb_path}")  # Debug print
                            original_glb_path.rename(new_glb_path)  # Using pathlib for renaming

                        # Update glb_file to the new or existing correct name
                        glb_file = new_glb_path
                    else:
                        print(f"No GLB file found in {skin_dir.name}. Skipping...")  # Debug print
                        continue  # Skip to the next directory if no GLB file is found
                    
                    skin_name = skin_dir.name  # Get the skin name

                    # Clear the scene for each new model import
                    generate_images_functions.clear_scene()

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
                    # main_object_name = generate_images_functions.find_main_object()
                    # print(f'animated_object_name: {animated_object_name}')
                    # print(f'main_object_name: {main_object_name}')

                    if animated_object_name:
                        print(f"Found animated object: {animated_object_name}")

                        # Find untracked actions for the animated object
                        untracked_actions = generate_images_functions.find_untracked_actions(animated_object_name)
                        print(f"Untracked actions for '{animated_object_name}': {untracked_actions}")

                        # Move untracked actions to NLA tracks
                        for action_name in untracked_actions:
                            generate_images_functions.move_action_to_nla(animated_object_name, action_name)

                        # Process all NLA tracks for the animated object
                        generate_images_functions.process_all_tracks(animated_object_name, champion_name, skin_name, output_dir, max_images)
                        
                    else:
                        print("No animated objects found in this model.")


if __name__ == "__main__":
    main()