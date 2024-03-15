## YouTube Downloader Telegram Bot

### Overview
This Python script implements a Telegram bot that allows users to download videos from YouTube. It utilizes the `pytube` library for downloading videos and playlists, and interacts with users via Telegram's bot API.

### Prerequisites
- Python 3.x
- Required Python packages: `requests`, `pytube`, `decouple`, `python-telegram-bot`

### Installation
1. Clone the repository or download the script.
2. Install the required Python packages using pip:

```bash
pip install requests pytube decouple python-telegram-bot
```
or
```bash
pip install -r requirments.txt
```
3. Obtain a Telegram bot token from the BotFather on Telegram.
4. Create a `.env` file in the same directory as the script and add your bot token:
```bash
token=YOUR_BOT_TOKEN
```

### Usage
1. Start the bot by running the script (`python your_script.py`).
2. Interact with the bot via Telegram:
- Send the `/start` command to initiate the bot.
- Choose between downloading a video or a playlist.
- Send the YouTube video or playlist link to initiate the download.
- The bot will respond with the download progress and the downloaded file.

### Code Structure
- **`download_video_from_youtube(video_url)`**: Function to download a video from YouTube using its URL.
- **`start(update, context)`**: Function to handle the `/start` command and display the initial menu.
- **`button(update, context)`**: Function to handle button callbacks and user choices.
- **`handle_user_input(update, context)`**: Function to handle user input (video or playlist links) and initiate downloads.
- **`main()`**: Entry point of the script; initializes the Telegram bot and sets up the necessary handlers.

### License
This project is licensed under the MIT License.

### Contact
For any questions, feedback, or support, please contact [Omid] at [Omidmmadi@gmail.com].
