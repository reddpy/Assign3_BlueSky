"""Implementation of automated moderator"""

from typing import List
from atproto import Client
from .label import post_from_url
import pandas as pd
import os
import re
import requests
from PIL import Image
import io
from perception.hashers import PHash

T_AND_S_LABEL = "t-and-s"
DOG_LABEL = "dog"
THRESH = 0.3

def check_keyword(keyword, post):

        pattern = re.compile(r'\b' + keyword + r'\b', re.IGNORECASE)

        found = pattern.search(post)

        return found is not None

class AutomatedLabeler:
    """Automated labeler implementation"""

    def __init__(self, client: Client, input_dir):
        self.client = client
        self.hasher = PHash()
        
        ## T&S Labels
        ts_domain_path = os.path.join(input_dir, 't-and-s-domains.csv')
        ts_word_path = os.path.join(input_dir, 't-and-s-words.csv')

        domains = pd.read_csv(ts_domain_path)['Domain'].tolist()
        words = pd.read_csv(ts_word_path)['Word'].tolist()

        self.ts = domains + words   

        ## Sources 
        news_domain_path = os.path.join(input_dir, 'news-domains.csv')

        self.news = pd.read_csv(news_domain_path).values.tolist()

        ## Dogs
        dog_dir_path = os.path.join(input_dir, 'dog-list-images')
   
        self.dogs = self.dog_dir_hashes(dog_dir_path)

    def moderate_post(self, url: str) -> List[str]:
        """
        Apply moderation to the post specified by the given url
        """

        labels = set()

        post = post_from_url(self.client, url)
        post_text = post.value.text
        images = self.get_post_images(url)

        for keyword in self.ts:
            if check_keyword(keyword, post_text):
                labels.add(T_AND_S_LABEL)

        for keyword, source in self.news:
            if check_keyword(keyword, post_text):
                labels.add(source)

        for image in images:
            if self.compare_against_dog_dir(image):
                labels.add(DOG_LABEL)

        return list(labels) if labels is not set() else []

    def get_post_images(self, url: str):
        images = []
        url_parts = url.split('/')
        author = url_parts[-3]
        post_id = url_parts[-1]
        
        post = self.client.app.bsky.feed.get_post_thread(
            {'uri': f'at://{author}/app.bsky.feed.post/{post_id}'}
        )

        img_embeds = getattr(post.thread.post.embed, 'images', [])

        for img in img_embeds:
            image_url = img.fullsize
            response = requests.get(image_url)
            image_data = Image.open(io.BytesIO(response.content)).convert('RGB')
            images.append(image_data)

        return images
    
    def dog_dir_hashes(self, directory):
        result = []
        for fname in os.listdir(directory):
            path = os.path.join(directory, fname)
            image = Image.open(path).convert('RGB')
            result.append(self.calculate_hashing(image))

        return result

    def compare_against_dog_dir(self, image):
        base = self.calculate_hashing(image)
        for hashes in self.dogs:
            hamming_distance = self.hasher.compute_distance(base, hashes)
            if hamming_distance <= THRESH:
                return True
        return False
    
    def calculate_hashing(self, image):
        return self.hasher.compute(image)

    