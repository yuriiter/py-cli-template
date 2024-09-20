import phonenumbers
import base64
from datetime import datetime
from dateutil import parser

def date_string_or_date_to_date(date):
    if date is None:
        return date
    if isinstance(date, str):
        if date.lower() == "present":
            return date
        try:
            return parser.parse(date)
        except ValueError:
            return None
    return date

def date_to_month_year(date):
    final_date = date_string_or_date_to_date(date)

    if isinstance(final_date, str) and final_date == "present":
        return final_date

    if isinstance(final_date, datetime):
        month = str(final_date.month).zfill(2)
        year = final_date.year
        return f"{month}/{year}"
    
    return None


def mask_phone_number(phone_number: str) -> str:
    clean_number = phone_number.replace("+", "").replace(" ", "")
    
    try:
        parsed_number = phonenumbers.parse(f"+{clean_number}")
        return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    except phonenumbers.NumberParseException:
        return "Invalid phone number"

def format_languages(languages):
    return [f"{item['language']} ({item['level']})" for item in languages]

def image_to_base64_filter(image_path):
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_formatted_today(_dummy):
    return datetime.now().strftime("%B %d, %Y")
