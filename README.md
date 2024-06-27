# YouTube-Fetcher-Scripts
A collection of Python scripts to fetch and export YouTube video data. This repository includes tools for retrieving YouTube videos, shorts, and longs based on keywords, with options to export the results to CSV or Excel files. Perfect for data analysis and content discovery.

# YouTube Video Fetcher Scripts

This repository contains three Python scripts to fetch video data from YouTube based on different criteria and export the results to CSV or Excel files.

## Scripts

### 1. YouTube Video Fetcher

**File**: `youtube_video_fetcher.py`

**Description**: 
Fetches YouTube videos based on a keyword, retrieves details about the videos, and exports the data to a CSV or Excel file.

### 2. YouTube Shorts Fetcher

**File**: `youtube_shorts_fetcher.py`

**Description**: 
Fetches YouTube short videos (60 seconds or shorter) based on a keyword, retrieves details about the videos, and exports the data to a CSV or Excel file.

### 3. YouTube Longs Fetcher

**File**: `youtube_longs_fetcher.py`

**Description**: 
Fetches YouTube long videos (longer than 60 seconds) based on a keyword, retrieves details about the videos, and exports the data to a CSV or Excel file.

## How to Use

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name
    ```

2. **Install Dependencies**:
    Ensure you have the necessary dependencies installed. You can use pip to install them:
    ```sh
    pip install pandas google-api-python-client isodate
    ```

3. **Run the Script**:
    Each script can be run from the command line. For example, to run the YouTube Video Fetcher script:
    ```sh
    python youtube_video_fetcher.py
    ```

4. **Follow Prompts**:
    The script will prompt you for:
    - A keyword to search for YouTube videos.
    - The export format (CSV or Excel).
    - The directory to save the file (leave blank for the current directory).

## API Key

These scripts require a YouTube Data API key. Add your API keys to the `API_KEYS` list in each script.

```python
API_KEYS = [
    'YOUR_API_KEY_1',
    'YOUR_API_KEY_2',
    'YOUR_API_KEY_3',
    # Add more API keys as needed
]
