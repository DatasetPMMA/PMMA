import json
import os

# Input and output
input_json = './raw_data/annotations/merged_videos_coco.json'
output_dir = './annotations'
os.makedirs(output_dir, exist_ok=True)

# Load the full COCO dataset
with open(input_json, 'r') as f:
    coco = json.load(f)

# Create a mapping from image_id to image
image_id_to_image = {img['id']: img for img in coco['images']}

# Splitting rules using reindexed IDs
splits = {
    'train': [(0, 8999), (30000, 43247)],
    'val': [(17301-7301, 19000-7301), (43277, 43809)],
    'test': [(21800-1800, 26156-1800), (43839, 44637)],
}


# Generate split JSONs
for split_name, ranges in splits.items():
    selected_images = []
    selected_ids = set()

    for img in coco['images']:
        img_id = img['id']
        if any(start <= img_id <= end for start, end in ranges):
            selected_images.append(img)
            selected_ids.add(img_id)

    selected_annotations = [
        ann for ann in coco['annotations'] if ann['image_id'] in selected_ids
    ]

    output_json = {
        'images': selected_images,
        'annotations': selected_annotations,
        'categories': coco['categories']
    }

    out_path = os.path.join(output_dir, f'{split_name}.json')
    with open(out_path, 'w') as f:
        json.dump(output_json, f)

    print(f'✅ {split_name}.json saved — {len(selected_images)} images, {len(selected_annotations)} annotations')