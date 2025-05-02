"""Implementation of automated moderator"""

from typing import List
from atproto import Client
from .label import post_from_url
from .llm_call import get_llm_response
from .video_functions import get_video_duration, extract_frames
import pandas as pd
import os
import requests

LABEL = 'Potentially Inappropriate'

class PolicyLabeler:
    """Automated labeler implementation"""

    def __init__(self, client: Client, input_dir):
        self.client = client
        
        ## T&S Labels
        posts_path = os.path.join(input_dir, 'bluesky_data/posts.csv')

        self.urls = pd.read_csv(posts_path)['post_url'].tolist()

    def moderate_post(self, url: str) -> List[str]:

        labels = set()

        post = post_from_url(self.client, url)
        post_text = post.value.text
        images = self.get_post_media(url)

        response = get_llm_response(post_text)

        if response == '1':
            labels.add(LABEL)

        if os.path.exists('./temp') and os.listdir('./temp'):
            for item in os.listdir('./temp'):
                item_path = os.path.join('./temp', item)
                if os.path.isfile(item_path):
                    os.remove(item_path)

        return list(labels) if labels is not set() else []

    def get_post_media(self, url: str):
        images = []
        url_parts = url.split('/')
        author = url_parts[-3]
        post_id = url_parts[-1]
        
        post = self.client.app.bsky.feed.get_post_thread(
            {'uri': f'at://{author}/app.bsky.feed.post/{post_id}'}
        )
        os.makedirs('./temp', exist_ok=True)

        if hasattr(post.thread.post.embed, 'images'):
            img_embeds = getattr(post.thread.post.embed, 'images', [])

            for i, img in enumerate(img_embeds):
                image_url = img.fullsize
                response = requests.get(image_url)
                
                filename = f'./temp/image_{i}.jpg'
                with open(filename, 'wb') as f:
                        f.write(response.content)

        
        elif hasattr(post.thread.post.embed, 'playlist'):
            video_url = getattr(post.thread.post.embed, 'playlist', [])
            video_duration = get_video_duration(video_url)
            frames = extract_frames(video_url, video_duration)

            return frames
        
        return []

if __name__ == '__main__':
    from atproto import Client
    from dotenv import load_dotenv

    

    load_dotenv(override=True)
    USERNAME = os.getenv("USERNAME")
    PW = os.getenv("PW")
    client = Client()
    labeler_client = None
    client.login(USERNAME, PW)

    labeler = PolicyLabeler(client, '.')

    url, expected_labels = 'https://bsky.app/profile/gothiccmoms.bsky.social/post/3lnm7oq4bqs2x', 'Pot'
    # url, expected_labels = 'https://bsky.app/profile/sweetladykitsune.bsky.social/post/3lnqquj5fts2h', 'Pot'
    labels = labeler.moderate_post(url)
    print(f"For {url}, labeler produced {labels}, expected {expected_labels}")
    



