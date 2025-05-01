import os
import sys
import subprocess
from pathlib import Path
import json

FFMPEG_PATH = r'C:\Users\harry\Downloads\tns\Assign3_BlueSky\.venv\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe'

def extract_frames(video_url, video_duration, output_dir="./test", num_frames=5):
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Extracting {num_frames} frames from {video_url}")
    
    frames = []
    
    for i in range(1, num_frames + 1):
        timestamp = video_duration * i / (num_frames + 1)
        output_file = os.path.join(output_dir, f"frame_{i}_{timestamp:.2f}s.jpg")
        
        cmd = [
            FFMPEG_PATH,
            '-y',  
            '-ss', str(timestamp),  
            '-i', video_url,  
            '-frames:v', '1',  
            '-q:v', '31',  
            output_file
        ]
        
        # Execute the command
        result = subprocess.run(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        
        frames.append(output_file)
            
    
    return frames

def main():
    # Bluesky video URL - direct m3u8 playlist
    video_url = "https://video.bsky.app/watch/did%3Aplc%3Adoc4xcitwuwfkl4lb2fq4udp/bafkreicgex5ubffnhnbl3nbwneqefvqojl7nk6nl7xcykxouvik3wlbfmy/playlist.m3u8"
    output_dir = "./test"
    
    # Extract frames
    frames = extract_frames(video_url, output_dir, 5)
    print(frames)
    


if __name__ == "__main__":
    main()