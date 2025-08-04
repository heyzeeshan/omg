import argparse
import os
import re
from jinja2 import Environment, FileSystemLoader

def to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower().replace('.', '_').replace(' ', '_')

def main():
    parser = argparse.ArgumentParser(description='Odoo Module Generator')
    parser.add_argument('module_name', type=str, help='Name of the Odoo module')
    parser.add_argument('--model', action='append', help='Model name (e.g., "Res Partner")')
    parser.add_argument('--fields', action='append', help='Fields for the last specified model (e.g., "name:Char,age:Integer")')
    parser.add_argument('--summary', type=str, default='My Odoo Module', help='Module summary')
    parser.add_argument('--author', type=str, default='Me', help='Author name')

    args = parser.parse_args()

    if not args.model:
        print("Error: At least one model must be specified using --model")
        return

    models = []
    for i, model_name in enumerate(args.model):
        model = {
            'name': model_name,
            'description': model_name,
            'fields': []
        }
        if args.fields and i < len(args.fields):
            fields_str = args.fields[i]
            for field_str in fields_str.split(','):
                field_parts = field_str.split(':')
                field_name = field_parts[0]
                field_type = field_parts[1] if len(field_parts) > 1 else 'Char'
                model['fields'].append({
                    'name': field_name,
                    'type': field_type,
                    'string': field_name.replace('_', ' ').title(),
                    'required': False  # You can enhance this to take more field attributes
                })
        models.append(model)

    # Create module directory
    module_dir = os.path.join(os.getcwd(), args.module_name)
    os.makedirs(module_dir, exist_ok=True)

    # Create subdirectories
    for subdir in ['models', 'views', 'security']:
        os.makedirs(os.path.join(module_dir, subdir), exist_ok=True)

    # Load Jinja2 environment
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

    def camelcase_filter(s):
        parts = s.replace('_', ' ').replace('.', ' ').title().replace(' ', '')
        return parts[0].upper() + parts[1:] if parts else ''

    env.filters['camelcase'] = camelcase_filter
    env.filters['snake_case'] = to_snake_case

    # Data for templates
    template_data = {
        'module_name': args.module_name,
        'module_summary': args.summary,
        'author_name': args.author,
        'models': models
    }

    # Generate ir.model.access.csv
    ir_model_access_template = env.get_template('ir.model.access.csv.j2')
    with open(os.path.join(module_dir, 'security', 'ir.model.access.csv'), 'w') as f:
        f.write(ir_model_access_template.render(template_data))

    # Generate individual model files and collect imports
    model_imports = []
    model_template = env.get_template('model.py.j2')
    for model in models:
        model_filename = f"{to_snake_case(model['name'])}.py"
        model_imports.append(model_filename.replace('.py', ''))
        with open(os.path.join(module_dir, 'models', model_filename), 'w') as f:
            f.write(model_template.render(model=model))

    # Generate individual view files and collect view filenames for manifest
    view_files = []
    view_template = env.get_template('view.xml.j2')
    for model in models:
        view_filename = f"{to_snake_case(model['name'])}_views.xml"
        view_files.append(view_filename)
        with open(os.path.join(module_dir, 'views', view_filename), 'w') as f:
            f.write(view_template.render(model=model, module_name=args.module_name))

    # Generate __manifest__.py
    manifest_template = env.get_template('__manifest__.py.j2')
    with open(os.path.join(module_dir, '__manifest__.py'), 'w') as f:
        f.write(manifest_template.render(template_data, view_files=view_files))

    # Generate root __init__.py
    root_init_template = env.get_template('__init__.py.j2')
    with open(os.path.join(module_dir, '__init__.py'), 'w') as f:
        f.write(root_init_template.render(template_data))

    # Create models/__init__.py with dynamic imports
    with open(os.path.join(module_dir, 'models', '__init__.py'), 'w') as f:
        for imp in model_imports:
            f.write(f"from . import {imp}\n")

    # Create empty __init__.py in views subdirectory
    with open(os.path.join(module_dir, 'views', '__init__.py'), 'w') as f:
        pass

    print(f"Odoo module '{args.module_name}' created successfully!")

if __name__ == '__main__':
    main()