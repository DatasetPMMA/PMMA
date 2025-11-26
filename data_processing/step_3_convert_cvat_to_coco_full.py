import xml.etree.ElementTree as ET
import json
import os

# 视频配置
video_cfg = {
    1: {
        "xml_path": "./raw_data/annotations_xml/video_1_annotations.xml",
        "prefix": "",
        "ranges": [(0, 8999)],
        "reindex_func": lambda f: f
    },
    2: {
        "xml_path": "./raw_data/annotations_xml/video_2_annotations.xml",
        "prefix": "",
        "ranges": [(7301, 9000), (1800, 6156)],
        "reindex_func": lambda f: f - 7301 + 10000 if 7301 <= f <= 9000 else f - 1800 + 20000
    },
    3: {
        "xml_path": "./raw_data/annotations_xml/video_3_annotations.xml",
        "prefix": "",
        "ranges": [(0, 14637)],
        "reindex_func": lambda f: f + 30000
    }
}

output_json = "./raw_data/annotations/merged_videos_coco.json"
IMAGE_WIDTH = 2208
IMAGE_HEIGHT = 1242

images = []
annotations = []
categories = []
category_name_to_id = {}
image_ids_seen = set()
ann_id = 0

def is_in_ranges(frame, ranges):
    return any(start <= frame <= end for start, end in ranges)

for vid, cfg in video_cfg.items():
    print(f"Processing video {vid}...")
    tree = ET.parse(cfg["xml_path"])
    root = tree.getroot()

    # --- Step 1: collect all frames from <box> and ensure all valid frames are added to images ---
    all_valid_frames = set()
    for r in cfg["ranges"]:
        all_valid_frames.update(range(r[0], r[1] + 1))  # inclusive

    for frame in sorted(all_valid_frames):
        new_id = cfg["reindex_func"](frame)
        file_name = f"{cfg['prefix']}{new_id:06d}.png"
        if new_id not in image_ids_seen:
            images.append({
                "id": new_id,
                "file_name": file_name,
                "width": IMAGE_WIDTH,
                "height": IMAGE_HEIGHT
            })
            image_ids_seen.add(new_id)

    # --- Step 2: handle annotations from <box> ---
    for track in root.findall("track"):
        label = track.attrib["label"]
        if label not in category_name_to_id:
            cid = len(category_name_to_id) + 1
            category_name_to_id[label] = cid
            categories.append({"id": cid, "name": label})
        cid = category_name_to_id[label]

        for box in track.findall("box"):
            orig_frame = int(box.attrib["frame"])
            if not is_in_ranges(orig_frame, cfg["ranges"]):
                continue
            new_frame_id = cfg["reindex_func"](orig_frame)

            xtl = float(box.attrib['xtl'])
            ytl = float(box.attrib['ytl'])
            xbr = float(box.attrib['xbr'])
            ybr = float(box.attrib['ybr'])
            w = xbr - xtl
            h = ybr - ytl

            annotations.append({
                "id": ann_id,
                "image_id": new_frame_id,
                "category_id": cid,
                "bbox": [xtl, ytl, w, h],
                "area": w * h,
                "iscrowd": 0
            })
            ann_id += 1

# --- Final build and save ---
coco = {
    "images": images,
    "annotations": annotations,
    "categories": categories
}

with open(output_json, "w") as f:
    json.dump(coco, f, indent=2)

print(f"✅ COCO JSON saved to {output_json}")
print(f"📊 Total images: {len(images)}")
print(f"📦 Total annotations: {len(annotations)}")
print(f"🏷️ Categories: {[cat['name'] for cat in categories]}")