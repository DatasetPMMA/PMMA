import argparse
import os


def opt():
    parser = argparse.ArgumentParser(description="Video Processing Options")

    # Add your paths here
    parser.add_argument('--input_video_path', type=str, default='videos/input.mp4', help='Path to input video')
    parser.add_argument('--output_video_path', type=str, default='videos/output', help='Directory to save processed videos')
    parser.add_argument('--tmp_dir', type=str, default='./tmp', help='Temporary files directory')
    
    # Add other hyperparameters here
    parser.add_argument('--video_index', type=int, default=1, help='Which video index to process')
    parser.add_argument('--split_right', action='store_true', help='Whether to split right side of the video')

    args = parser.parse_args()
    
    os.makedirs(args.output_video_path, exist_ok=True)
    os.makedirs(args.tmp_dir, exist_ok=True)
    return args



# import ffmpeg


# ## step 1
# def process_video(video_index, input_video_path, video_save_path):
#     ## original video path

#     os.makedirs(video_save_path, exist_ok=True)

#     cap = cv2.VideoCapture(input_video_path)
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     cap.release()
#     if video_index == 1:
#         point_zero = 900
#         start_points = [0]
#         end_points = [9000]
#         for index in range(len(start_points)):
#             output_video = f"{video_save_path}/video1_{index}.mp4"
#             start_frame = point_zero + start_points[index]
#             end_frame = point_zero + end_points[index]
#             start_time = start_frame / fps
#             duration = (end_frame - start_frame) / fps
            
#             print(f'fps: {fps} | start_time: {start_frame} | end_frame: {end_frame}')
            
#             command = ["ffmpeg",
#                     "-ss", str(start_time),   
#                     "-i", input_video_path,       
#                     "-t", str(duration),        
#                     "-c", "copy",          
#                     output_video
#                         ]
#             subprocess.run(command)
#             print(f'Code finished: {index}')            
        
#     elif video_index == 2:
#         point_zero = 2673
#         start_points = [0]
#         end_points = [9000]
#         # start_points = [0, 1800, 7293]
#         # end_points = [381, 6161, 9000]
#         for index in range(len(start_points)):
#             output_video = f"{video_save_path}/video2_{index}.mp4"
#             start_frame = point_zero + start_points[index]
#             end_frame = point_zero + end_points[index]
#             start_time = start_frame / fps
#             duration = (end_frame - start_frame) / fps
            
#             print(f'fps: {fps} | start_time: {start_frame} | end_frame: {end_frame}')


#             command = [
#                 "ffmpeg",
#                 "-ss", str(start_time),
#                 "-i", input_video_path,
#                 "-t", str(duration),
#                 "-c:v", "libx264",
#                 "-preset", "fast",
#                 "-crf", "18",
#                 "-c:a", "copy",
#                 output_video
#             ]
#             # command = ["ffmpeg",
#             #         "-ss", str(start_time),   
#             #         "-i", input_video_path,       
#             #         "-t", str(duration),        
#             #         "-c", "copy",          
#             #         output_video
#             #             ]
#             subprocess.run(command)
#             print(f'Code finished: {index}')
#     elif video_index == 3:
#         point_zero = 1541
#         start_points = [0]
#         end_points = [14637]
#         for index in range(len(start_points)):
#             output_video = f"{video_save_path}/video3_{index}.mp4"
#             start_frame = point_zero + start_points[index]
#             end_frame = point_zero + end_points[index]
#             start_time = 120
#             duration = 1140
            
#             print(f'fps: {fps} | start_time: {start_frame} | end_frame: {end_frame}')
            
#             command = ["ffmpeg",
#                     "-ss", str(start_time),   
#                     "-i", input_video_path,       
#                     "-t", str(duration),        
#                     "-c", "copy",          
#                     output_video
#                         ]
#             subprocess.run(command)
#             print(f'Code finished: {index}')            




# ## step 2
# def split_video_left_right(input_video_path, output_left_path, output_right_path, require_right):
#     # Probe video to get width and height
#     probe = ffmpeg.probe(input_video_path)
#     video_stream = next(s for s in probe['streams'] if s['codec_type'] == 'video')
#     width = int(video_stream['width'])
#     height = int(video_stream['height'])
#     half_width = width // 2

#     # Common encoding args for QuickTime compatibility
#     common_args = [
#         '-c:v', 'libx264',
#         '-crf', '18',                # visually lossless, smaller files
#         '-preset', 'medium',
#         '-profile:v', 'baseline',    # Ensure compatibility with QuickTime
#         '-pix_fmt', 'yuv420p',       # ensures compatibility
#         '-c:a', 'aac',               # AAC audio for .mp4 compatibility
#         '-movflags', '+faststart'    # allows faster playback startup
#     ]

#     # Left half
#     cmd_left = [
#         'ffmpeg',
#         '-i', input_video_path,
#         '-filter:v', f'crop={half_width}:{height}:0:0',
#         *common_args,
#         output_left_path
#     ]

#     # Right half
#     cmd_right = [
#         'ffmpeg',
#         '-i', input_video_path,
#         '-filter:v', f'crop={half_width}:{height}:{half_width}:0',
#         *common_args,
#         output_right_path
#     ]

#     subprocess.run(cmd_left, check=True)
    
#     # Generate right video or not
#     if require_right:
#         subprocess.run(cmd_right, check=True)




