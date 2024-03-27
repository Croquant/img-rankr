import hashlib

import requests


def calculate_md5_hash(file_url):
    try:
        response = requests.get(file_url)
        if response.status_code != 200:
            raise Exception(f"Error downloading file from {file_url}")

        return hashlib.md5(response.content).hexdigest()

    except Exception as e:
        raise Exception(f"Error calculating MD5 hash: {e}")
