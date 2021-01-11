# NaaandezBot
Discord Bot that replies to some custom commands. Made to have fun with the Discord API.

## Requirements
`python >=3.7`

## Installation
```
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Usage
Create a Discord Bot [following these instructions](https://discordpy.readthedocs.io/en/latest/discord.html#discord-intro), then place your bot's token on a new file called `.env` like follows:

```BOT_TOKEN=YOUR_TOKEN_HERE```

Finally, run `python main.py` and you're all set up!

### Note
To use the Google Calendar functionality, you would have to obtain your `credentials.json` from the Google Developer's Console ([see here](https://developers.google.com/calendar/quickstart/python)) and place it in the `config` folder.

## Commands
Various commands are included within the bot. All prefixes support the `help` directive, which inform the user how to use a given command.

### Piru
Commands that start with `!piru` prefix make the bot reply with cat ASCII art according to each mood passed in as argument:
* `!piru play`
* `!piru sleep`
* `!piru alert`
* `!piru stare`
* `!piru love`

### Wave
The `!wave` command makes the bot expect the '👋' emoji from the user before 15 seconds are up. If done successfully, you would make the bot happy. If not, the bot would be angry at you.

### Rekt
The `!rekt` command returns a spoiler-marked image of our lord and saviour, Gino.

### Google Calendar Events
Commands that start with `!cal` prefix make the bot reply with the events from a particular Gmail account linked to the `credentials.json` file. Can be formatted as an ASCII calendar or as a simple list.
* `!cal events`
* `!cal view`

## Disclaimers
Only has been tested on a MacBookPro running macOS Catalina Version 10.15.7. You may have to install SSL Certificates manually on the machine where the bot is being run ([see this issue](https://github.com/Rapptz/discord.py/issues/423), which I've solved with `sudo path/to/Install\ Certificates.command`).
