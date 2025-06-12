#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import time
import re
from urllib.parse import urlparse, urljoin

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--user-data-dir=/tmp/chrome_profile")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
    chrome_options.binary_location = "/snap/bin/chromium"
    
    try:
        from selenium.webdriver.chrome.service import Service
        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        print(f"Error setting up Chrome driver: {e}")
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
        
        print(f"Downloaded: {filename}")
        return True
        
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def scrape_google_site():
    url = "https://sites.google.com/view/climatesystem/"
    driver = setup_driver()
    
    if not driver:
        print("Failed to set up browser driver")
        return
    
    try:
        print(f"Loading {url}...")
        driver.get(url)
        
        # Wait for page to load
        time.sleep(5)
        
        # Find all images on the page
        images = driver.find_elements(By.TAG_NAME, "img")
        
        print(f"Found {len(images)} images")
        
        os.makedirs('images', exist_ok=True)
        
        downloaded_count = 0
        
        for i, img in enumerate(images):
            try:
                src = img.get_attribute('src')
                if not src:
                    continue
                    
                # Skip small icons and placeholders
                width = img.get_attribute('width') or img.size.get('width', 0)
                height = img.get_attribute('height') or img.size.get('height', 0)
                
                if width and height:
                    if int(width) < 50 or int(height) < 50:
                        continue
                
                # Skip data URLs and very small images
                if src.startswith('data:') or 'spacer.gif' in src or '1x1' in src:
                    continue
                
                print(f"Image {i+1}: {src}")
                
                # Generate filename
                parsed = urlparse(src)
                if parsed.path:
                    filename = os.path.basename(parsed.path)
                    if not filename:
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
                    
            except Exception as e:
                print(f"Error processing image {i+1}: {e}")
                continue
        
        print(f"\nDownloaded {downloaded_count} images successfully")
        
        # Also try to find background images in CSS
        print("\nLooking for background images...")
        elements = driver.find_elements(By.XPATH, "//*[@style]")
        
        for element in elements:
            style = element.get_attribute('style')
            if style and 'background-image' in style:
                # Extract URL from background-image
                match = re.search(r'background-image:\s*url\(["\']?([^"\')]+)["\']?\)', style)
                if match:
                    bg_url = match.group(1)
                    print(f"Background image: {bg_url}")
                    
                    filename = f"background_{len(os.listdir('images')) + 1}.jpg"
                    filepath = os.path.join('images', filename)
                    
                    if download_image(bg_url, filepath):
                        downloaded_count += 1
        
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_google_site()