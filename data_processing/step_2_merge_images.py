import os
import shutil

# Define frame copy instructions
copy_plan = [
    {
        "src_dir": "./raw_data/frames_video_1_left",
        "start": 0,
        "end": 8999,
        "new_start": 0
    },
    {
        "src_dir": "./raw_data/frames_video_2_left",
        "start": 7301,
        "end": 8999,
        "new_start": 10000
    },
    {
        "src_dir": "./raw_data/frames_video_2_left",
        "start": 1800,
        "end": 6156,
        "new_start": 20000
    },
    {
        "src_dir": "./raw_data/frames_video_3_left",
        "start": 0,
        "end": 14637,
        "new_start": 30000
    }
]

# Output folder
output_dir = "./raw_data/frames_total"
os.makedirs(output_dir, exist_ok=True)

# Copy and rename
for task in copy_plan:
    src = task["src_dir"]
    offset = task["new_start"] - task["start"]
    for i in range(task["start"], task["end"] + 1):
        src_filename = f"frame_{i:06d}.png"
        src_path = os.path.join(src, src_filename)

        new_index = i + offset
        dst_filename = f"{new_index:06d}.png"
        dst_path = os.path.join(output_dir, dst_filename)

        if os.path.exists(src_path):
            shutil.copy2(src_path, dst_path)
        else:
            print(f"⚠️ Missing file: {src_path}")

print("✅ All selected frames copied and reindexed.")
