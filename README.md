# YouTube Music Downloader

@@TODO: GET SECOND TAKEOUT! 

@@TODO: GET SECOND TAKEOUT! 

@@TODO: GET SECOND TAKEOUT! 

This project automatically downloads music from your YouTube watch history. It relies on the [yt-dlp](https://github.com/yt-dlp/yt-dlp) command-line utility.

## Prerequisites
- Python 3
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) must be installed and available in your system's PATH.

## Setup Instructions

### Step 1: Download Google Takeout Data

1. Go to Google Takeout.
2. Uncheck all categories except **"YouTube and YouTube Music"**.
3. Click **"Multiple formats"** and set History to JSON.
4. *Optional but faster:* On "What to download" - Select only **Watch History**.
5. Click **"Next step"** and request your data.
6. When your archive is ready, download and extract it.
7. Copy the `watch-history.json` file from `Takeout/YouTube and YouTube Music/` into your local `./data/` folder in this project.

### Step 2: Ensure you are logged into YouTube

> **Note on Cookies:** You do **not** need a browser extension to manually export `cookies.txt`! This script is natively configured to dynamically extract your active YouTube session cookie directly from Google Chrome Beta's internal database (`~/.config/google-chrome-beta/Default`). 
> 
> If the cookies expire mid-download, the script will automatically restart itself to fetch fresh ones from Chrome.

1. Open **Google Chrome Beta**.
2. Go to [www.youtube.com](https://www.youtube.com).
3. Ensure you are logged into your Google/YouTube account.
4. Leave Chrome running in the background while the script runs so your session remains active.

## Running the Script

You can start the download process by running:
```bash
python3 main.py
```

To test the script and output without downloading everything, you can run a dry-run:
```bash
python3 main.py --dry-run
```
