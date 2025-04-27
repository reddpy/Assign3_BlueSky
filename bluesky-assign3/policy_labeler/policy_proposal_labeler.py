"""Implementation of political content labeler"""

import os
import re
import sys
from typing import List

from atproto import Client

from urllib.parse import urlparse

THRESH = 0.3

POST_SENTIMENT_SCORING = {
    "very negative": -2,
    "negative": -1,
    "neutral": 0,
    "positive": 1,
    "very positive": 2,
}

FIGURE_DIR_PATH = "./figure_data_lists"
NEWS_DIR_PATH = "./news_url_data_lists"


def post_from_url(client: Client, url: str):
    """
    Retrieve a Bluesky post from its URL
    """
    parts = url.split("/")
    rkey = parts[-1]
    handle = parts[-3]
    return client.get_post(rkey, handle)


def load_political_figures():
    # Get all entries in the directory
    files = list()
    political_figures = list()
    for filename in os.listdir(FIGURE_DIR_PATH):
        file_path = os.path.join(FIGURE_DIR_PATH, filename)

        # Check if the entry is a file (not a subdirectory)
        if os.path.isfile(file_path):
            files.append(file_path)

    for file in files:
        with open(file, "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                political_figures.append(line)

    return political_figures


def load_political_URLS():
    # Get all entries in the directory
    files = list()
    political_urls = list()
    for filename in os.listdir(NEWS_DIR_PATH):
        file_path = os.path.join(NEWS_DIR_PATH, filename)

        # Check if the entry is a file (not a subdirectory)
        if os.path.isfile(file_path):
            files.append(file_path)

    for file in files:
        with open(file, "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                political_urls.append(line)

    return political_urls


class AutomatedLabeler:
    """Automated labeler for political content"""

    def __init__(self, client, input_dir):
        self.client = client
        self.political_domains = load_political_URLS()
        self.political_figures = load_political_figures()

    def extract_domains(self, url):
        """Extract domain and path from a URL"""
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            path = parsed_url.path
            return domain + path
        except:
            return url  # Return the original URL if parsing fails

    def extract_urls_from_post(
        self, post_response
    ):  # Renamed 'post' to 'post_response' for clarity
        """
        Extract URLs from a Bluesky post's response object.

        Args:
            post_response: The response object returned by client.get_post()

        Returns:
            list: List of URLs found in the post
        """
        urls = []

        # Check if the response object has a 'value' attribute (the record)
        # and if that value has 'facets'
        if (
            post_response
            and hasattr(post_response, "value")
            and post_response.value
            and hasattr(post_response.value, "facets")
            and post_response.value.facets
        ):
            # Access facets through post_response.value
            for facet in post_response.value.facets:
                # Check if facet itself has features (structure might vary slightly by type)
                if hasattr(facet, "features"):
                    for feature in facet.features:
                        # Check if the feature is a link and has a URI
                        # Using getattr for safety, checking $type might be more robust if available
                        if (
                            hasattr(feature, "uri")
                            and getattr(feature, "py_type", None)
                            == "app.bsky.richtext.facet#link"
                        ):
                            urls.append(feature.uri)
        else:
            # Optional: Log if facets are missing or structure is unexpected
            # print(f"No facets found or unexpected structure in post response: {post_response}")
            pass

        return urls

    def check_post_for_urls(self, post_obj):
        urls = self.extract_urls_from_post(post_obj)
        return urls

    def url_is_political(self, url, post):
        """Check if URL is from a political domain"""
        domain_with_path = self.extract_domains(url)

        political_domain = False

        for political_domain in self.political_domains:
            if political_domain in domain_with_path:
                political_domain = True
            
        article_title_tokens = str(post.value.embed.external.title).split(" ")
        print(article_title_tokens)
        

        return False

    def moderate_post(self, url: str) -> List[str]:
        """
        Apply moderation to identify political content in the post
        specified by the given url
        """
        # Get the post
        post = post_from_url(self.client, url)

        # Extract URLs
        post_urls = self.extract_urls_from_post(post)

        # Check each URL
        political_urls = []
        for url in post_urls:
            is_political = self.url_is_political(url=url, post=post)

            print("URL:", url)
            print("Political:", is_political)
            print("ARTICLE TITLE:", post.value.embed.external.title)
            if is_political:
                political_urls.append(url)

        # Return label if political
        if political_urls:
            return ["political"]

        return []
