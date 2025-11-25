import os
import requests
from bs4 import BeautifulSoup

# Configuration
HTML_FILE = 'landing.html'
IMAGES_DIR = 'images'

# Ensure images directory exists
os.makedirs(IMAGES_DIR, exist_ok=True)

# Read HTML file
with open(HTML_FILE, 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Find all gallery images
gallery_imgs = soup.select('.gallery-item img')

for idx, img in enumerate(gallery_imgs, start=1):
    img_url = img.get('data-src')
    if not img_url:
        continue
    ext = os.path.splitext(img_url.split('?')[0])[1] or '.jpg'
    local_name = f'img{idx}{ext}'
    local_path = os.path.join(IMAGES_DIR, local_name)
    print(f'Downloading {img_url} -> {local_path}')
    try:
        r = requests.get(img_url, timeout=10)
        r.raise_for_status()
        with open(local_path, 'wb') as out:
            out.write(r.content)
        # Update HTML src to local path
        img['src'] = f'{IMAGES_DIR}/{local_name}'
        img['data-src'] = ''
    except Exception as e:
        print(f'Failed to download {img_url}: {e}')

# Write updated HTML
with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(str(soup))

print('Done! All images downloaded and HTML updated.')
