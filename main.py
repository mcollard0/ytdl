#!/usr/bin/env python3
import json
import argparse
import subprocess
import sys
import os

HISTORY_FILE = "data/watch-history.json"
BATCH_FILE = "yt-dlp.batch"

BLACKLIST_WORDS = [
    "trailer",
    "teaser",
    "vlog",
    "interview",
    "podcast",
    "tutorial",
    "review",
    "gameplay",
    "unboxing",
    "guide",
    "walkthrough",
    "reaction",
    "let's play",
    "movie",
    " clip "
]

def clean_title(title):
    # Google Takeout JSON files are already decoded as UTF-8 by python json library,
    # but sometimes they encode utf-8 as latin-1. Let's fix that if present.
    try:
        # Check if it has mangled unicode like â
        if '\u00e2' in title or '\u00c3' in title:
            title = title.encode('latin1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass

    if title.startswith("Watched "):
        title = title[len("Watched "):]
    return title

def main():
    parser = argparse.ArgumentParser(description="Process YouTube history and run yt-dlp")
    parser.add_argument("--dry-run", action="store_true", help="Run yt-dlp in dry-run mode (max 1 download)")
    # accept any other arguments to pass to yt-dlp
    args, unknown_args = parser.parse_known_args()

    if not os.path.exists(HISTORY_FILE):
        print(f"Error: {HISTORY_FILE} not found.")
        sys.exit(1)

    print(f"Loading {HISTORY_FILE}...")
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    urls = []
    print("Processing entries...")
    for entry in data:
        details = entry.get("details", [])
        from_ads = any(d.get("name") == "From Google Ads" for d in details)
        
        if from_ads:
            continue
            
        title_url = entry.get("titleUrl")
        if not title_url:
            continue
            
        title = entry.get("title", "")
        cleaned_title = clean_title(title)
        
        # Check blacklist
        lower_title = cleaned_title.lower()
        if any(word in lower_title for word in BLACKLIST_WORDS):
            continue
            
        # Route through YouTube Music
        title_url = title_url.replace("www.youtube.com", "music.youtube.com")
        
        # We collect the URLs for the batch file
        urls.append(title_url)
    
    print(f"Writing {len(urls)} URLs to {BATCH_FILE}...")
    with open(BATCH_FILE, "w", encoding="utf-8") as f:
        for url in urls:
            f.write(f"{url}\n")
            
    # Construct yt-dlp command
    # Command suggestion from architecture:
    # yt-dlp { if --dry-run then --max-downloads 1 } -r 16MB -R 3 --buffer-size 8196K \
    # -o "/tmp/%(title)s.%(ext)s" --batch-file yt-dlp.batch --paths library/ \
    # --download-archive yt-dlp-download.history --restrict-filenames \
    # --no-overwrites --part --mtime --cookies data/cookies.txt \
    # --cache-dir ./cache/ --extract-audio --audio-format mp3 --audio-quality 0
    
    cmd = [
        "yt-dlp",
        "-r", "16M",
        "-R", "3",
        "--buffer-size", "8196K",
        "-o", "./library/%(title)s.%(ext)s",
        "--batch-file", BATCH_FILE,
        "--download-archive", "yt-dlp-download.history",
        "--restrict-filenames",
        "--no-overwrites",
        "--no-post-overwrites",
        "--part",
        "--mtime",
        "--cookies-from-browser", "chrome:~/.config/google-chrome-beta/Default",
        "--cache-dir", "./cache/",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "--match-filters", "!is_live & duration < 28800"
    ]
    
    if args.dry_run:
        cmd.extend(["--max-downloads", "1"])
        print("Dry run mode enabled. Appended --max-downloads 1")
        
    if unknown_args:
        cmd.extend(unknown_args)
        
    print(f"Running command: {' '.join(cmd)}")
    
    # We should create the cache and library directories just in case yt-dlp doesn't
    os.makedirs("./cache/", exist_ok=True)
    os.makedirs("library/", exist_ok=True)
    
    try:
        while True:
            process = subprocess.Popen(cmd, stderr=subprocess.PIPE, text=True)
            cookie_expired = False
            
            # Monitor stderr in real-time for the invalid cookies warning
            for line in process.stderr:
                sys.stderr.write(line)
                sys.stderr.flush()
                if "The provided YouTube account cookies are no longer valid" in line:
                    print("\n[WARNING] YouTube cookies rotated! Restarting yt-dlp to extract fresh cookies from Chrome...", file=sys.stderr)
                    process.terminate()
                    cookie_expired = True
                    break
                    
            process.wait()
            
            if cookie_expired:
                continue # Loop back around and execute yt-dlp again!
                
            if process.returncode != 0 and process.returncode != 101: # 101 is max-downloads exit code
                sys.exit(process.returncode)
                
            break # If it finishes without expiring, break out of loop!
            
    except KeyboardInterrupt:
        if 'process' in locals():
            process.terminate()
        sys.exit(1)
    except FileNotFoundError:
        print("Error: 'yt-dlp' executable not found. Please ensure it is installed and in your PATH.")
        sys.exit(1)

if __name__ == "__main__":
    main()
