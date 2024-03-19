import bpy
import math
from pathlib import Path
from mathutils import Vector
import random 

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
def render_and_save(frame_number, track_name, strip_name, champion_name, skin_name, camera_number, output_dir):
    # ensure_camera_exists()
    bpy.context.scene.frame_set(frame_number)
    # Adjust the filename to include the strip name for uniqueness
    filename = f"{track_name}_{strip_name}_frame{frame_number}_camera{camera_number}.png"  # Use PNG to support transparency
    # Create directory path for the current champion and skin
    champion_skin_dir = Path(output_dir) / champion_name / skin_name
    champion_skin_dir.mkdir(parents=True, exist_ok=True)
    file_path = champion_skin_dir / filename
    bpy.context.scene.render.filepath = str(file_path)
    # Change render settings to output PNG format, which supports transparency
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    # Enable transparency in the render settings
    bpy.context.scene.render.film_transparent = True
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
def setup_cameras(object_name):
    obj = bpy.data.objects.get(object_name)
    if not obj:
        print(f"Object named {object_name} not found.")
        return

    # Calculate the size of the object's bounding box
    bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    obj_size = calculate_bbox_size(bbox_corners)

    # print(f'STATS: {obj_size}')

    # Calculate adjusted camera positions based adjusted_camera_settings = adjust_camera_positions_relative_to_object(
    #     object_name, base_scale=(1, 1, 1), base_camera_locations=base_camera_locations)on the object size
    # 

    # Define thresholds
    small_size_threshold = 300

    if obj_size < small_size_threshold:
        # More aggressive adjustments for very small objects
        adjusted_camera_settings = [
            ((-23.116 , 26.3025, 14.9586), (69.9249, 0.79381, 222.67), 'Camera1'),
            ((24.0246, -26.567, 12.7796 ), (71.52, 0.80116, -316.909), 'Camera1'),
            ((55.1704, 47.95, 23.925), (72.7251, 0.8062, 131.106), 'Camera1')
        ]
    else:
        # Use the provided base_camera_locations for larger objects
        adjusted_camera_settings = [
                ((2141.81, -1774.61, 1058.34 ), (69.5247, 0.790755, 49.8618), 'Camera1'),
                ((-2085.92, 1828.95, 1058.34), (69.5247, 0.790649, -131.338), 'Camera2'),
                ((3717.41 , 1079.67, 1844.11), (64.72, 0.7647, 105.8), 'Camera3')
            ]

    cameras = []
    # Add cameras to the scene based on the adjusted settings
    for location, rotation, name in adjusted_camera_settings:
        camera = add_camera(location, rotation, name)
        cameras.append(camera)
    
    return cameras

'''
        ((2141.81, -1774.61, 1058.34 ), (69.5247, 0.790755, 49.8618), 'Camera1'),
        ((-2085.92, 1828.95, 1058.34), (69.5247, 0.790649, -131.338), 'Camera2'),
        ((3717.41 , 1079.67, 1844.11), (64.72, 0.7647, 105.8), 'Camera3')

        # original camera locations
        ((12.391, -1412.3, 457.6), (76.4, 0, 0), 'Camera1'),
                ((250, 500, 400), (60, 0, 150), 'Camera2'),
                ((-350, 550, 450), (60, 0, 211), 'Camera3')


    '''
    

def calculate_bbox_size(bbox_corners):
    # Find min and max coordinates along each axis
    min_x = min(corner.x for corner in bbox_corners)
    max_x = max(corner.x for corner in bbox_corners)
    min_y = min(corner.y for corner in bbox_corners)
    max_y = max(corner.y for corner in bbox_corners)
    min_z = min(corner.z for corner in bbox_corners)
    max_z = max(corner.z for corner in bbox_corners)
    
    # Calculate dimensions
    width = max_x - min_x
    height = max_y - min_y
    depth = max_z - min_z
    
    # Calculate diagonal length as object size
    obj_size = math.sqrt(width**2 + height**2 + depth**2)
    return obj_size

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


def process_all_tracks(armature_name, champion_name, skin_name, output_dir, max_images=None, frame_interval=5):
    cameras = setup_cameras(armature_name)
    print(f'Armature: {armature_name}')
    armature = bpy.data.objects.get(armature_name)
    bpy.context.view_layer.objects.active = armature
    armature.select_set(True)

    if armature.animation_data and armature.animation_data.nla_tracks:
        for track in armature.animation_data.nla_tracks:
            track.mute = True

        total_frames = sum(int(track.strips[-1].frame_end) - int(track.strips[0].frame_start) + 1 for track in armature.animation_data.nla_tracks if track.strips)
        tracks_to_process = len(armature.animation_data.nla_tracks)
        frames_per_track = frame_interval if max_images is None else max(1, max_images // tracks_to_process)
        
        processed_images = 0
        for track in armature.animation_data.nla_tracks:
            if max_images is not None and processed_images >= max_images:
                break

            track.mute = False
            update_scene()

            for strip in track.strips:
                frame_start = int(strip.frame_start)
                frame_end = int(strip.frame_end)
                if max_images is None:
                    selected_frames = range(frame_start, frame_end + 1, frame_interval)
                else:
                    available_frames = range(frame_start, frame_end + 1)
                    frames_to_select = min(frames_per_track, len(available_frames))
                    selected_frames = random.sample(available_frames, frames_to_select) if frames_to_select < len(available_frames) else list(available_frames)

                for frame in selected_frames:
                    if max_images is not None and processed_images >= max_images:
                        break
                    for cam_num, camera in enumerate(cameras):
                        bpy.context.scene.camera = camera
                        render_and_save(frame, track.name, strip.name, champion_name, skin_name, cam_num, output_dir)
                        processed_images += 1
                        if max_images is None:
                            break  # Take one picture per selected frame and camera setup when max_images is None

            track.mute = True
            update_scene()

            if max_images is not None and processed_images >= max_images:
                break


# Function to get the base directory of the league_object_detection_tracking folder
def get_base_directory():
    # Use the Path class to get the current working directory
    return Path.cwd().parent.parent.parent

# Function to disable backface culling for all materials of a given object
def disable_backface_culling(obj):
    if obj.type == 'MESH':
        for mat_slot in obj.material_slots:
            if mat_slot.material:
                # Directly set use_backface_culling on the material, not the shader node
                mat_slot.material.use_backface_culling = False

def log_failed_imports(champion_name, skin_name, log_file='failed_imports_test.txt'):
    """
    Logs the names of champions and skins that failed to import to a text file.
    
    Args:
    champion_name (str): Name of the champion.
    skin_name (str): Name of the skin.
    log_file (str): Path to the log file.
    """
    with open(log_file, 'a') as file: 
        file.write(f"{champion_name} - {skin_name}\n")

def find_main_object():
    largest_volume = 0
    main_object = None
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            volume = obj.dimensions.x * obj.dimensions.y * obj.dimensions.z
            if volume > largest_volume:
                largest_volume = volume
                main_object = obj
    return main_object.name if main_object else None