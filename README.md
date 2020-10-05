# Drama generator
> Make a drama out of your chats

Drama generator is an easily extensible Python script for generating dramatic texts from chats on social media sites.

Currently, we can generate dramas from chats exported from:
- [Facebook Messenger](https://www.messenger.com/)
- [Telegram](https://telegram.org/)
- [WhatsApp](https://www.whatsapp.com/)

To learn how generate your own dramas, you can read our [Wiki page](https://github.com/drobilc/DramaGenerator/wiki) or follow our installation instructions below.

## Installation

Before running `DramaGenerator` script, make sure you have the following requirements:

- `XeLaTeX` - download [MiXTeX](https://miktex.org/download) and follow [this](http://www.texts.io/support/0002/) installation guide
- free font [Gentium Basics](https://software.sil.org/gentium/download/)

After you've installed all requirements listed above, run the following commands to clone this repository and install all Python requirements.

```cmd
git clone https://github.com/drobilc/DramaGenerator.git
cd DramaGenerator
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Running

Run the drama generator script using `python generate_drama.py <PATH TO INPUT FILE>`.
The `<PATH TO INPUT FILE>` is the only mandatory argument

The drama generator script also accepts the following arguments:

- `--output-file` `<PATH TO OUTPUT FILE>` has default value of `/drama_generator/generated_dramas/<INPUT FILE NAME>`
- `--parser <PARSER>` should be chosen according to what social media are the messages from and in which format they are. Values can be choosen from the following options: `FacebookHTMLParser`, `TelegramJSONDataExtractor`. If none is given, the default value `FacebookHTMLParser` will be used.
- `--title <TITLE>` is the title user wants for their drama/infographic
- `--after <DATE FROM>` only messages sent after this date will be used in the process of generating the drama, format `YYYY-MM-DD-HH:MM:SS`, eg. `2020-03-27` or `2020-03-27-07:31:22`
- `--before <DATE TO>` only messages sent before this date will be used in the process of generating the drama, format `YYYY-MM-DD-HH:MM:SS`, eg. `2020-03-27` or `2020-03-27-07:31:22`
- `--exclude <EXCLUDE PERSONS>` is a list of persons user wants excluded form the chat - their messages won't be used, e.g. `--exclude "first person,second person,third person"`
- `--shout` capitalizes all the messages in the drama

Example:

```cmd
    python generate_drama.py
        drama_generator/chats/test_input
        --output-file drama_generator/generated_dramas/test_output
        --parser FacebookHTMLParser
        --title "The Great Monologue"
        --after 2020-01-01-00:00:00
        --before 2020-07-15
```

## Debugging

For debugging in Visual Studio Code, your `launch.json` file should look like so:

```json
{
    "configurations": [
        {
            "name": "Python: Generate Drama",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "args": ["drama_generator/chats/test_input",
                    "-o=generated_dramas/test_output",
                    "-p=FacebookHTMLParser",
                    "--title='The Great Monologue'",
                    "-a=2020-03-27-07:31:22",
                    "-b=2020-09-03",
                    "-e=Jane Doe",
                    "--shout"]
        }
    ]
}
```
