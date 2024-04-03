import hashlib
from io import BytesIO

import dhash
import requests
from PIL import Image


def calculate_md5_hash(file_url):
    try:
        response = requests.get(file_url)
        if response.status_code != 200:
            raise Exception(f"Error downloading file from {file_url}")

        return hashlib.md5(response.content).hexdigest()

    except Exception as e:
        raise Exception(f"Error calculating MD5 hash: {e}")


def calculate_dhash(file_url):
    try:
        response = requests.get(file_url)
        if response.status_code != 200:
            raise Exception(f"Error downloading file from {file_url}")

        image = Image.open(BytesIO(response.content)).convert("L")
        row, col = dhash.dhash_row_col(image)
        return dhash.format_hex(row, col)

    except Exception as e:
        raise Exception(f"Error calculating MD5 hash: {e}")
