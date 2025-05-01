import os
import subprocess
import m3u8
from urllib.parse import urljoin
from PIL import Image

FFMPEG_PATH = r'C:\Users\harry\Downloads\tns\Assign3_BlueSky\.venv\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe'

def get_video_duration(playlist_url):
    playlist = m3u8.load(playlist_url)
    
    if playlist.is_variant:
        playlist_uri = sorted(playlist.playlists, key=lambda x: x.stream_info.bandwidth, reverse=True)[0].uri
        
        if not playlist_uri.startswith('http'):
            base_url = '/'.join(playlist_url.split('/')[:-1]) + '/'
            playlist_uri = urljoin(base_url, playlist_uri)
        
        return get_video_duration(playlist_uri)
    
    return sum(segment.duration for segment in playlist.segments)

def extract_frames(video_url, video_duration, output_dir="./emp", num_frames=5):
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

        result = subprocess.run(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )

        image_data = Image.open(output_file).convert('RGB')
        frames.append(image_data)
            
    return frames

def main():
    video_url = "https://video.bsky.app/watch/did%3Aplc%3Adoc4xcitwuwfkl4lb2fq4udp/bafkreicgex5ubffnhnbl3nbwneqefvqojl7nk6nl7xcykxouvik3wlbfmy/playlist.m3u8"
    output_dir = "./test"
    
    frames = extract_frames(video_url, output_dir, 5)
    print(frames)

    print("Downloading video from m3u8 playlist...")
    video_path = get_video_duration("https://video.bsky.app/watch/did%3Aplc%3Adoc4xcitwuwfkl4lb2fq4udp/bafkreicgex5ubffnhnbl3nbwneqefvqojl7nk6nl7xcykxouvik3wlbfmy/playlist.m3u8")
    
    print(f"Video downloaded to: {video_path}")
        

if __name__ == "__main__":
    main()