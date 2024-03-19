from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from pathlib import Path
import random
from collections import defaultdict

def calculate_new_position_for_bbox(map_width, map_height, box_width, box_height, existing_boxes=[]):
    """
    Calculate a new position for the bounding box to ensure it's mostly within the map boundaries and doesn't overlap significantly with existing boxes.
    """
    max_attempts = 100
    for _ in range(max_attempts):
        # Ensure the bounding box is at least 80% within the map boundaries
        margin_width = box_width * 0.2
        margin_height = box_height * 0.2

        # Calculate the valid range for the top-left corner
        min_x = 0 + margin_width
        max_x = map_width - box_width - margin_width
        min_y = 0 + margin_height
        max_y = map_height - box_height - margin_height

        new_x = random.uniform(min_x, max_x)
        new_y = random.uniform(min_y, max_y)

        new_box = (new_x, new_y, new_x + box_width, new_y + box_height)
        if all(not _boxes_overlap(new_box, box, overlap_tolerance=0.3) for box in existing_boxes):
            return int(new_x), int(new_y)
    return None, None  # Return None if no non-overlapping position is found

def _boxes_overlap(box1, box2, overlap_tolerance=0.3):
    """
    Check if two boxes (x1, y1, x2, y2) overlap more than the allowed tolerance.
    
    :param box1: Tuple (x1, y1, x2, y2) defining the first box.
    :param box2: Tuple (x1, y1, x2, y2) defining the second box.
    :param overlap_tolerance: Float, the maximum allowed overlap ratio (0 to 1).
    :return: Boolean, True if boxes overlap more than allowed, False otherwise.
    """
    # Calculate the intersection rectangle
    x_left = max(box1[0], box2[0])
    y_top = max(box1[1], box2[1])
    x_right = min(box1[2], box2[2])
    y_bottom = min(box1[3], box2[3])

    # Check if there is no overlap
    if x_right < x_left or y_bottom < y_top:
        return False

    # Calculate intersection area
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # Calculate each box area
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])

    # Calculate the smallest box area
    min_area = min(box1_area, box2_area)

    # Allow overlap if intersection is less than tolerance times the smallest box area
    return intersection_area > overlap_tolerance * min_area

def place_images_on_map_adjusted_bbox(champion_images_paths, map_asset_path, labels_paths, output_dir, output_labels_dir, image_counter, champions_count):
    # Load the map asset
    map_img = Image.open(map_asset_path).convert('RGBA')
    map_width, map_height = map_img.size
    result_img = Image.new('RGBA', (map_width, map_height))
    result_img.paste(map_img, (0, 0))

    existing_boxes = []  # To keep track of the bounding boxes already placed
    new_labels_data = []
    map_image_name = Path(map_asset_path).stem  # Extract the name of the map image

    for champion_image_path, label_path in zip(champion_images_paths, labels_paths):
        with open(label_path, 'r') as file:
            label_data = file.readline().strip().split()

        champion_image_name = Path(champion_image_path).stem  # Extract the name of the champion image

        parts = champion_image_path.parts
        champion_name = parts[-3]
        skin_name = parts[-2]
        champions_count.setdefault(champion_name, {}).setdefault(skin_name, 0)
        champions_count[champion_name][skin_name] += 1

        champion_img = Image.open(champion_image_path).convert('RGBA')
        # Apply data augmentation
        champion_img, label_data = apply_data_augmentation(champion_img, label_data, map_width, map_height)

        box_width = float(label_data[3]) * map_width
        box_height = float(label_data[4]) * map_height
        new_x, new_y = calculate_new_position_for_bbox(map_width, map_height, box_width, box_height, existing_boxes)
        if new_x is None or new_y is None:
            continue  # If no suitable position is found, skip this image

        # Calculate original top-left corner position
        orig_x = float(label_data[1]) * map_width - box_width / 2
        orig_y = float(label_data[2]) * map_height - box_height / 2

        result_img.paste(champion_img, (new_x - int(orig_x), new_y - int(orig_y)), champion_img)
        existing_boxes.append((new_x, new_y, new_x + box_width, new_y + box_height))

        # Calculate new relative center coordinates
        new_x_center_rel = (new_x + box_width / 2) / map_width
        new_y_center_rel = (new_y + box_height / 2) / map_height
        new_labels_data.append(f"{label_data[0]} {new_x_center_rel} {new_y_center_rel} {label_data[3]} {label_data[4]}")

    if new_labels_data:
        # Generate filenames using the original image name and the map image name
        unique_filename = f"{champion_image_name}__{map_image_name}__{image_counter}.jpg"
        unique_labelname = f"{champion_image_name}__{map_image_name}__{image_counter}.txt"

        output_path = output_dir / unique_filename
        result_img = result_img.convert('RGB')  # Convert to RGB for saving
        result_img.save(output_path)

        output_label_path = output_labels_dir / unique_labelname
        with open(output_label_path, 'w') as file:
            for line in new_labels_data:
                file.write(line + "\n")


