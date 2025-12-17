# Installing ani-cli on iOS using iSH

## Prerequisites

1. Install [iSH](https://apps.apple.com/us/app/ish-shell/id1436902243) from the App Store
2. Install a video player:
   - [Infuse](https://apps.apple.com/us/app/infuse/id1136220934) (default, recommended, better UI)
   - [VLC for Mobile](https://apps.apple.com/us/app/vlc-for-mobile/id650377962) (alternative, free)

## Installation Steps

### 1. Update iSH packages

Open iSH and run:

```bash
apk update
apk upgrade
```

### 2. Install required dependencies

```bash
apk add grep sed curl fzf git python3 py3-pip
```

### 3. Install Python dependencies

```bash
python3 -m pip install --user https://github.com/pratikpatel8982/yt-dlp-hianime/archive/master.zip
```

This installs the megacloud extractor needed to get video URLs from HiAnime.

**Note:** This may take a few minutes on iSH as it needs to download and compile dependencies.

### 4. Install ani-cli

```bash
# Clone the repository
git clone --depth 1 https://github.com/monster-temp/ani-cli-hianime.git ~/.ani-cli-hianime

# Copy scripts to system path
cp ~/.ani-cli-hianime/ani-cli /usr/local/bin/ani-cli
cp ~/.ani-cli-hianime/extract_m3u8.py /usr/local/bin/extract_m3u8.py

# Make scripts executable
chmod +x /usr/local/bin/ani-cli
chmod +x /usr/local/bin/extract_m3u8.py

# Clean up
rm -rf ~/.ani-cli-hianime
```

### 5. Run ani-cli

```bash
ani-cli
```

## How It Works

1. The script will automatically detect that it's running on iSH
2. After selecting an anime and episode, it will display a clickable link
3. Tap the link to open the video in your chosen player (Infuse by default, or VLC)
4. The video will start playing

### Choosing Your Player

**Infuse (Default):**
```bash
ani-cli "one piece"
# or explicitly
ani-cli --infuse "one piece"
# or short form
ani-cli -I "one piece"
```

**VLC (Alternative):**
```bash
ani-cli --vlc "one piece"
# or short form
ani-cli -v "one piece"
```

## Example Usage

```bash
# Search and watch anime
ani-cli "one piece"

# Watch specific episode
ani-cli -e 5 "one piece"

# Watch dubbed version
ani-cli --dub "one piece"

# Continue from history
ani-cli -c
```

## Troubleshooting

### "command not found" error

Make sure `/usr/local/bin` is in your PATH:

```bash
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.profile
source ~/.profile
```

### VLC/Infuse link doesn't work

Make sure your chosen player is installed from the App Store:
- VLC uses the `vlc://` URL scheme
- Infuse uses the `infuse://` URL scheme

If the link doesn't work, try the other player with `--vlc` or `--infuse` flag.

### Missing dependencies

If you get errors about missing commands, install them:

```bash
apk add grep sed curl fzf git python3
```

## Notes

- Downloads are not recommended on iSH as they are very slow (this is an iSH limitation)
- The script automatically filters out incompatible stream types for iOS
- Subtitles may not work with all streams on iOS

