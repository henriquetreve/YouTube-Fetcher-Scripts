import pandas as pd
from googleapiclient.discovery import build
import os
import isodate
import re
import random

# List of API keys
API_KEYS = [
    'YOUR_API_KEY_1',
    'YOUR_API_KEY_2',
    'YOUR_API_KEY_3',
    # Add more API keys as needed
]

def get_random_api_key():
    return random.choice(API_KEYS)

# Function to format duration
def format_duration(iso_duration):
    duration = isodate.parse_duration(iso_duration)
    total_seconds = int(duration.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# Function to sanitize the keyword to make it a valid filename
def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z0-9 \-_]', '_', name).strip().replace(' ', '_')

# Function to fetch video data from YouTube
def fetch_youtube_videos(query, max_results=200):
    api_key = get_random_api_key()
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    video_data = []
    next_page_token = None
    
    while len(video_data) < max_results:
        search_request = youtube.search().list(
            part='snippet',
            q=query,
            type='video',
            order='viewCount',
            maxResults=50,
            pageToken=next_page_token
        )
        
        search_response = search_request.execute()
        video_ids = [item['id']['videoId'] for item in search_response['items']]
        
        # Fetch video details in batches
        for i in range(0, len(video_ids), 50):
            batch_ids = video_ids[i:i + 50]
            video_request = youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=','.join(batch_ids)
            )
            video_response = video_request.execute()
            
            for item in video_response['items']:
                duration_iso = item['contentDetails']['duration']
                duration_seconds = isodate.parse_duration(duration_iso).total_seconds()
                if duration_seconds <= 60:  # Only include videos 60 seconds or shorter
                    video_format = 'Short video'
                    
                    video_info = {
                        'title': item['snippet']['title'],
                        'description': item['snippet']['description'],
                        'thumbnail': item['snippet']['thumbnails']['high']['url'],
                        'link': f"https://www.youtube.com/watch?v={item['id']}",
                        'views': item['statistics'].get('viewCount', 0),
                        'likes': item['statistics'].get('likeCount', 0),
                        'comments': item['statistics'].get('commentCount', 0),
                        'duration': format_duration(duration_iso),
                        'format': video_format
                    }
                    video_data.append(video_info)
                    
                    if len(video_data) >= max_results:
                        break
        
        if 'nextPageToken' in search_response:
            next_page_token = search_response['nextPageToken']
        else:
            break
    
    return video_data

# Function to resolve filename conflicts by appending a number
def resolve_filename_conflict(filename, extension):
    base_filename = filename
    counter = 1
    
    while os.path.exists(f"{base_filename}{extension}"):
        base_filename = f"{filename}({counter})"
        counter += 1
    
    return f"{base_filename}{extension}"

# Function to export data to CSV
def export_to_csv(data, filename):
    filename = resolve_filename_conflict(filename.replace('.csv', ''), '.csv')
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data exported to {filename}")

# Function to export data to Excel
def export_to_excel(data, filename):
    filename = resolve_filename_conflict(filename.replace('.xlsx', ''), '.xlsx')
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Data exported to {filename}")

# Main function
def main():
    query = input('Enter the keyword to search for YouTube videos: ')
    sanitized_query = sanitize_filename(query)
    
    videos = fetch_youtube_videos(query)
    
    export_format = input('Enter the export format (csv/excel): ').lower()
    directory = input('Enter the directory to save the file (leave blank for current directory): ')
    
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    
    if export_format == 'csv':
        filename = os.path.join(directory, f'youtube_shorts_{sanitized_query}.csv') if directory else f'youtube_shorts_{sanitized_query}.csv'
        export_to_csv(videos, filename)
    elif export_format == 'excel':
        filename = os.path.join(directory, f'youtube_shorts_{sanitized_query}.xlsx') if directory else f'youtube_shorts_{sanitized_query}.xlsx'
        export_to_excel(videos, filename)
    else:
        print('Invalid format. Please choose either "csv" or "excel".')

if __name__ == '__main__':
    main()
