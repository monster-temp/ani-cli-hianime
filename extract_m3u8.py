#!/usr/bin/env python3
"""
Extract M3U8 URL from megacloud embed using the yt-dlp-hianime plugin's megacloud module
"""
import sys
sys.path.insert(0, '/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/yt_dlp_plugins/extractor')

from megacloud import Megacloud

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

