from setuptools import setup, find_packages

setup(
    name='odoo-module-generator',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Jinja2',
    ],
    entry_points={
        'console_scripts': [
            'omg=odoo_module_generator.omg:main',
        ],
    },
    author='Mohammed Zeeshan Jagirdar', 
    author_email='mzjagirdar10@gmail.com', 
    description='A tool to automate Odoo module creation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/heyzeeshan/odoo-module-generator', 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
