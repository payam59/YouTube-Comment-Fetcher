# YouTube Comment Fetcher

This tool is designed to fetch all top-level comments and their replies from a specified YouTube video. 
It uses the YouTube Data API v3 to retrieve the comments and saves them to a text file.

## Installation

Before using this tool, make sure you have Python installed on your system. This tool requires Python 3.x.

1. Clone the Repository:
   
git clone https://github.com/payam59/YouTube-Comment-Fetcher.git
cd YouTube-Comment-Fetcher

2. Install Dependencies:
This tool requires `google-api-python-client`. You can install it using pip:

pip install --upgrade google-api-python-client


3. API Key:
You need a YouTube Data API v3 key to use this tool. Follow these steps to obtain your API key:
- Go to the [Google Developers Console](https://console.developers.google.com/).
- Create a new project.
- Enable the YouTube Data API v3 for your project.
- Create credentials (API key) for your project.

## Usage

Run the script from the command line, providing the YouTube video URLS and the output path. You can also specify your API key if you don't want to use the default one.

python youtube_comment_fetcher.py [OUTPUT_PATH] --apikey [YOUR_API_KEY]

- `OUTPUT_PATH`: Replace this with the path where the output files will be saved.
- `YOUR_API_KEY` (optional): Use this if you want to specify a different API key.

Example:
python youtube_comment_fetcher.py D:\OutputFolder --apikey yourapikey

When prompted, 'Enter the YouTube video URLs separated by commas:'

enter the YouTube video URLs separated by commas.
   Like: https://www.youtube.com/watch?v=yS_eLn36tL0,https://www.youtube.com/watch?v=OnjX0O9dPMc

The script will fetch comments and replies for each video and save them as separate files in the specified `OUTPUT_PATH`.

- Note: You should replace `[OUTPUT_PATH]` and `[YOUR_API_KEY]` with your specific output path and API key.

## API Quota Limits

Note that the YouTube Data API has quota limits. Fetching a large number of comments and replies may consume your API quota rapidly. 
Ensure that your usage complies with YouTube's terms of service and monitor your API usage.

## License

[MIT License](https://github.com/payam59/YouTube-Comment-Fetcher/blob/main/LICENSE)

## Contributions

Contributions are welcome. Please feel free to submit a pull request or open an issue.

---

This project is not affiliated with YouTube or Google.
