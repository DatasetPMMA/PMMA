import cv2
import os
import subprocess

def cut_video_by_frame(input_path, output_path, start_frame, num_frames):
    """
    Cuts a video starting from a specific frame and saves a given number of frames.

    Parameters:
    - input_path (str): Path to the input video file.
    - output_path (str): Path to save the output video file.
    - start_frame (int): Frame index to start cutting from.
    - num_frames (int): Number of frames to extract.
    """
    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        raise IOError("Cannot open video file: " + input_path)

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)  # KEEP AS FLOAT
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f'Cut video by frame fps: {fps}')

    # Check if the requested range is valid
    if start_frame >= total_frames:
        raise ValueError("Start frame is beyond the total number of frames in the video.")
    if start_frame + num_frames > total_frames:
        num_frames = total_frames - start_frame  # Adjust to max available

    # Set video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Go to the start frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    # Extract and write frames
    count = 0
    while count < num_frames:
        ret, frame = cap.read()
        if not ret:
            print(f"Stopped early at frame {start_frame + count}")
            break
        out.write(frame)
        count += 1

    cap.release()
    out.release()
    print(f"Saved {count} frames starting from frame {start_frame} to '{output_path}'.")


def split_video_left_right(input_path, left_output_path, right_output_path,right_flag):
    """
    Splits a video into two sub-videos: left and right halves (spatially), frame by frame.

    Parameters:
    - input_path (str): Path to the input video.
    - left_output_path (str): Path to save the left half video.
    - right_output_path (str): Path to save the right half video.
    """
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise IOError("Cannot open video file: " + input_path)

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    print(f'Split video left and right fps: {fps}')
    # Half width for left/right
    half_width = width // 2

    # Create video writers for left and right videos
    left_writer = cv2.VideoWriter(left_output_path, fourcc, fps, (half_width, height))
    right_writer = cv2.VideoWriter(right_output_path, fourcc, fps, (half_width, height))

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Split the frame
        left_half = frame[:, :half_width]
        right_half = frame[:, half_width:]

        # Write each half to its respective video
        left_writer.write(left_half)
        if right_flag:
            right_writer.write(right_half)

        frame_idx += 1

    cap.release()
    left_writer.release()
    if right_flag:
        right_writer.release()

    print(f"Video split complete: {frame_idx} frames written to each output.")


def video_to_images(video_path, output_dir, prefix='frame'):
    """
    Extracts all frames from a video and saves them as individual image files.

    Parameters:
    - video_path (str): Path to the input video.
    - output_dir (str): Directory where images will be saved.
    - prefix (str): Prefix for saved image filenames (default: 'frame').
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError("Cannot open video file: " + video_path)

    os.makedirs(output_dir, exist_ok=True)

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Construct image file name
        filename = os.path.join(output_dir, f"{prefix}_{frame_idx:05d}.png")
        cv2.imwrite(filename, frame)
        frame_idx += 1

    cap.release()
    print(f"Saved {frame_idx} frames to '{output_dir}'.")


def split_video_ffmpeg(input_path, left_output, right_output):
    cmd = [
        "ffmpeg", "-i", input_path,
        "-filter_complex",
        "[0:v]crop=iw/2:ih:0:0[left];[0:v]crop=iw/2:ih:iw/2:0[right]",
        "-map", "[left]", left_output,
        "-map", "[right]", right_output
    ]
    subprocess.run(cmd)
    

# Video 1
video_index = 1

## Input
video_path = f'./raw_data/original_videos/2025-04-04-mobility-aids{video_index}.mp4'
cut_video_by_frame(video_path, f'output_{video_index}.mp4', 900, 9000)
split_video_left_right(f'output_{video_index}.mp4', f'left_half_{video_index}.mp4', f'right_half_{video_index}.mp4', False)
video_to_images(f'left_half_{video_index}.mp4', f'./raw_data/frames_video_{video_index}_left')


# Video 3
video_index = 3
## Input
video_path = f'../raw_data/original_videos/2025-04-04-mobility-aids{video_index}.mp4'
cut_video_by_frame(video_path, f'output_{video_index}.mp4', 1541, 14637)
split_video_left_right(f'output_{video_index}.mp4', f'left_half_{video_index}.mp4', f'right_half_{video_index}.mp4', False)
video_to_images(f'left_half_{video_index}.mp4', f'./raw_data/frames_video_{video_index}_left')
