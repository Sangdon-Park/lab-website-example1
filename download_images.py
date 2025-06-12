#!/usr/bin/env python3
import requests
import os
from urllib.parse import urlparse

def download_image(url, filename):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,ko;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'image',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site',
        'Referer': 'https://sites.google.com/',
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    try:
        response = session.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        # Check if content is actually an image
        content_type = response.headers.get('content-type', '')
        if not content_type.startswith('image/'):
            print(f"Warning: Content type is {content_type}, not an image")
        
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Successfully downloaded: {filename}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return False

# Images to download
images = {
    'main-background.jpg': 'https://lh6.googleusercontent.com/GS4srxDt-dAkG3zSQ8BKnJ-jeJDGaNPhriFN7upox9uirN8MnNDE9R3Nx0M4rEQbbktJfqdSuDGXR6QN4kk0XW4e1i2srYKsVO5H7cEN_W5zdK51sGwkiUnBW6Ox3A76P9VF2HHYS0OgZApWygawfsotdukrdLSZl6vq2NuSG5X6uCqZClNL-w=w1280',
}

# Create images directory if it doesn't exist
os.makedirs('images', exist_ok=True)

# Download images
for filename, url in images.items():
    filepath = os.path.join('images', filename)
    download_image(url, filepath)