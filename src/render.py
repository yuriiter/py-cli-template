from jinja2 import Environment, FileSystemLoader, select_autoescape
from filters import  format_languages, mask_phone_number, date_to_month_year, image_to_base64_filter
import os
import tempfile
import asyncio
from pyppeteer import launch

def render_template(template_path: str, data: dict) -> str:
    templates_dir = os.path.dirname(template_path)
    env = Environment(
        loader=FileSystemLoader(searchpath=templates_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template_name = os.path.basename(template_path)

    env.filters['format_languages'] = format_languages
    env.filters['mask_phone_number'] = mask_phone_number
    env.filters['date_to_month_year'] = date_to_month_year
    env.filters['image_to_base64_filter'] = image_to_base64_filter

    template = env.get_template(template_name)

    return template.render(data=data, base_url=templates_dir)

def render_pdf(html: str) -> bytes:
    async def render_pdf():
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file_path = temp_file.name

        browser = await launch()
        page = await browser.newPage()
        await page.setContent(html)
        await page.pdf({'path': temp_file_path})
        await browser.close()

        with open(temp_file_path, 'rb') as pdf_file:
            pdf_bytes = pdf_file.read()

        os.remove(temp_file_path)

        return pdf_bytes

    return asyncio.run(render_pdf())

if __name__ == "__main__":
    pass
