# ani-cli (HiAnime Edition)

A modified version of [ani-cli](https://github.com/pystardust/ani-cli) that uses **HiAnime** as the source and includes **interactive mode**.

## Features

- 🎯 **HiAnime Integration** - Uses HiAnime API instead of AllAnime
- 💬 **Interactive Mode** - No flags needed! Just run `ani-cli` and answer prompts
- 🎭 **Sub/Dub Selection** - Choose between sub or dub interactively
- 📱 **iOS Support** - Works on iPhone/iPad via iSH
- 🍎 **macOS Compatible** - Fixed episode navigation for BSD grep

## Installation

### macOS / Linux

```bash
git clone https://github.com/monster-temp/ani-cli-hianime.git
cd ani-cli-hianime
chmod +x ani-cli extract_m3u8.py

# Install globally (optional)
sudo cp ani-cli /usr/local/bin/ani-cli
sudo cp extract_m3u8.py /usr/local/bin/extract_m3u8.py
```

### iOS (iSH)

1. Install [iSH](https://apps.apple.com/us/app/ish-shell/id1436902243) and [Infuse](https://apps.apple.com/us/app/infuse/id1136220934) from App Store
   - Alternative: Use [VLC](https://apps.apple.com/us/app/vlc-for-mobile/id650377962) instead (add `--vlc` flag)

2. Open iSH and update packages:
```bash
apk update
apk upgrade
```

3. Install dependencies:
```bash
apk add grep sed curl fzf git python3
```

4. Install ani-cli:
```bash
git clone --depth 1 https://github.com/monster-temp/ani-cli-hianime.git ~/.ani-cli-hianime
cp ~/.ani-cli-hianime/ani-cli /usr/local/bin/ani-cli
cp ~/.ani-cli-hianime/extract_m3u8.py /usr/local/bin/extract_m3u8.py
chmod +x /usr/local/bin/ani-cli
chmod +x /usr/local/bin/extract_m3u8.py
rm -rf ~/.ani-cli-hianime
```

5. Run it:
```bash
ani-cli
```

**Note:** The script will output an Infuse link by default that you can tap to open in Infuse for iOS.

**Using VLC instead of Infuse:** Add the `--vlc` or `-v` flag to use VLC instead:
```bash
ani-cli --vlc
```

## Usage

### Interactive Mode (Recommended)

Just run without any arguments:

```bash
ani-cli
```

It will ask you:
1. **Search anime:** `one piece`
2. **Sub or Dub? (s/d):** `d`
3. **Which episode?:** `111`

### With Flags (Classic Mode)

```bash
# Watch specific episode in dub
ani-cli --dub -e 111 "one piece"

# Watch episode range
ani-cli -e 1-5 "naruto"

# Download instead of streaming
ani-cli -d -e 1 "bleach"

# Use Infuse instead of VLC (iOS/macOS)
ani-cli --infuse "one piece"

# Use VLC explicitly
ani-cli --vlc "one piece"
```

## Requirements

- `curl`
- `sed`
- `grep`
- `python3`
- `fzf`
- Video player: `mpv`, `iina` (macOS), or `vlc`

## How It Works

1. Searches HiAnime for anime
2. Extracts episode list from HiAnime API
3. Gets video URL from Megacloud servers using Python extractor
4. Plays in your video player or downloads

## Credits & Acknowledgments

This project is a fork of the amazing [**ani-cli**](https://github.com/pystardust/ani-cli) by [pystardust](https://github.com/pystardust) and contributors.

### Original ani-cli
- **Repository:** https://github.com/pystardust/ani-cli
- **Author:** pystardust and the ani-cli community
- **Description:** A cli tool to browse and play anime

### What We Changed
- **Source:** Switched from AllAnime to HiAnime API
- **Interactive Mode:** Added prompts for anime name, sub/dub selection, and episode number
- **macOS Compatibility:** Fixed episode list extraction for BSD grep
- **iOS Support:** Optimized for iSH shell on iPhone/iPad
- **Megacloud Extractor:** Added Python-based M3U8 URL extraction

### Special Thanks
- Original ani-cli developers and maintainers for creating such an awesome tool
- HiAnime for providing a reliable anime streaming source
- The open-source community

## License

GPL-3.0 (same as original ani-cli)

This project inherits the GPL-3.0 license from the original ani-cli project.

