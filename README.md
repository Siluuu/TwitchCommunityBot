# TwitchCommunityBot
A Twitch bot programmed together with the community live on Twitch.

## Setup

### Prerequisites
- Python 3.10+ must be installed.
- Git must be installed for the installation steps below.

### Installation
1. Open **Command Prompt (CMD)**, **PowerShell**, or your preferred terminal on Windows.

2. Clone the repository:
   - Copy the repository URL: `https://github.com/Siluuu/TwitchCommunityBot.git`.
   - Run the following command in your terminal to clone the repository:
     ```
     git clone https://github.com/Siluuu/TwitchCommunityBot.git
     ```

3. Navigate to the project directory:
   - If you're using Command Prompt, enter:
     ```
     cd TwitchCommunityBot
     ```

4. Open the `.env` file in the project folder using any text editor (e.g., Notepad, Visual Studio Code) and replace the placeholder values with your Twitch credentials and any other required settings.

5. Double-click the `start.bat` file to run it:
   - On the first run, it will:
     - Create a virtual environment (`venv`).
     - Install the required Python packages listed in the `requirements.txt` file.

   This setup ensures all dependencies are properly installed, and the bot is ready to function.

## Dependencies
This project uses the following libraries:

- **[python-dotenv](https://github.com/theskumar/python-dotenv)** - Manages environment variables.
- **[TwitchIO](https://github.com/PythonistaGuild/TwitchIO)** - Provides tools to interact with Twitch chat.
- **[Requests](https://github.com/psf/requests)** - Simplifies HTTP requests.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer
By using this project, you agree to comply with the licenses of all third-party dependencies. Additionally, if you use this bot to interact with services like Twitch, you must ensure compliance with their terms of service and developer policies.
