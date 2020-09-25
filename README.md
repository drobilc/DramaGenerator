# README

## Requirements

To run Drama generator you need the following installed:

- python libraries from `requirements.txt` file (`pip install requirements.txt`)
- XeLaTeX, download MiXTeX from <https://miktex.org/download> and follow this <http://www.texts.io/support/0002/> or similar installation guide, or install TeXWorks or similar that also includes XeLaTeX
- free font Gentium Basics, accessible here: <https://software.sil.org/gentium/download/>

## Running

Run in command line as:

`python generate_drama.py <PATH TO INPUT FILE> -o <PATH TO OUTPUT FILE> -p <PARSER> --title <TITLE> --from <DATE FROM> --to <DATE TO> --exclude <EXCLUDED PERSONS> --shout`

where:

- `<PATH TO INPUT FILE>` is the only mandatory parameter
- `<PATH TO OUTPUT FILE>` has default value of `/drama_generator/generated_dramas/<INPUT FILE NAME>`
- `<PARSER>` should be chosen according to what social media are the messages from and in which format they are. Values can be choosen from the following options: `FacebookHTMLParser`, `TelegramJSONDataExtractor`. If none is given, the default value `FacebookHTMLParser` will be used.
- `<TITLE>` is the title user wants for their drama/infographic
- `<DATE FROM>` only messges sent after this date will be used in the process of generating the drama/infographics, format YYYY-MM-DD-HH:MM:SS.UUUUUU, eg. 2020-03-27 or 2020-03-27-07:31:22.000000
- `<DATE TO>` only messges sent before this date will be used in the process of generating the drama/infographics, format YYYY-MM-DD-HH:MM:SS.UUUUUU, eg. 2020-03-27 or 2020-03-27-07:31:22.000000
- `<EXCLUDE PERSONS>` is a list of persons user wants excluded form the chat - their messages won't be used, the names of those persons have to be enclosed in `''`, e.g. `--exclude 'first person' \'second person\'`
- `--shout` capitalizes all the messages in the drama

Example:

```cmd
python generate_drama.py drama_generator/chats/AjdaFrankovic_sCuAc-0aFQ -o=drama_generator/generated_dramas/test1 -p FacebookHTMLParser, --title The Great Monologue of Ajda --from 2020-01-01-00:00:00:000001 --to 2020-07-15 --exclude 'Niki Bizjak'
```

For debugging in VSC, your `launch.json` file should look like so:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Generate Drama", //whatever name you like
            "type": "python",
            "request": "launch",
            "program": "${file}", //current file, but you can also set up a path to your file here
            "console": "integratedTerminal", // where to run
            "args": ["drama_generator/chats/AjdaFrankovic_sCuAc-0aFQ", "-o drama_generator/generated_dramas/test1", "-p FacebookHTMLParser"] //["<PAtH To INPUT FILE>", "-o=<PATH TO OUTPUT FILE>", "-p=<PARSER>", possible other arguments here, enclosed by ""]
        }
    ]
}
```
