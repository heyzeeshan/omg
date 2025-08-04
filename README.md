# Odoo Module Generator (OMG)

## Project Overview

The Odoo Module Generator (OMG) is a command-line interface (CLI) tool designed to streamline the initial setup of new Odoo modules. It automates the creation of essential boilerplate files, including Python models, XML views, and security access rules, based on simple command-line arguments. This tool significantly reduces the manual effort and potential for errors when starting new Odoo development projects, allowing developers to focus on core business logic faster.

## Features

-   **Automated Module Structure:** Generates the standard Odoo module directory structure.
-   **Python Model Generation:** Creates `models.py` with defined models and fields (Char, Integer, Float, Text, etc.).
-   **XML View Generation:** Produces `views.xml` for form, tree, and action views, ready for customization.
-   **Security Access Rules:** Sets up `ir.model.access.csv` for basic user permissions.
-   **Customizable Metadata:** Allows specifying module name, summary, and author.
-   **CamelCase Class Names:** Automatically converts model names to Odoo-standard CamelCase for Python classes.
-   **Clean `__init__.py` Management:** Ensures correct `__init__.py` files are placed for proper module and package recognition.

## Technologies Used

-   **Python:** The core programming language for the CLI tool.
-   **Jinja2:** A powerful templating engine used to generate the Odoo module files (Python, XML, CSV).
-   **`argparse`:** Python's standard library for parsing command-line arguments.

## Installation

You can install OMG directly from PyPI using pip:

```bash
pip install odoo-module-generator
```

## Usage

To generate a new Odoo module, run the `omg` command followed by your desired module name and model definitions.

```bash
omg <module_name> --model <ModelName> --fields <field1:Type,field2:Type> [--summary "Module Summary"] [--author "Author Name"]
```

### Arguments:

-   `<module_name>`: The technical name of your Odoo module (e.g., `my_custom_module`). This will also be the name of the generated directory.
-   `--model <ModelName>`: (Required, can be repeated) Defines an Odoo model. The `ModelName` will be converted to CamelCase for the Python class and snake_case for the `_name` attribute.
    -   Example: `--model "Product Item"`
-   `--fields <field1:Type,field2:Type>`: (Optional, applies to the last `--model` defined) Defines fields for the model.
    -   `field1`: The technical name of the field (e.g., `product_code`).
    -   `Type`: The Odoo field type (e.g., `Char`, `Integer`, `Float`, `Text`, `Boolean`, `Date`, `Datetime`).
    -   Example: `--fields "code:Char,quantity:Integer,notes:Text"`
-   `--summary "Module Summary"`: (Optional) A brief description of your module. Defaults to "My Odoo Module".
-   `--author "Author Name"`: (Optional) The author's name for the module manifest. Defaults to "Me".

### Examples:

#### 1. Basic Module with One Model and Fields

Generate a module named `my_crm` with a model `Customer` and fields `name` (Char) and `email` (Char):

```bash
omg my_crm --model "Customer" --fields "name:Char,email:Char" --summary "Custom CRM module" --author "John Doe"
```

#### 2. Module with Multiple Models

Generate a module named `project_management` with two models: `Project` and `Task`.

```bash
omg project_management \
    --model "Project" --fields "name:Char,start_date:Date,end_date:Date" \
    --model "Task" --fields "name:Char,description:Text,is_done:Boolean" \
    --summary "Project Management Module"
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues on the [GitHub repository](https://github.com/yourusername/odoo-module-generator).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.