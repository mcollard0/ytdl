# YouTube Music Downloader

This project automatically downloads music from your YouTube watch history. It relies on the [yt-dlp](https://github.com/yt-dlp/yt-dlp) command-line utility.

## Prerequisites
- Python 3
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) must be installed and available in your system's PATH.

## Setup Instructions

### Security Note
> **⚠️ WARNING:** Your `cookies.txt` file contains sensitive session information. Treat it like a password and **do not share it**. Do not commit it to version control.

### Step 1: Download Google Takeout Data

1. Go to Google Takeout.
2. Uncheck all categories except **"YouTube and YouTube Music"**.
3. Click **"Multiple formats"** and set History to JSON.
4. *Optional but faster:* On "What to download" - Select only **Watch History**.
5. Click **"Next step"** and request your data.
6. When your archive is ready, download and extract it.
7. Copy the `watch-history.json` file from `Takeout/YouTube and YouTube Music/` into your local `./data/` folder in this project.

### Step 2: Get a Browser Extension

You need an extension that can export cookies in the "Netscape" format. A popular choice is **Get cookies.txt** (available for Chrome and Firefox).

### Step 3: Export Your Cookies

1. Make sure you are logged into your YouTube/Google account in your browser.
2. Go to [www.youtube.com](https://www.youtube.com).
3. Click the "Get cookies.txt" extension icon in your browser's toolbar and click **Copy**. This will copy the cookie data to your clipboard.

### Step 4: Create the `cookies.txt` File

1. Create a new text file named `cookies.txt` inside your local `./data/` folder.
2. Paste the copied cookie data into this file and save it.

## Running the Script

You can start the download process by running:
```bash
python3 main.py
```

To test the script and output without downloading everything, you can run a dry-run:
```bash
python3 main.py --dry-run
```
