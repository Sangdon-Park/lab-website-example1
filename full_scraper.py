#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import os
import re
import time
from urllib.parse import urljoin, urlparse, unquote

def get_page_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,ko;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://sites.google.com/',
    }
    
    try:
        print(f"Fetching: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
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
        
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        file_size = os.path.getsize(filename)
        if file_size > 1000:  # At least 1KB
            print(f"✓ Downloaded: {filename} ({file_size} bytes)")
            return True
        else:
            os.remove(filename)
            print(f"✗ Skipped small file: {url}")
            return False
            
    except Exception as e:
        print(f"✗ Failed to download {url}: {e}")
        return False

def extract_images_from_page(url, page_name):
    print(f"\n=== Processing {page_name} ===")
    html_content = get_page_content(url)
    
    if not html_content:
        print(f"Failed to fetch content from {url}")
        return []
    
    soup = BeautifulSoup(html_content, 'html.parser')
    downloaded_images = []
    
    # Find all img tags
    images = soup.find_all('img')
    print(f"Found {len(images)} img tags in {page_name}")
    
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
        
        print(f"  Image {i+1}: {src}")
        
        # Generate filename
        parsed = urlparse(src)
        if parsed.path:
            filename = os.path.basename(unquote(parsed.path))
            if not filename or '.' not in filename:
                filename = f"{page_name}_image_{i+1}.jpg"
        else:
            filename = f"{page_name}_image_{i+1}.jpg"
        
        # Clean filename
        filename = re.sub(r'[^\w\-_\.]', '_', filename)
        if not any(filename.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
            filename += '.jpg'
        
        # Add page prefix to avoid conflicts
        filename = f"{page_name}_{filename}"
        filepath = os.path.join('images', filename)
        
        if download_image(src, filepath):
            downloaded_images.append(filename)
    
    # Look for background images in style attributes
    print(f"Looking for background images in {page_name}...")
    elements_with_style = soup.find_all(attrs={"style": True})
    
    for element in elements_with_style:
        style = element.get('style', '')
        matches = re.findall(r'background-image:\s*url\(["\']?([^"\')]+)["\']?\)', style)
        for match in matches:
            bg_url = match
            if bg_url.startswith('//'):
                bg_url = 'https:' + bg_url
            elif bg_url.startswith('/'):
                bg_url = urljoin(url, bg_url)
            
            print(f"  Background image: {bg_url}")
            filename = f"{page_name}_background_{len(downloaded_images) + 1}.jpg"
            filepath = os.path.join('images', filename)
            
            if download_image(bg_url, filepath):
                downloaded_images.append(filename)
    
    # Look for embedded Google Drive files
    print(f"Looking for Google Drive content in {page_name}...")
    drive_links = soup.find_all('a', href=re.compile(r'drive\.google\.com'))
    for link in drive_links:
        href = link.get('href')
        print(f"  Google Drive link: {href}")
        # Try to extract thumbnail
        if 'id=' in href:
            file_id = re.search(r'id=([a-zA-Z0-9_-]+)', href)
            if file_id:
                thumbnail_url = f"https://drive.google.com/thumbnail?id={file_id.group(1)}&sz=w800"
                filename = f"{page_name}_drive_{file_id.group(1)}.jpg"
                filepath = os.path.join('images', filename)
                if download_image(thumbnail_url, filepath):
                    downloaded_images.append(filename)
    
    return downloaded_images

def scrape_all_pages():
    # All the Google Sites pages we need to scrape
    pages = {
        'home': 'https://sites.google.com/view/climatesystem/',
        'research': 'https://sites.google.com/view/climatesystem/research',
        'pi_profile': 'https://sites.google.com/view/climatesystem/pi-prof-j-s-kim/prof-jin-soo-kim',
        'pi_insights': 'https://sites.google.com/view/climatesystem/pi-prof-j-s-kim/personal-insights',
        'members': 'https://sites.google.com/view/climatesystem/members/members',
        'alumni': 'https://sites.google.com/view/climatesystem/members/alumni',
        'publications': 'https://sites.google.com/view/climatesystem/publications',
        'news': 'https://sites.google.com/view/climatesystem/news/news',
        'news_before': 'https://sites.google.com/view/climatesystem/news/before',
    }
    
    # Create images directory
    os.makedirs('images', exist_ok=True)
    
    all_downloaded_images = []
    
    for page_name, url in pages.items():
        try:
            downloaded = extract_images_from_page(url, page_name)
            all_downloaded_images.extend(downloaded)
            time.sleep(2)  # Be polite to the server
        except Exception as e:
            print(f"Error processing {page_name}: {e}")
            continue
    
    print(f"\n=== SUMMARY ===")
    print(f"Total images downloaded: {len(all_downloaded_images)}")
    for img in all_downloaded_images:
        print(f"  - {img}")
    
    print(f"\nFiles in images directory:")
    try:
        for file in os.listdir('images'):
            filepath = os.path.join('images', file)
            size = os.path.getsize(filepath)
            print(f"  {file} ({size} bytes)")
    except Exception as e:
        print(f"Error listing files: {e}")

if __name__ == "__main__":
    print("Starting complete image scraping from Google Sites...")
    scrape_all_pages()
    print("\nScraping completed!")