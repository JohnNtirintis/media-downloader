import os
import json
import time
import yt_dlp
import random
import logging
from pathlib import Path
from datetime import datetime

# Global config
config = {}
delimiter = None
file_format = '.mp3'  # Default before loading config

# Configure logging
log_dir = config.get('logs_directory', 'logs')
os.makedirs(log_dir, exist_ok=True)
log_filename = os.path.join(log_dir, 'downloader-{:%Y-%m-%d-%H-%M-%S}.log'.format(datetime.now()))

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def get_default_downloads_folder():
    """Get the default Downloads folder for the system"""
    return str(Path.home() / "Downloads")

def load_config():
    global config, delimiter, file_format
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        delimiter = config['delimiter']
        file_format = config['file_formats']['1']
        logger.info('Configuration loaded successfully')
    except FileNotFoundError:
        logger.error('config.json not found. Please ensure the file exists.')
        exit(1)
    except KeyError as e:
        logger.error(f'Missing configuration key: {e}')
        exit(1)
    except json.JSONDecodeError:
        logger.error('config.json is not valid JSON')
        exit(1)

def main():
    global file_format
    try:
        load_config()

        # Welcome Banner
        print("\n" + "="*50)
        print(" "*12 + "VIDEO DOWNLOADER")
        print("="*50)
        logger.info('Application started')
        
        # Display Current Settings
        print("\n[CURRENT SETTINGS]")
        print(f"  Delimiter  : '{delimiter}'")
        print(f"  Default Format : {file_format}")
        
        # Download Folder Selection
        print("\n[DOWNLOAD FOLDER]")
        default_downloads = get_default_downloads_folder()
        print(f"  Default: {default_downloads}")
        custom_folder = input("  Enter custom download folder (or press Enter for default): ").strip()
        download_folder = custom_folder if custom_folder else default_downloads
        
        # Create folder if it doesn't exist
        os.makedirs(download_folder, exist_ok=True)
        logger.info(f'Download folder set to: {download_folder}')
        print(f"  Download folder: {download_folder}")
        
        # File Format Selection
        print("\n[FILE FORMAT SELECTION]")
        print("  (1) MP3 - Audio only")
        print("  (2) MP4 - Video with audio")
        option = input("\n  Enter your choice (1 or 2): ").strip()
        
        file_format = config['file_formats'].get(option, '.mp3')
        logger.info(f'User selected format: {file_format}')
        print(f"  Format set to {file_format}")
        
        # Download Mode Selection
        print("\n[DOWNLOAD MODE SELECTION]")
        print("  (1) Single/Multiple URLs")
        print("  (2) Entire Playlist")
        option = input("\n  Enter your choice (1 or 2): ").strip()
        
        if option == '1':
            print("\n[SINGLE/MULTIPLE URL MODE]")
            print("  Enter video URL(s) to download.")
            print(f"  For multiple URLs, separate them by '{delimiter}'") 
            print(f"  Example: URL1{delimiter} URL2{delimiter} URL3")
            urls_input = input("\n  URL(s): ").strip()
            
            if urls_input:
                logger.info(f'Starting download from URLs')
                download_videos(urls_input, file_format, download_folder)
            else:
                logger.warning('No URLs provided')
                print("  No URLs entered.")
                
        elif option == '2':
            print("\n[PLAYLIST MODE]")
            playlist_url = input("  Enter playlist URL: ").strip()
            
            if playlist_url:
                logger.info(f'Starting playlist download from: {playlist_url}')
                download_playlist(playlist_url, file_format, download_folder)
            else:
                logger.warning('No playlist URL provided')
                print("  No URL entered.")
        else:
            logger.error('Invalid selection')
            print("\n  Invalid choice. Please enter 1 or 2.")
        
        print("\n" + "="*50)
        print("  Download process completed!")
        print("="*50 + "\n")
        logger.info('Application session ended')
        
    except Exception as e:
        logger.error(f'Unexpected error in main: {e}', exc_info=True)
        print(f"\n  An error occurred: {e}")
    
