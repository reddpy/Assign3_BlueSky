"""Implementation of automated moderator"""

from typing import List
from atproto import Client
from .label import post_from_url
from .llm_call import get_llm_response, encode_images
import pandas as pd
import os
import re
import requests
from PIL import Image
import io

LABEL = 'Potentially Inappropriate'

class AutomatedLabeler:
    """Automated labeler implementation"""

    def __init__(self, client: Client, input_dir):
        self.client = client
        
        ## T&S Labels
        posts_path = os.path.join(input_dir, 'bluesky_data/posts.csv')

        self.urls = pd.read_csv(posts_path)['post_url'].tolist()

    def moderate_post(self, url: str) -> List[str]:
        """
        Apply moderation to the post specified by the given url
        """

        labels = set()

        post = post_from_url(self.client, url)
        post_text = post.value.text
        images = self.get_post_media(url)
        if images:
            encode_images(images)
        else:
            pass


        return list(labels) if labels is not set() else []

    def get_post_media(self, url: str):
        images = []
        url_parts = url.split('/')
        author = url_parts[-3]
        post_id = url_parts[-1]
        
        post = self.client.app.bsky.feed.get_post_thread(
            {'uri': f'at://{author}/app.bsky.feed.post/{post_id}'}
        )

        if hasattr(post.thread.post.embed, 'images'):
            img_embeds = getattr(post.thread.post.embed, 'images', [])

            for img in img_embeds:
                image_url = img.fullsize
                response = requests.get(image_url)
                image_data = Image.open(io.BytesIO(response.content)).convert('RGB')
                images.append(image_data)

            return images
        
        elif hasattr(post.thread.post.embed, 'playlist'):
            video_url = getattr(post.thread.post.embed, 'playlist', [])

            