def apply_data_augmentation(image, label_data, map_width, map_height):
    # 1. Brightness adjustment
    if random.choice([True, False]):
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(random.uniform(0.7, 1.3))  # Adjust brightness randomly within 70% to 130%

    # 2. Adding blur
    if random.choice([True, False]):
        image = image.filter(ImageFilter.GaussianBlur(radius=random.uniform(0, 2)))  # Apply Gaussian blur with a random radius

    # 3. Mirroring the image
    if random.choice([True, False]):
        image = ImageOps.mirror(image)
        # Mirror the bounding box
        label_data = mirror_bbox(label_data, map_width)
    
    # 6. Contrast adjustment
    if random.choice([True, False]):
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(random.uniform(0.8, 1.2))  # Adjust contrast randomly within 80% to 120%

    # 7. Color adjustment
    if random.choice([True, False]):
        image = adjust_colors(image)

    return image, label_data

def mirror_bbox(label_data, map_width):
    """
    Mirror the bounding box coordinates in the horizontal direction based on the image width.
    Correctly adjusts the bounding box to stay on the mirrored object.
    """
    # Convert relative coordinates to absolute
    x_center_rel = float(label_data[1])
    box_width_rel = float(label_data[3])

    # Convert relative to absolute dimensions for calculation
    x_center_abs = x_center_rel * map_width
    box_width_abs = box_width_rel * map_width

    # Calculate the distance from the original right edge of the bounding box to the right edge of the image
    distance_to_right_edge = map_width - (x_center_abs + box_width_abs / 2)

    # The new left edge of the bounding box is this same distance from the left edge of the image
    new_left_edge_abs = distance_to_right_edge

    # The new center is halfway across the bounding box from the new left edge
    new_x_center_abs = new_left_edge_abs + box_width_abs / 2

    # Convert the new center to relative coordinates
    new_x_center_rel = new_x_center_abs / map_width

    # Update the label data with the new relative center
    label_data[1] = str(new_x_center_rel)

    return label_data

def adjust_colors(image):
    """
    Adjust the colors of the image without affecting transparent pixels.
    """
    r, g, b, a = image.split()  # Split into channels
    r = r.point(lambda i: i * random.uniform(0.9, 1.1) % 256)
    g = g.point(lambda i: i * random.uniform(0.9, 1.1) % 256)
    b = b.point(lambda i: i * random.uniform(0.9, 1.1) % 256)
    # Reassemble the image using the original alpha channel to preserve transparency
    return Image.merge('RGBA', (r, g, b, a))

def main():
    max_images_per_skin = 200  # The desired number of placements for each skin
    champions_count = defaultdict(lambda: defaultdict(int))  # Tracks placements for each skin

    stage1_version = '1.0'
    final_data_version = '1.0'

    base_dir = Path.cwd().parent.parent.parent
    map_assets_path = base_dir / 'data/league_map_images'
    champion_images_path = base_dir / 'data/stage1' / f'version{stage1_version[0]}' / f'version{stage1_version}' / 'images'
    labels_dir = base_dir / 'data/stage1' / f'version{stage1_version[0]}' / f'version{stage1_version}' / 'labels'
    output_dir = base_dir / 'data/synthetic/' / f'version{final_data_version[0]}' / f'version{final_data_version}' / 'images'
    output_labels_dir = base_dir / 'data/synthetic/' / f'version{final_data_version[0]}' / f'version{final_data_version}' / 'labels'
    summary_path = Path.cwd() / 'placement_summary.txt'

    output_dir.mkdir(parents=True, exist_ok=True)
    output_labels_dir.mkdir(parents=True, exist_ok=True)

    all_map_assets = list(map_assets_path.glob('*.jpg'))
    if not all_map_assets:
        print("No map assets found.")
        return

    # Load champion skin images and initialize tracking for placements
    champion_skin_groups = {}
    for img_path in champion_images_path.glob('**/*.png'):
        parts = img_path.parts
        champion_name, skin_name = parts[-3], parts[-2]
        champion_skin_groups.setdefault(champion_name, {}).setdefault(skin_name, []).append(img_path)

    # Flatten the list of all skins to manage their placements directly
    all_skins = [(champ, skin, img) for champ, skins in champion_skin_groups.items() for skin, imgs in skins.items() for img in imgs]

    # Initialize a counter for each skin image
    skin_usage_counts = defaultdict(int)

    # Main loop to place each skin max_images_per_skin times
    image_counter = 1
    while any(count < max_images_per_skin for count in skin_usage_counts.values()):
        for champ, skin, img_path in all_skins:
            # Check if this skin needs more placements
            if skin_usage_counts[(champ, skin, str(img_path))] >= max_images_per_skin:
                continue

            map_asset_path = random.choice(all_map_assets)
            selected_images = [img_path]
            label_path = labels_dir / img_path.relative_to(champion_images_path).with_suffix('.txt')
            labels_paths = [label_path] if label_path.exists() else []

            if labels_paths:
                place_images_on_map_adjusted_bbox(selected_images, map_asset_path, labels_paths, output_dir, output_labels_dir, image_counter, champions_count)
                image_counter += 1

                # Update usage count for this skin
                skin_usage_counts[(champ, skin, str(img_path))] += 1

                # Break if all skins have reached the max_images_per_skin limit
                if all(count >= max_images_per_skin for count in skin_usage_counts.values()):
                    break

    # Write summary information
    with open(summary_path, 'w') as f:
        for (champion, skin, _), count in skin_usage_counts.items():
            f.write(f"{champion} - {skin}: {count}\n")

if __name__ == "__main__":
    main()