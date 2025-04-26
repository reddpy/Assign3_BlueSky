st = "The Integrity Institute's latest research on algorithmic amplification of harmful content is a must-read for anyone working in this space. Their evidence-based approach is exactly what the field needs: https://integrityinstitute.org/"

# print(st.lower().split())

from dotenv import load_dotenv
import argparse
import json
import os
from atproto import Client

import pandas as pd

from pylabel import AutomatedLabeler, label_post, did_from_handle

load_dotenv(override=True)
USERNAME = os.getenv("USERNAME")
PW = os.getenv("PW")

def main():
    """
    Main function for the test script
    """
    client = Client()
    labeler_client = None
    client.login(USERNAME, PW)
    did = did_from_handle(USERNAME)

    url = "https://bsky.app/profile/labeler-test.bsky.social/post/3lktfpq6gti24"

    parts = url.split("/")
    rkey = parts[-1]
    handle = parts[-3]
    post = client.get_post(rkey, handle)
    post_text = post.value.text

    print(type(post_text))


if __name__ == '__main__':
    # main()
    df = pd.read_csv(r'./labeler-inputs/news-domains.csv')
    print(df)
    print(df.values.tolist())