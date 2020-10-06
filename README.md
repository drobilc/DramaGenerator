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
The `<PATH TO INPUT FILE>` is the only **mandatory** argument.

The drama generator script also accepts the following arguments:

### General arguments

These arguments can be applied regardless of the choice of social media, format of exported messages, or format you want generated.

|FLAG           |SHORTER FLAG|ARGUMENT|DEFAULT|MEANING|
|---------------|:----------:|:------:|-------|-------|
|`--output-file`|`-o `       |string  |`/drama_generator/generated_dramas/<INPUT FILE NAME>`|path to output file|
|`--parser`     |`-p`        |string  |`FacebookHTMLParser`|parser chosen according to what social media the messages sre from and in which format they are, values can be choosen from the following options: `FacebookHTMLParser`, `TelegramJSONDataExtractor`, `WhatsAppParser`, `PickleParser`|
|`--generator`  |`-g`        |string  |`LatexGenerator`|generator chosen based on what we want our generated file to be: a drama or an infografic with statistics; values can be choosen from the following options: `LatexGenerator`, `PlariLatexGenerator`, `StatisticsGenerator`|

### Parser specific arguments

|USABLE IN PARSER    |FLAG           |ARGUMENT|DEFAULT              |MEANING|
|--------------------|---------------|:------:|---------------------|-------|
|`FacebookHTMLParser`|`--date-format`|string  |`%b %d, %Y, %I:%M %p`|format of the datetime from the file with your exported messages to be used when parsing|
|`FacebookHTMLParser`|`--locale`     |string  |`english_us`         |locale from the file with your exported messages to be used when parsing dates\*|
|`WhatsAppParser`    |`--date-format`|string  |`%d/%m/%Y, %H:%M`    |format of the datetime from the file with your exported messages to be used when parsing|

\* in case date format contains localized date strings such as `Marec`/`March`/`März`/...

### Processor specific arguments - filters

These arguments can be applied regardless of the choice of social media, format of exported messages, or format you want generated. They do not have default values.

|FLAG       |SHORTER FLAG|ARGUMENT|MEANING|
|-----------|:----------:|:------:|-------|
|`--after`  |-`a`        |string  |date in format `YYYY-MM-DD-HH:MM:SS` or `YYYY-MM-DD`, only messages sent after this date will be used in generation process|
|`--before` |`-b`        |string  |date in format `YYYY-MM-DD-HH:MM:SS` or `YYYY-MM-DD`, only messages sent before this date will be used in generation process|
|`--exclude`|`-e`        |string  |list of persons separated by `,`, whose messages should not be used in generation process|
|`--shout`  |            |none    |if this flag is present, all messages in generated drama will be written in capital letters|

### Generator specific arguments

|USABLE IN GENERATOR   |FLAG              |SHORTER FLAG|ARGUMENT|DEFAULT    |MEANING|
|----------------------|------------------|:----------:|:------:|-----------|-------|
|`LatexGenerator`, `StatisticsGenerator`|`--title`         |`-t`        |string  |`The Drama`|title of the outputed document|
|`LatexGenerator`     |`--no-acts`       |            |none    |           |if this flag is present, the generated drama won't be divided into acts|
|`LatexGenerator`     |`--no-scenes`     |            |none    |           |if this flag is present, the generated drama won't be divided into scenes, and consequently, won't be divided into acts either|
|`LatexGenerator`     |`--new-scene-time`|            |float   |           |number of hours that need to pass between two consecutive messages for the first to end the last scene and the second to begin a new one|
|`StatisticsGenerator`|`--stopwords`     |            |string  |           |path to file containing a list of stopwords, each in its own line|

### Example usage

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
