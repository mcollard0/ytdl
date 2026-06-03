Youtube Downloader

Iterate through watch-history.json file, extracting titleUrl and process items not containing details/"From Google Ads", create yt-dlp yt-dlp.batch file. 

Command suggestion: 
yt-dlp { if --dry-run then --max-downloads 1 } -r 16MB -R 3 --buffer-size 8196K -o "library/%(title)s.%(ext)s" --batch-file yt-dlp.batch --download-archive yt-dlp-download.history --restrict-filenames --no-overwrites --part --mtime --cookies data/cookies.txt --cache-dir ./cache/ --extract-audio --audio-format mp3 --audio-quality 0 

Requirements: 
    titleUrl: Convert UNicode, remove "Watched "
    Allow options to be overridden on command line and passed through to yt-dlp, excepting --dry-run 

