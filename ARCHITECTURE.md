Youtube Downloader

Iterate through `watch-history.json` file, extracting `titleUrl` and process items not containing `details/"From Google Ads"`.
Filter out non-music entries using a predefined `BLACKLIST_WORDS` list (e.g. trailers, vlogs, etc.).
Aggregate URLs into `yt-dlp.batch`.

Command execution: 
The script spawns `yt-dlp` in a continuous `while True` loop to dynamically capture active session cookies directly from the Google Chrome Beta SQLite database.
If `yt-dlp` emits a "cookies are no longer valid" warning, the script gracefully terminates the process and loops to restart `yt-dlp`, instantly capturing the freshly rotated cookie from Chrome without user intervention.

Command structure: 
`yt-dlp { if --dry-run then --max-downloads 1 } -r 16M -R 3 --buffer-size 8196K -o "./library/%(title)s.%(ext)s" --batch-file yt-dlp.batch --download-archive yt-dlp-download.history --restrict-filenames --no-overwrites --no-post-overwrites --part --mtime --cookies-from-browser chrome:~/.config/google-chrome-beta/Default --cache-dir ./cache/ --extract-audio --audio-format mp3 --audio-quality 0 --match-filters !is_live & duration < 28800`

Requirements: 
    titleUrl: Convert Unicode, remove "Watched "
    Allow options to be overridden on command line and passed through to yt-dlp, excepting --dry-run 
