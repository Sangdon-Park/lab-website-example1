#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urljoin, urlparse

def get_page_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,ko;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching page: {e}")
        return None

def download_image(url, filename):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Referer': 'https://sites.google.com/',
    }
    
    try:
        response = requests.get(url, headers=headers, stream=True, timeout=30)
        response.raise_for_status()
        
        # Check if content is actually an image
        content_type = response.headers.get('content-type', '')
        if 'image' not in content_type and 'octet-stream' not in content_type:
            print(f"Warning: Content type is {content_type}, might not be an image")
        
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        file_size = os.path.getsize(filename)
        if file_size > 1000:  # At least 1KB
            print(f"Downloaded: {filename} ({file_size} bytes)")
            return True
        else:
            os.remove(filename)
            print(f"Skipped small file: {url}")
            return False
            
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def extract_images():
    url = "https://sites.google.com/view/climatesystem/"
    
    print(f"Fetching content from {url}...")
    html_content = get_page_content(url)
    
    if not html_content:
        print("Failed to fetch page content")
        return
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Create images directory
    os.makedirs('images', exist_ok=True)
    
    downloaded_count = 0
    
    # Find all img tags
    images = soup.find_all('img')
    print(f"Found {len(images)} img tags")
    
    for i, img in enumerate(images):
        src = img.get('src')
        if not src:
            continue
        
        # Skip data URLs and very small images
        if src.startswith('data:') or 'spacer.gif' in src or '1x1' in src:
            continue
        
        # Convert relative URLs to absolute
        if src.startswith('//'):
            src = 'https:' + src
        elif src.startswith('/'):
            src = urljoin(url, src)
        
        print(f"Image {i+1}: {src}")
        
        # Generate filename
        parsed = urlparse(src)
        if parsed.path:
            filename = os.path.basename(parsed.path)
            if not filename or '.' not in filename:
                filename = f"image_{i+1}.jpg"
        else:
            filename = f"image_{i+1}.jpg"
        
        # Clean filename
        filename = re.sub(r'[^\w\-_\.]', '_', filename)
        if not any(filename.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
            filename += '.jpg'
        
        filepath = os.path.join('images', filename)
        
        if download_image(src, filepath):
            downloaded_count += 1
    
    # Look for background images in style attributes
    print("\nLooking for background images in CSS...")
    elements_with_style = soup.find_all(attrs={"style": True})
    
    for element in elements_with_style:
        style = element.get('style', '')
        # Look for background-image URLs
        matches = re.findall(r'background-image:\s*url\(["\']?([^"\')]+)["\']?\)', style)
        for match in matches:
            bg_url = match
            if bg_url.startswith('//'):
                bg_url = 'https:' + bg_url
            elif bg_url.startswith('/'):
                bg_url = urljoin(url, bg_url)
            
            print(f"Background image: {bg_url}")
            filename = f"background_{downloaded_count + 1}.jpg"
            filepath = os.path.join('images', filename)
            
            if download_image(bg_url, filepath):
                downloaded_count += 1
    
    # Also check for embedded content
    print("\nLooking for embedded content...")
    iframes = soup.find_all('iframe')
    for iframe in iframes:
        src = iframe.get('src')
        if src:
            print(f"Iframe found: {src}")
    
    print(f"\nTotal downloaded: {downloaded_count} images")

if __name__ == "__main__":
    extract_images()