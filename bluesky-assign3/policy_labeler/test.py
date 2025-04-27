"""Test script for the political content labeler"""


import os
import sys
from atproto import Client
from dotenv import load_dotenv
from policy_proposal_labeler import AutomatedLabeler

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
     sys.path.insert(0, parent_dir) # Insert at beginning for higher priority


# Load environment variables
load_dotenv(override=True)
USERNAME = os.getenv("USERNAME")
PW = os.getenv("PW")

def main():
    # Initialize the client and login
    client = Client()
    client.login(USERNAME, PW)
    
    # Initialize the labeler
    labeler = AutomatedLabeler(client, input_dir="./")
    
    # Test post URL - replace with a real Bluesky post URL
    test_url = "https://bsky.app/profile/just-jack-1.bsky.social/post/3lnnge7lssc2y"
    
    # Test the labeler
    print(f"Testing post: {test_url}")
    labels = labeler.moderate_post(test_url)
    
    if labels:
        print(f"Post labeled as: {', '.join(labels)}")
    else:
        print("Post not flagged for any labels")

if __name__ == "__main__":
    main()