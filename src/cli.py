import argparse
import json
import os
import time
import hashlib
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
        help="Path to the JSON file with data or a JSON string"
    )
    parser.add_argument(
        "-o", "--output",
        help="Path to the output PDF file (optional)"
    )
    return parser.parse_args()

def parse_data(data_path_or_string):
    try:
        with open(data_path_or_string, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return json.loads(data_path_or_string)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON data provided")

def generate_default_output_path(file_idx):
    timestamp = int(time.time())
    hash_value = hashlib.md5(f"{timestamp}".encode()).hexdigest()[:5]
    directory = f"out/generated_{hash_value}_{timestamp}"
    os.makedirs(directory, exist_ok=True)
    return os.path.join(directory, f"{file_idx}.pdf")

def main():
    args = parse_arguments()

    data = parse_data(args.data)

    html_output = render_template(args.template, data)
    pdf_output = render_pdf(html_output)

    output_path = args.output if args.output else generate_default_output_path(file_idx=0)

    # with open('output.html', "w") as f:
    #     f.write(html_output)

    with open(output_path, "wb") as f:
        f.write(pdf_output)

    print(f"PDF successfully generated and saved to {output_path}")

if __name__ == "__main__":
    main()
