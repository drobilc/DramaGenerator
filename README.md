# README

## Running

Run in command line as:

`python generate_drama.py <PATH TO INPUT FILE> -o=<PATH TO OUTPUT FILE> -p=<PARSER>`

where:

- `<PATH TO INPUT FILE>` is a mandatory parameter
- `<PATH TO OUTPUT FILE>` is optional with default value of `/drama_generator/generated_dramas/<INPUT FILE NAME>`
- `<PARSER>` is a mandatory parameter and should be chosen according to what social media are the messages from and in which format they are. Values can be choosen from the following options: `FacebookHTMLDataExtractor`, `TelegramJSONDataExtractor`.  

Example: `python generate_drama.py drama_generator/chats/AjdaFrankovic_sCuAc-0aFQ -o=drama_generator/generated_dramas/test1 -p=FacebookHTMLDataExtractor`

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
            "args": ["drama_generator/chats/AjdaFrankovic_sCuAc-0aFQ", "-o=drama_generator/generated_dramas/test1", "-p=FacebookHTMLDataExtractor"] //["<PAtH To INPUT FILE>", "-o=<PATH TO OUTPUT FILE>", "-p=<PARSER>", possible other arguments here, enclosed by ""]
        }
    ]
}
```
