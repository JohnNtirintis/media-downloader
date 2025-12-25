# Media Downloader

A Python-based video and audio downloader that supports downloading from YouTube and other video platforms. Download individual videos, multiple URLs at once, or entire playlists.

## Features

- **Multiple Download Modes**
  - Single/Multiple URL downloads
  - Entire playlist downloads
  
- **Format Options**
  - MP3 (audio only)
  - MP4 (video with audio)

- **Customizable Settings (config.json)**
  - Configure delimiter for multiple URLs
  - Adjust quality settings for different formats
  - Specify custom download folders
  
- **Logging**
  - Detailed logs saved to `logs/` directory (can be changed in config.json)
  - Log files for each session

## Requirements

- Python 3.7 or higher
- `yt-dlp` (YouTube downloader)
- FFmpeg (for audio/video conversion)

## Installation

1. Clone or download this repository:
   ```bash
   git clone <repository-url>
   cd media-downloader
   ```

2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure FFmpeg is installed on your system:
   - **Windows**: Download from [FFmpeg official website](https://ffmpeg.org/download.html) or use `choco install ffmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `apt-get install ffmpeg`

## Configuration

Edit `config.json` to customize the downloader:

```json
{
    "logs_directory": "logs",
    "delimiter": ",",
    "file_formats": {
        "1": ".mp3",
        "2": ".mp4"
    },
    "quality_formats": {
        "mp3": "worst",
        "mp4": "best[ext=mp4]"
    }
}
```

### Configuration Options

- **logs_directory**: Directory where log files are stored
- **delimiter**: Character(s) to separate multiple URLs (default: comma)
- **file_formats**: Available format options to present to the user
- **quality_formats**: Quality settings for each format
  - `mp3`: "worst" for smaller file sizes, or "best" for better quality
  - `mp4`: "best[ext=mp4]" for best quality MP4 videos

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. Follow the on-screen prompts:
   - Select a download folder (or use the default Downloads folder)
   - Choose file format (MP3 or MP4)
   - Select download mode (single/multiple URLs or playlist)
   - Enter the video URL(s) or playlist URL

### Example Usage

**Single URL:**
```
Enter video URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

**Multiple URLs (comma-separated):**
```
Enter video URLs: https://www.youtube.com/watch?v=video1, https://www.youtube.com/watch?v=video2, https://www.youtube.com/watch?v=video3
```

**Playlist:**
```
Enter playlist URL: https://www.youtube.com/playlist?list=PLxxxxxx
```

## Project Structure

```
media-downloader/
├── main.py              # Main application script
├── config.json          # Configuration file
├── README.md            # This file
├── logs/                # Log files (auto-created)
└── requirements.txt     # Python dependencies
```

## Logging

All download activities are logged to the `logs/` directory. Log files are named with timestamps for easy tracking of download sessions:

```
logs/downloader-2025-12-26-14-30-45.log
```

Each log contains:
- Timestamp of each operation
- Log level (INFO, ERROR, WARNING)
- Details about downloads and errors

## Error Handling

The application includes robust error handling for:
- Invalid URLs
- Network connectivity issues
- Missing configuration files
- Missing dependencies
- File system errors

All errors are logged to both console and log files for troubleshooting.

## Troubleshooting

**"config.json not found" error:**
- Ensure `config.json` exists in the same directory as `main.py`
- Check that the file has valid JSON syntax

**"yt-dlp not installed" error:**
- Run `pip install yt-dlp`

**"FFmpeg not found" error:**
- Install FFmpeg on your system (see Installation section)

**Downloads are slow:**
- Check your internet connection
- Modify quality settings in `config.json`

## Supported Platforms

- Windows
- macOS
- Linux

## License

This project is open source and available under the MIT License.

## Support

For issues or feature requests, please create an issue in the repository.

---

**Made with Python and yt-dlp**
