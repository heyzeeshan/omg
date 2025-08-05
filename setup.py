from setuptools import setup, find_packages

setup(
    name='omg-cli',
    version='0.1.8',
    packages=find_packages(),
    package_data={
        'omg_cli': ['templates/*.j2'],
    },
    include_package_data=True,
    install_requires=[
        'Jinja2',
    ],
    entry_points={
        'console_scripts': [
            'omg=omg_cli.__main__:main',
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
