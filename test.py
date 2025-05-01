import m3u8
from urllib.parse import urljoin

def get_video_duration(playlist_url):
    playlist = m3u8.load(playlist_url)
    
    if playlist.is_variant:
        playlist_uri = sorted(playlist.playlists, key=lambda x: x.stream_info.bandwidth, reverse=True)[0].uri
        
        if not playlist_uri.startswith('http'):
            base_url = '/'.join(playlist_url.split('/')[:-1]) + '/'
            playlist_uri = urljoin(base_url, playlist_uri)
        
        return get_video_duration(playlist_uri)
    
    return sum(segment.duration for segment in playlist.segments)


def main():
        
    print("Downloading video from m3u8 playlist...")
    video_path = get_video_duration("https://video.bsky.app/watch/did%3Aplc%3Adoc4xcitwuwfkl4lb2fq4udp/bafkreicgex5ubffnhnbl3nbwneqefvqojl7nk6nl7xcykxouvik3wlbfmy/playlist.m3u8")
    
    print(f"Video downloaded to: {video_path}")
        

if __name__ == "__main__":
    main()