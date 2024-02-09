import pandas as pd
from bs4 import BeautifulSoup
import re

def extract_video_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    video_info_list = []

    # Find all video containers
    video_containers = soup.find_all('div', {'data-e2e': 'recommend-list-item-container'})

    for video_container in video_containers:
        video_info = {}

        # Extract video ID
        video_id_container = video_container.find('div', class_='css-1fofj7p-DivBasicPlayerWrapper e1yey0rl2')
        if video_id_container and video_id_container.get('id'):
            video_info['videoID'] = video_id_container.get('id').split('-')[-1]
        else:
            video_info['videoID'] = 'N/A'

        # Extract creator's username
        creator_container = video_container.find('h3', {'data-e2e': 'video-author-uniqueid'})
        if creator_container:
            video_info['creator'] = creator_container.text.strip()

        # Extract likes, comments, favorites, shares
        stats_container = video_container.find('div', class_='css-1cifsuk-DivActionItemContainer e1whjx9o0')

        # Define a function to extract content between '>' and '<'
        def extract_content(tag):
            return re.search(r'>(.*?)<', str(tag)).group(1).strip()

        # Extracting likes, comments, favorites, shares using the extract_content function
        video_info['likes'] = extract_content(stats_container.find('strong', {'data-e2e': 'like-count'}))
        video_info['comments'] = extract_content(stats_container.find('strong', {'data-e2e': 'comment-count'}))
        video_info['favorites'] = extract_content(stats_container.find('strong', {'data-e2e': 'undefined-count'}))
        video_info['shares'] = extract_content(stats_container.find('strong', {'data-e2e': 'share-count'}))

        # Extracting hashtags
        hashtags_container = video_container.find_all('a', {'data-e2e': 'search-common-link'})
        video_info['hashtags'] = [tag.text for tag in hashtags_container]

        # Removing hashtags that we no longer want
        

        video_info_list.append(video_info)

    return video_info_list

# Read the HTML content from the saved .html file
html_file_path = "data_analysis/sample_data/tiktok.html"
with open(html_file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

# Extract video information and create a DataFrame
df = pd.DataFrame(extract_video_info(html_content), columns=['videoID', 'creator', 'likes', 
                                                             'comments', 'favorites', 'shares', 
                                                             'hashtags'])

# Save DataFrame to CSV
df.to_csv("data_analysis/scraped_data.csv", index=False)