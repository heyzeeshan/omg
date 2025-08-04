import argparse
import os
from jinja2 import Environment, FileSystemLoader

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

    # Data for templates
    template_data = {
        'module_name': args.module_name,
        'module_summary': args.summary,
        'author_name': args.author,
        'models': models
    }

    # Render templates
    for template_name in os.listdir(os.path.join(os.path.dirname(__file__), 'templates')):
        template = env.get_template(template_name)
        file_content = template.render(template_data)
        file_name = template_name.replace('.j2', '')
        if file_name == 'models.py':
            with open(os.path.join(module_dir, 'models', file_name), 'w') as f:
                f.write(file_content)
        elif file_name == 'views.xml':
            with open(os.path.join(module_dir, 'views', file_name), 'w') as f:
                f.write(file_content)
        elif file_name == 'ir.model.access.csv':
            with open(os.path.join(module_dir, 'security', file_name), 'w') as f:
                f.write(file_content)
        else:
            with open(os.path.join(module_dir, file_name), 'w') as f:
                f.write(file_content)

    # Create empty __init__.py in subdirectories
    for subdir in []:
        with open(os.path.join(module_dir, subdir, '__init__.py'), 'w') as f:
            pass

    # Create __init__.py in models subdirectory and import models.py
    with open(os.path.join(module_dir, 'models', '__init__.py'), 'w') as f:
        f.write("from . import models\n")

    print(f"Odoo module '{args.module_name}' created successfully!")

if __name__ == '__main__':
    main()
