# CLI Tool: PDF Generator from Jinja Templates and JSON

This CLI tool allows you to generate PDF files from Jinja templates, using data provided in JSON format. You can supply either a JSON file or a JSON string as input and output the PDF to a specified location.

## Usage

```sh
(venv) ➜  cli_templating git:(main) python src/cli.py --help
usage: cli.py [-h] -t TEMPLATE -d DATA [-o OUTPUT]

Generate PDF from Jinja template

options:
  -h, --help            show this help message and exit
  -t TEMPLATE, --template TEMPLATE
                        Path to the Jinja template file
  -d DATA, --data DATA  Path to the JSON file with data or a JSON string
  -o OUTPUT, --output OUTPUT
                        Path to the output PDF file (optional)
```
