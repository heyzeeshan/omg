# Odoo Module Generator (OMG)

A command-line tool to automate the initial setup of new Odoo modules.

## Installation

```bash
pip install odoo-module-generator
```

## Usage

```bash
omg <module_name> --model <ModelName> --fields <field1:Type,field2:Type> [--summary "Module Summary"] [--author "Author Name"]
```

**Example:**

```bash
omg my_custom_module --model "My Custom Model" --fields "name:Char,description:Text,amount:Float" --summary "A custom module for Odoo" --author "Your Name"
```
