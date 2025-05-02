import os
import subprocess
import sys
from pathlib import Path

def extract_frames_direct(video_url, output_dir="./frames", num_frames=5):
    """Extract frames directly from the video URL using FFmpeg"""
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Extracting {num_frames} frames directly from {video_url}")
    print(f"Frames will be saved to {output_dir}")
    
    # We'll use fixed timestamps instead of trying to determine video duration
    # Based on your output, the video is about 1.67 seconds long
    duration = 1.67  # seconds
    
    frames = []
    
    # Extract frames at evenly spaced intervals
    for i in range(1, num_frames + 1):
        # Calculate timestamp as a fraction of the duration
        timestamp = duration * i / (num_frames + 1)
        output_file = os.path.join(output_dir, f"direct_frame_{i}_{timestamp:.2f}s.jpg")
        
        print(f"Extracting frame {i}/{num_frames} at {timestamp:.2f}s...")
        
        try:
            # Build the FFmpeg command
            cmd = [
                'ffmpeg',
                '-y',  # Overwrite output files without asking
                '-ss', str(timestamp),  # Seek to this position
                '-i', video_url,  # Input file
                '-frames:v', '1',  # Extract only one frame
                '-q:v', '1',  # Highest quality
                output_file
            ]
            
            # Execute the command
            result = subprocess.run(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Check if the file was created
            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                frames.append({
                    'frame_number': i,
                    'timestamp': timestamp,
                    'path': output_file
                })
                print(f"Successfully extracted frame {i}")
            else:
                print(f"Failed to extract frame {i} - Output file is empty or missing")
                print(f"FFmpeg stderr: {result.stderr}")
            
        except Exception as e:
            print(f"Error extracting frame {i}: {str(e)}")
    
    return frames

def main():
    # Check if FFmpeg is available
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("FFmpeg is available")
    except FileNotFoundError:
        print("FFmpeg is not installed or not in PATH")
        print("Please install FFmpeg or add it to your PATH")
        sys.exit(1)
    
    # Bluesky video URL - direct m3u8 playlist
    video_url = "https://video.bsky.app/watch/did%3Aplc%3Adoc4xcitwuwfkl4lb2fq4udp/bafkreicgex5ubffnhnbl3nbwneqefvqojl7nk6nl7xcykxouvik3wlbfmy/playlist.m3u8"
    output_dir = "./test"
    
    # Extract frames
    frames = extract_frames_direct(video_url, output_dir, 5)
    
    # Print results
    if frames:
        print("\nSuccessfully extracted frames:")
        for frame in frames:
            print(f"Frame {frame['frame_number']}: {frame['timestamp']:.2f}s - {frame['path']}")
        print(f"\nTotal frames extracted: {len(frames)}")
    else:
        print("Failed to extract any frames.")

if __name__ == "__main__":
    main()