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

1. Install [iSH](https://apps.apple.com/us/app/ish-shell/id1436902243) from App Store
2. Open iSH and run:

```bash
apk add curl sed grep python3 fzf git
git clone https://github.com/monster-temp/ani-cli-hianime.git
cd ani-cli-hianime
chmod +x ani-cli extract_m3u8.py
./ani-cli
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

## Credits

- Original [ani-cli](https://github.com/pystardust/ani-cli) by pystardust
- Modified for HiAnime integration
- Interactive mode and iOS support added

## License

GPL-3.0