def download_video(url, file_format, download_folder):
    try:
        logger.info(f'Downloading video from: {url}')
        
        # Get appropriate quality format from config
        quality = config['quality_formats'].get('mp4', 'best[ext=mp4]')
        
        # Configure yt-dlp options for MP4 download
        ydl_opts = {
            'format': quality,
            'quiet': True,
            'no_warnings': True,
            'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
            'socket_timeout': 30,
            'retries': 3,
            'fragment_retries': 3,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            title = info.get('title', 'video')
            
        logger.info(f'Successfully downloaded: {filename}')
        print(f"Downloaded: {title}")
        return filename
    except yt_dlp.utils.DownloadError as e:
        logger.error(f'Invalid YouTube URL or unavailable: {url}')
        print(f"Invalid or unavailable URL")
        return None
    except Exception as e:
        logger.error(f'Error downloading video from {url}: {e}', exc_info=True)
        print(f"Error downloading: {e}")
        return None

def download_videos(urls, file_format, download_folder):
    try:
        # Remove trailing delimiters and split
        urls = urls.strip()
        if urls.endswith(delimiter):
            urls = urls.rstrip(delimiter)
        
        links = [url.strip() for url in urls.split(delimiter)]
        logger.info(f'Processing {len(links)} URL(s)')
        print(f"\n  Processing {len(links)} video(s)...\n")
        
        for i, url in enumerate(links, 1):
            if not url:
                continue
            
            print(f"  [{i}/{len(links)}] ", end="")
            
            if file_format == '.mp3':
                # Extract MP3 directly
                convert_to_mp3(url, file_format, download_folder)
            else:
                # Download MP4 video
                download_video(url, file_format, download_folder)
            
            # Add delay between downloads to avoid YouTube blocking
            if i < len(links):
                sleep_timer = random.randint(2, 5)
                logger.info(f'Waiting {sleep_timer} seconds before next download...')
                time.sleep(sleep_timer)
    except Exception as e:
        logger.error(f'Error in download_videos: {e}', exc_info=True)
        print(f"  Error processing URLs: {e}")

def download_playlist(url, file_format, download_folder):
    try:
        logger.info(f'Loading playlist: {url}')
        
        # Extract playlist info without downloading
        ydl_opts = {
            'extract_flat': 'in_playlist',
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(url, download=False)
            playlist_title = playlist_info.get('title', 'Playlist')
            video_urls = [f"https://www.youtube.com/watch?v={entry['id']}" 
                          for entry in playlist_info.get('entries', [])]
        
        print(f"\n  Playlist: {playlist_title}")
        print(f"  Videos in playlist: {len(video_urls)}\n")
        logger.info(f'Playlist loaded with {len(video_urls)} videos')
        download_videos(delimiter.join(video_urls), file_format, download_folder)
    except Exception as e:
        logger.error(f'Error loading playlist {url}: {e}', exc_info=True)
        print(f"  Error loading playlist: {e}")
    
def convert_to_mp3(url, file_format, download_folder):
    try:
        logger.info(f'Extracting MP3 from: {url}')
        print(f"Extracting MP3...", end="")
        
        # Get lowest quality format from config for MP3 (audio quality doesn't depend on video quality)
        quality = config['quality_formats'].get('mp3', 'worst')
        
        # Use yt-dlp to extract audio directly as MP3
        ydl_opts = {
            'format': quality,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True,
            'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
            'socket_timeout': 30,
            'retries': 3,
            'fragment_retries': 3,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'audio')
        
        logger.info(f'Successfully extracted MP3: {title}')
        print(f" Extracted: {title}")
    except yt_dlp.utils.DownloadError as e:
        logger.error(f'Invalid YouTube URL or unavailable: {url}')
        print(f" Invalid or unavailable URL")
    except Exception as e:
        logger.error(f'Error extracting MP3 from {url}: {e}', exc_info=True)
        print(f" Error: {e}")

if __name__ == '__main__':
    main()
    