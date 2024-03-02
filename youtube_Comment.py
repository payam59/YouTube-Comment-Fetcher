import argparse
from googleapiclient.discovery import build
import os
import re
from urllib.parse import urlparse, parse_qs
from googleapiclient.errors import HttpError

# Function to get comment replies
def get_comment_replies(youtube, parent_id):
    replies = []
    next_page_token = None

    while True:
        response = youtube.comments().list(
            part='snippet',
            parentId=parent_id,
            maxResults=100,  # Maximum number of replies per request
            pageToken=next_page_token
        ).execute()

        for item in response['items']:
            reply_content = item['snippet']['textDisplay']
            reply_date = item['snippet']['publishedAt']  # Extract the date of the reply
            reply = f"{reply_date}: {reply_content}"  # Combine date and content
            replies.append(reply)

        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            break

    return replies


# Function to check if comments are disabled for a video
def are_comments_disabled(video_info):
    if 'status' in video_info:
        return video_info['status'].get('embeddable', True) is False or video_info['status'].get('publicStatsViewable', True) is False
    return False
 
# Function to get comments
def get_video_comments(youtube, video_id):
    comments = []
    next_page_token = None

    while True:
        response = youtube.commentThreads().list(
            part='snippet,replies',
            videoId=video_id,
            maxResults=100,  # Maximum number of comments per request
            pageToken=next_page_token
        ).execute()

        for item in response['items']:
            top_level_comment_content = item['snippet']['topLevelComment']['snippet']['textDisplay']
            top_level_comment_date = item['snippet']['topLevelComment']['snippet']['publishedAt']  # Extract the date
            top_level_comment = f"{top_level_comment_date}: {top_level_comment_content}"  # Combine date and content
            comments.append(top_level_comment)

            # Check if there are replies to the comment
            if 'replies' in item:
                comment_replies = get_comment_replies(youtube, item['snippet']['topLevelComment']['id'])
                comments.extend(comment_replies)

        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            break

    return comments

# Function to sanitize a string for use as a filename
def sanitize_filename(filename):
    # Remove invalid characters using a regular expression
    return re.sub(r'[\/:*?"<>|]', '_', filename)

def main():
    parser = argparse.ArgumentParser(description='YouTube Comments and Replies Fetcher')
    parser.add_argument('output_path', help='Path where the output files will be saved')
    parser.add_argument('--apikey', help='Your YouTube Data API v3 key', 
                        default='Your_KEY')


    args = parser.parse_args()

    # Ask the user for the YouTube video URLs separated by commas
    video_links = input('Enter the YouTube video URLs separated by commas: ')

    # Use a regular expression to extract video IDs from links
    video_ids = []
    for link in video_links.split(','):
        url_parsed = urlparse(link)
        video_id_match = re.search(r'(?:v=|be/)([^\?&]+)', url_parsed.path)
        if video_id_match:
            video_ids.append(video_id_match.group(1))
        else:
            # Try to extract video ID from query parameters if available
            query_params = parse_qs(url_parsed.query)
            video_id = query_params.get('v')
            if video_id:
                video_ids.append(video_id[0])
            else:
                print(f'Invalid YouTube video link: {link}')
                continue

    # Build a resource object
    youtube = build('youtube', 'v3', developerKey=args.apikey)

    for video_id in video_ids:
        try:
            # Fetch video details to get the video title
            video_response = youtube.videos().list(
                part='snippet,status',
                id=video_id
            ).execute()

            if 'items' in video_response:
                video_info = video_response['items'][0]
                video_title = video_info['snippet']['title']

                # Check if comments are disabled
                if are_comments_disabled(video_info):
                    print(f'Comments for video {video_id} are disabled.')
                    continue
            else:
                print(f'Video {video_id} not found.')
                continue

            # Sanitize the video title to remove invalid characters
            sanitized_video_title = sanitize_filename(video_title)

            # Generate the output file name based on the sanitized video title
            output_file_name = f"{sanitized_video_title}.txt"
            output_file_path = os.path.join(args.output_path, output_file_name)

            try:
                # Fetch comments and replies
                video_comments = get_video_comments(youtube, video_id)

                # Write comments and replies to the generated file
                with open(output_file_path, 'w', encoding='utf-8') as file:
                    for comment in video_comments:
                        file.write(comment + '\n')

                # Print status update for each video
                print(f'Total comments and replies fetched for video {video_id}: {len(video_comments)}')
                print(f'Comments and replies saved to: {output_file_path}')
            except HttpError as e:
                if 'commentsDisabled' in str(e):
                    print(f'Comments for video {video_id} are disabled.')
                else:
                    raise
        except Exception as e:
            print(f'An error occurred for video {video_id}: {str(e)}')

if __name__ == "__main__":
    main()
