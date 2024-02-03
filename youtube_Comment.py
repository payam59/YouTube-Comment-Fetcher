import argparse
from googleapiclient.discovery import build
import os
import re

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
            reply = item['snippet']['textDisplay']
            replies.append(reply)

        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            break

    return replies

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
            top_level_comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
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
    parser.add_argument('video_id', help='ID of the YouTube video for which to fetch comments and replies')
    parser.add_argument('--apikey', help='Your YouTube Data API v3 key', 
                        default='Your_API_Key')
    parser.add_argument('output_path', help='Path where the output file will be saved')

    args = parser.parse_args()

    # Build a resource object
    youtube = build('youtube', 'v3', developerKey=args.apikey)

    # Fetch video details to get the video title
    video_response = youtube.videos().list(
        part='snippet',
        id=args.video_id
    ).execute()

    if 'items' in video_response:
        video_title = video_response['items'][0]['snippet']['title']
    else:
        print('Video not found.')
        return

    sanitized_video_title = sanitize_filename(video_title)
    # Generate the output file name based on the video title
    output_file_name = f"{sanitized_video_title}.txt"
    output_file_path = os.path.join(args.output_path, output_file_name)

    # Fetch comments and replies
    video_comments = get_video_comments(youtube, args.video_id)

    # Write comments and replies to the generated file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for comment in video_comments:
            file.write(comment + '\n')

    # Print status update
    print(f'Total comments and replies fetched: {len(video_comments)}')
    print(f'Comments and replies saved to: {output_file_path}')

if __name__ == "__main__":
    main()
