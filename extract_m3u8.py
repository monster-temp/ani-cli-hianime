#!/usr/bin/env python3
"""
Extract M3U8 URL from megacloud embed using the yt-dlp-hianime plugin's megacloud module
"""
import sys
import os
import site

# Try to find the megacloud module in various locations
possible_paths = [
    # macOS system Python
    '/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/yt_dlp_plugins/extractor',
    # User site-packages
    os.path.join(site.USER_SITE, 'yt_dlp_plugins', 'extractor'),
    # System site-packages (for iSH and other Linux)
    '/usr/lib/python3.11/site-packages/yt_dlp_plugins/extractor',
    '/usr/lib/python3.10/site-packages/yt_dlp_plugins/extractor',
    '/usr/local/lib/python3.11/site-packages/yt_dlp_plugins/extractor',
    '/usr/local/lib/python3.10/site-packages/yt_dlp_plugins/extractor',
]

# Add all Python site-packages directories
for path in site.getsitepackages():
    possible_paths.append(os.path.join(path, 'yt_dlp_plugins', 'extractor'))

# Try each path
megacloud_found = False
for path in possible_paths:
    if os.path.exists(path):
        sys.path.insert(0, path)
        megacloud_found = True
        break

if not megacloud_found:
    print("ERROR: Could not find megacloud module. Please install yt-dlp-hianime plugin:", file=sys.stderr)
    print("  python3 -m pip install --user https://github.com/pratikpatel8982/yt-dlp-hianime/archive/master.zip", file=sys.stderr)
    sys.exit(1)

try:
    from megacloud import Megacloud
except ImportError as e:
    print(f"ERROR: Failed to import megacloud module: {e}", file=sys.stderr)
    print("Please install yt-dlp-hianime plugin:", file=sys.stderr)
    print("  python3 -m pip install --user https://github.com/pratikpatel8982/yt-dlp-hianime/archive/master.zip", file=sys.stderr)
    sys.exit(1)

if len(sys.argv) < 2:
    print("Usage: extract_m3u8.py <megacloud_embed_url>", file=sys.stderr)
    sys.exit(1)

embed_url = sys.argv[1]

try:
    scraper = Megacloud(embed_url)
    data = scraper.extract()
    
    # Extract M3U8 URL from sources
    for source in data.get('sources', []):
        file_url = source.get('file')
        if file_url and file_url.endswith('.m3u8'):
            print(file_url)
            sys.exit(0)
    
    print("ERROR: No M3U8 URL found", file=sys.stderr)
    sys.exit(1)
    
except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)

