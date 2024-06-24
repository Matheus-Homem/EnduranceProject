import os
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from src.web.platform.core.enums import DefinitionType, TemplateType
from src.web.platform.core.protocols import Definition

def generate_html(definition_type: DefinitionType, definition: Definition):
    templates_dir = os.path.join('src', 'web', 'platform', 'jinja_templates')

    env = Environment(loader=FileSystemLoader(templates_dir))

    if definition_type == DefinitionType.PAGE:
        template_name = TemplateType.PAGE
    else:
        raise ValueError(f"Unsupported definition type: {definition_type}")

    try:
        template = env.get_template(template_name)
    except TemplateNotFound:
        raise FileNotFoundError(f"Template {template_name} not found in {env.loader.searchpath}")

    data = {
        "extends": '{% extends "base.html" %}',
        "title": definition.get_title(),
        "header": definition.get_header()
    }

    rendered_page = template.render(data)

    output_dir = os.path.join('outputs', 'html')
    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, 'rendered_page.html')

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(rendered_page)

    return output_file_path