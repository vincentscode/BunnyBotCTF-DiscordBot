# BunnyBotCTF-DiscordBot
🤖 A discord bot to track ctf progression and archive old ctf channels.

## Usage
0. Clone this repo
1. Rename `config/config.json.example` to `config/config.json` and provide a valid Discord API Key.
2. Download the container using `docker pull ghcr.io/vincentscode/bunnybot:latest`
3. Start the container with your config using `docker run -d -v $(pwd)/config:/usr/src/app/config ghcr.io/vincentscode/bunnybot:latest`
4. Add the Bot to your server
5. Enjoy!
