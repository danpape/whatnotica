#!/usr/bin/env python3
"""
Whatnotica Shopify Scraper
--------------------------
Scrapes product data from the Shopify site and generates Zola-compatible
markdown files and downloads images.

Usage:
    python scrape_shopify.py

This will:
1. Fetch the product catalog pages
2. Extract product details (title, price, image, description)
3. Download product images to static/images/
4. Generate markdown files in content/products/
"""

import json
import os
import re
import urllib.request
import urllib.parse
from html.parser import HTMLParser
from pathlib import Path
import time
import ssl

# Configuration
SITE_URL = "https://www.whatnotica.com"
OUTPUT_DIR = Path(__file__).parent
CONTENT_DIR = OUTPUT_DIR / "content" / "products"
IMAGES_DIR = OUTPUT_DIR / "static" / "images"

# Create directories
CONTENT_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# SSL context for HTTPS
ssl_context = ssl.create_default_context()


def slugify(text):
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def fetch_url(url):
    """Fetch a URL and return the content."""
    print(f"  Fetching: {url}")
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (compatible; migration script)'
    })
    try:
        with urllib.request.urlopen(req, context=ssl_context, timeout=30) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"  Error fetching {url}: {e}")
        return None


def download_image(url, filename):
    """Download an image to the images directory."""
    filepath = IMAGES_DIR / filename
    if filepath.exists():
        print(f"  Image exists: {filename}")
        return True
    
    # Ensure URL has protocol
    if url.startswith("//"):
        url = "https:" + url
    
    # Remove width parameter for full resolution
    url = re.sub(r'\?.*$', '', url)
    
    print(f"  Downloading: {filename}")
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (compatible; migration script)'
    })
    try:
        with urllib.request.urlopen(req, context=ssl_context, timeout=30) as response:
            with open(filepath, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"  Error downloading {url}: {e}")
        return False


def fetch_products_json():
    """
    Shopify stores expose product data as JSON at /products.json
    This is the easiest way to get all product data!
    """
    url = f"{SITE_URL}/products.json"
    print(f"\nFetching product JSON from {url}")
    
    content = fetch_url(url)
    if not content:
        return None
    
    try:
        data = json.loads(content)
        return data.get('products', [])
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None


def create_product_markdown(product):
    """Generate a markdown file for a product."""
    title = product.get('title', 'Untitled')
    handle = product.get('handle', slugify(title))
    
    # Get price from first variant
    variants = product.get('variants', [])
    price = variants[0].get('price', '0.00') if variants else '0.00'
    
    # Get description (strip HTML tags simply)
    body_html = product.get('body_html', '')
    description = re.sub(r'<[^>]+>', '', body_html).strip() if body_html else ''
    
    # Get image
    images = product.get('images', [])
    image_url = images[0].get('src', '') if images else ''
    image_filename = ''
    
    if image_url:
        # Extract filename from URL
        image_filename = os.path.basename(urllib.parse.urlparse(image_url).path)
        # Clean up the filename
        image_filename = re.sub(r'\?.*$', '', image_filename)
        
        # Download the image
        download_image(image_url, image_filename)
    
    # Generate markdown content
    # Escape quotes in title for TOML format                         
    escaped_title = title.replace('"', '\\"')                       

    markdown = f'''+++
title = "{escaped_title}"
date = 2024-01-01

[extra]
price = "${price}"
image = "images/{image_filename}"
+++

{description}
'''
    
    # Write to file
    filepath = CONTENT_DIR / f"{handle}.md"
    print(f"  Creating: {filepath.name}")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    return True


def main():
    print("=" * 60)
    print("Whatnotica Shopify Migration Script")
    print("=" * 60)
    
    # Try the JSON endpoint first (easiest method)
    products = fetch_products_json()
    
    if not products:
        print("\nCouldn't fetch products.json - Shopify may have it disabled.")
        print("You may need to manually export products from Shopify admin.")
        return
    
    print(f"\nFound {len(products)} products")
    print("-" * 40)
    
    success_count = 0
    for i, product in enumerate(products, 1):
        print(f"\n[{i}/{len(products)}] Processing: {product.get('title', 'Unknown')}")
        try:
            if create_product_markdown(product):
                success_count += 1
        except Exception as e:
            print(f"  Error: {e}")
        
        # Be nice to the server
        time.sleep(0.5)
    
    print("\n" + "=" * 60)
    print(f"Migration complete!")
    print(f"  Products processed: {success_count}/{len(products)}")
    print(f"  Markdown files: {CONTENT_DIR}")
    print(f"  Images: {IMAGES_DIR}")
    print("=" * 60)
    
    print("\nNext steps:")
    print("  1. Review the generated files")
    print("  2. Run 'zola serve' to preview")
    print("  3. Run 'zola build' to generate static site")
    print("  4. Deploy to GitHub Pages / Cloudflare Pages")


if __name__ == "__main__":
    main()
