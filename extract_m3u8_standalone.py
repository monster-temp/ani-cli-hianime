#!/usr/bin/env python3
"""
Standalone M3U8 extractor for megacloud - Python 3.9+ compatible
Based on yt-dlp-hianime plugin but simplified for iSH compatibility
"""
import sys
import re
import json
import base64

try:
    import requests
except ImportError:
    print("ERROR: requests module not found. Install with: apk add py3-requests", file=sys.stderr)
    sys.exit(1)

def hash_value(key):
    """Hash function for key generation"""
    key_value = 0
    for char in key:
        key_value = (key_value * 31 + ord(char)) & 0xFFFFFFFF
    return key_value

def compute_xor_value(key_len):
    """Compute XOR value for decryption"""
    base = 81
    max_val = 255
    k = (max_val - base) // key_len
    return base + key_len * k

def generate_index_sequence(n):
    """Generate index sequence for key extraction"""
    result = [5, 8, 14, 11]
    if n <= 4:
        return result
    for i in range(2, n - 2):
        result.append(result[i] + i + 3 - (i % 2))
    return result

def extract_key(script_content):
    """Extract encryption key from script"""
    # Find the key pattern in the script
    pattern = r'case\s+0x[0-9a-f]+:.*?=\s*([a-zA-Z_$][\w$]*)\s*,.*?=\s*([a-zA-Z_$][\w$]*);'
    matches = re.findall(pattern, script_content, re.DOTALL)
    
    if not matches:
        return None, None
        
    # Extract variable names
    var1, var2 = matches[0]
    
    # Find variable values
    val1_pattern = rf'var\s+{re.escape(var1)}\s*=\s*"([^"]+)"'
    val2_pattern = rf'var\s+{re.escape(var2)}\s*=\s*"([^"]+)"'
    
    val1_match = re.search(val1_pattern, script_content)
    val2_match = re.search(val2_pattern, script_content)
    
    if val1_match and val2_match:
        return val1_match.group(1), val2_match.group(1)
    
    return None, None

def decrypt_source(encrypted, key1, key2):
    """Decrypt the encrypted source URL"""
    try:
        # Decode base64
        decoded = base64.b64decode(encrypted).decode('utf-8')
        
        # Simple XOR decryption
        key = key1 + key2
        xor_val = compute_xor_value(len(key))
        
        result = []
        for i, char in enumerate(decoded):
            key_char = key[i % len(key)]
            decrypted_char = chr(ord(char) ^ ord(key_char) ^ xor_val)
            result.append(decrypted_char)
            
        return ''.join(result)
    except Exception as e:
        print(f"Decryption error: {e}", file=sys.stderr)
        return None

def extract_m3u8(embed_url):
    """Extract M3U8 URL from megacloud embed page"""
    try:
        # Get the embed page
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://hianime.to/'
        }

        # Extract the video ID from URL first
        video_id_match = re.search(r'/e-1/([^?]+)', embed_url)
        if not video_id_match:
            print(f"ERROR: Could not extract video ID from URL: {embed_url}", file=sys.stderr)
            return None

        video_id = video_id_match.group(1)

        # Get the sources API directly (simpler approach)
        api_url = f"https://megacloud.tv/embed-2/ajax/e-1/getSources?id={video_id}"
        api_response = requests.get(api_url, headers=headers, timeout=10)
        api_response.raise_for_status()

        data = api_response.json()

        # Debug: print the response structure
        print(f"DEBUG: API response keys: {list(data.keys())}", file=sys.stderr)

        # Try to get sources directly first
        sources = data.get('sources')

        if not sources:
            print(f"ERROR: No 'sources' field in API response: {data}", file=sys.stderr)
            return None

        # Check if it's a string (encrypted) or list (plain)
        if isinstance(sources, str):
            print("DEBUG: Sources are encrypted, attempting decryption...", file=sys.stderr)
            # Sources are encrypted - need to decrypt
            # Get the embed page to find the decryption script
            response = requests.get(embed_url, headers=headers, timeout=10)
            response.raise_for_status()

            script_match = re.search(r'<script[^>]*src="([^"]*e-1[^"]*)"', response.text)
            if not script_match:
                print("ERROR: Could not find decryption script in embed page", file=sys.stderr)
                return None

            script_url = script_match.group(1)
            if not script_url.startswith('http'):
                script_url = 'https://megacloud.tv' + script_url

            print(f"DEBUG: Fetching decryption script from: {script_url}", file=sys.stderr)
            script_response = requests.get(script_url, headers=headers, timeout=10)
            key1, key2 = extract_key(script_response.text)

            if not key1 or not key2:
                print("ERROR: Could not extract decryption keys from script", file=sys.stderr)
                return None

            print(f"DEBUG: Decryption keys found, decrypting...", file=sys.stderr)
            decrypted = decrypt_source(sources, key1, key2)
            if not decrypted:
                print("ERROR: Decryption failed", file=sys.stderr)
                return None

            try:
                sources = json.loads(decrypted)
            except json.JSONDecodeError as e:
                print(f"ERROR: Failed to parse decrypted sources: {e}", file=sys.stderr)
                return None

        # Now sources should be a list
        if not isinstance(sources, list):
            print(f"ERROR: Sources is not a list: {type(sources)}", file=sys.stderr)
            return None

        # Find the M3U8 URL
        for source in sources:
            if isinstance(source, dict) and source.get('file', '').endswith('.m3u8'):
                print(f"DEBUG: Found M3U8 URL", file=sys.stderr)
                return source['file']

        print(f"ERROR: No M3U8 URL found in sources: {sources}", file=sys.stderr)
        return None
        
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: extract_m3u8_standalone.py <megacloud_embed_url>", file=sys.stderr)
        sys.exit(1)
    
    m3u8_url = extract_m3u8(sys.argv[1])
    if m3u8_url:
        print(m3u8_url)
        sys.exit(0)
    else:
        sys.exit(1)

