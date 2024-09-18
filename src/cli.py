import argparse
import json
from render import render_template, render_pdf

def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate PDF from Jinja template")
    parser.add_argument(
        "-t", "--template",
        required=True,
        help="Path to the Jinja template file"
    )
    parser.add_argument(
        "-d", "--data",
        required=True,
        help="Path to the JSON file with data"
    )
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Path to the output HTML file"
    )
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Load JSON data
    with open(args.data, "r") as f:
        data = json.load(f)

    # Render the template
    html_output = render_template(args.template, data)
    pdf_output = render_pdf(html_output)

    with open('output.html', "w") as f:
        f.write(html_output)

    with open(args.output, "wb") as f:
        f.write(pdf_output)

    print(f"HTML successfully generated and saved to {args.output}")

if __name__ == "__main__":
    main()
