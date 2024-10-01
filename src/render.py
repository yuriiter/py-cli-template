from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import tempfile
import asyncio
from pyppeteer import launch
import importlib.util
import inspect

def render_template(template_path: str, data: dict) -> str:
    templates_dir = os.path.dirname(template_path)
    env = Environment(
        loader=FileSystemLoader(searchpath=templates_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template_name = os.path.basename(template_path)

    filters_module_path = os.path.join(templates_dir, 'filters.py')
    if os.path.exists(filters_module_path):
        spec = importlib.util.spec_from_file_location("filters", filters_module_path)
        filters = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(filters)

        for name, func in inspect.getmembers(filters, inspect.isfunction):
            env.filters[name] = func

    template = env.get_template(template_name)
    return template.render(**data, base_url=templates_dir)

async def generate_pdf(html: str) -> bytes:
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

def render_pdf(html: str) -> bytes:
    return asyncio.run(generate_pdf(html))

def jinja_to_pdf(template_path: str, data: dict):
    html = render_template(template_path, data)
    pdf = render_pdf(html)
    return pdf

if __name__ == "__main__":
    pass
