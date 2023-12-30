import bpy
import math
from pathlib import Path


# Function to ensure there is an active camera in the scene
# def ensure_camera_exists():
#     # Check if there is any camera in the scene
#     cameras = [obj for obj in bpy.data.objects if obj.type == 'CAMERA']
#     if cameras:
#         # Set the first found camera as the active camera
#         bpy.context.scene.camera = cameras[0]
#     else:
#         # Create and set up the camera
#         bpy.ops.object.camera_add(location=(12.391, -1412.3, 457.6))
#         camera = bpy.context.object
#         camera.data.type = 'PERSP'
#         camera.data.clip_end = 100000
#         camera.rotation_mode = 'XYZ'
#         camera.rotation_euler[0] = math.radians(76.4)
#         camera.rotation_euler[1] = math.radians(-0.000029)
#         camera.rotation_euler[2] = math.radians(-0.000001)
#         bpy.context.scene.camera = camera

def set_active_camera_by_name(camera_name):
    if camera_name in bpy.data.cameras:
        # Set the active camera
        bpy.context.scene.camera = bpy.data.objects[camera_name]
        print(f"Active camera set to {camera_name}")
    else:
        print(f"Camera named {camera_name} not found in the scene.")


# Function to update the scene and context
def update_scene():
    bpy.context.view_layer.update()
    bpy.context.evaluated_depsgraph_get().update()


# Function to render and save the image in the specified directory structure
def render_and_save(frame_number, track_name, strip_name, champion_name, skin_name, camera_number):
    # ensure_camera_exists()
    bpy.context.scene.frame_set(frame_number)
    # Adjust the filename to include the strip name for uniqueness
    filename = f"{track_name}_{strip_name}_frame{frame_number}_camera{camera_number}.png"
    # Create directory path for the current champion and skin
    output_dir = get_base_directory() / 'images'
    champion_skin_dir = Path(output_dir) / champion_name / skin_name
    champion_skin_dir.mkdir(parents=True, exist_ok=True)
    file_path = champion_skin_dir / filename
    bpy.context.scene.render.filepath = str(file_path)
    bpy.ops.render.render(write_still=True)


# Function to clear all objects in the scene
def clear_scene():
    # Select and delete all objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    # Purge orphan data
    bpy.ops.outliner.orphans_purge()

# Function to add a camera at a specific location and rotation
def add_camera(location, rotation_euler_degrees, name):
    bpy.ops.object.camera_add(location=location)
    camera = bpy.context.object
    camera.data.type = 'PERSP'
    camera.data.clip_end = 100000
    camera.rotation_mode = 'XYZ'
    # Convert degrees to radians and apply rotation
    camera.rotation_euler = [math.radians(angle) for angle in rotation_euler_degrees]
    camera.name = name  # Set the name of the camera
    return camera

# Function to set up multiple cameras
def setup_cameras():
    # ((50, -1300, 400), (80, 0, 15), 'Camera2'),
    # ((-30, -1250, 420), (75, 0, -15), 'Camera3')
    # Define test locations and rotations for cameras
    camera_settings = [
        ((12.391, -1412.3, 457.6), (76.4, 0, 0), 'Camera1'),
        ((250, 500, 400), (60, 0, 150), 'Camera2'),
        ((-350, 550, 450), (60, 0, 211), 'Camera3')

    ]
    cameras = []
    # Add cameras to the scene
    for location, rotation, name in camera_settings:
        camera = add_camera(location, rotation, name)
        cameras.append(camera)
    return cameras

# Function to find objects with animation data
def find_objects_with_animation():
    for obj in bpy.data.objects:
        if obj.animation_data and obj.animation_data.action:
            return obj.name
    return None

def find_untracked_actions(armature_name):
    armature = bpy.data.objects.get(armature_name)
    untracked_actions = []

    # Include the current active action if it exists
    if armature.animation_data and armature.animation_data.action:
        untracked_actions.append(armature.animation_data.action.name)

    # Include all linked actions
    for action in bpy.data.actions:
        if action.users and not action.use_fake_user:
            # Check if the action is not already in an NLA track
            if not any(strip.action == action for track in armature.animation_data.nla_tracks for strip in track.strips):
                untracked_actions.append(action.name)

    return list(set(untracked_actions))  # Return unique action names

# Function to move an action to NLA tracks
def move_action_to_nla(armature_name, action_name):
    armature = bpy.data.objects.get(armature_name)
    if armature.animation_data and armature.animation_data.action:
        action = armature.animation_data.action
        if action.name == action_name:
            if not armature.animation_data.nla_tracks:
                armature.animation_data_create()
            
            new_track = armature.animation_data.nla_tracks.new()
            new_track.name = action.name
            new_strip = new_track.strips.new(action.name, int(action.frame_range[0]), action)
            new_strip.action = action
            armature.animation_data.action = None
            print(f"Moved action '{action_name}' into a new NLA track.")
        else:
            print(f"The active action is not '{action_name}', it's '{action.name}'.")
    else:
        print(f"No active action on armature '{armature_name}' to move.")


def process_all_tracks(armature_name, champion_name, skin_name, track_limit=None):
    cameras = setup_cameras()
    armature = bpy.data.objects.get(armature_name)
    bpy.context.view_layer.objects.active = armature
    armature.select_set(True)

    if armature.animation_data:
        # First mute all tracks
        for track in armature.animation_data.nla_tracks:
            track.mute = True
        tracks_processed = 0
        for track in armature.animation_data.nla_tracks:
            if track_limit is not None and tracks_processed >= track_limit:
                break  # Stop processing if the limit is reached

            track.mute = False
            update_scene()  # Update scene after unmuting the track

            for strip in track.strips:
                frame_start = int(strip.frame_start)
                frame_end = int(strip.frame_end)
                animation_length = frame_end - frame_start

                # Adjusted dynamic interval calculation
                interval = animation_length // 5 + 1
                # if animation_length <= 20:
                #     interval = 2
                # elif animation_length <= 100:
                #     interval = max(2, animation_length // 20)
                # else:
                #     interval = max(5, animation_length // 50)

                # Render at calculated intervals within this strip
                for frame in range(frame_start, frame_end + 1, interval):
                    for cam_num, camera in enumerate(cameras):
                        bpy.context.scene.camera = camera
                        render_and_save(frame, track.name, strip.name, champion_name, skin_name, cam_num)

            track.mute = True
            update_scene()

            tracks_processed += 1  # Increment the counter after processing a track


# Function to get the base directory of the league_object_detection_tracking folder
def get_base_directory():
    # Use the Path class to get the current working directory
    return Path.cwd().parent

# Function to disable backface culling for all materials of a given object
def disable_backface_culling(obj):
    if obj.type == 'MESH':
        for mat_slot in obj.material_slots:
            if mat_slot.material:
                # Directly set use_backface_culling on the material, not the shader node
                mat_slot.material.use_backface_culling = False

def log_failed_imports(champion_name, skin_name, log_file='failed_imports.txt'):
    """
    Logs the names of champions and skins that failed to import to a text file.
    
    Args:
    champion_name (str): Name of the champion.
    skin_name (str): Name of the skin.
    log_file (str): Path to the log file.
    """
    with open(log_file, 'a') as file:  # 'a' mode appends to the file without overwriting existing data
        file.write(f"{champion_name} - {skin_name}\n")