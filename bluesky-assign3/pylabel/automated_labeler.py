"""Implementation of automated moderator"""

from typing import List
from atproto import Client
from .label import post_from_url
import pandas as pd
import os
import re

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
        
        ## T&S Labels
        ts_domain_path = os.path.join(input_dir, 't-and-s-domains.csv')
        ts_word_path = os.path.join(input_dir, 't-and-s-words.csv')

        domains = pd.read_csv(ts_domain_path)['Domain'].tolist()
        words = pd.read_csv(ts_word_path)['Word'].tolist()

        self.ts = domains + words   

        ## Sources 
        news_domain_path = os.path.join(input_dir, 'news-domains.csv')

        self.news = pd.read_csv(news_domain_path).values.tolist()
   
    def moderate_post(self, url: str) -> List[str]:
        """
        Apply moderation to the post specified by the given url
        """

        labels = set()

        post = post_from_url(self.client, url)
        post_text = post.value.text

        for keyword in self.ts:
            if check_keyword(keyword, post_text):
                labels.add(T_AND_S_LABEL)

        for keyword, source in self.news:
             if check_keyword(keyword, post_text):
                  labels.add(source)


        return list(labels) if labels is not set() else []


    