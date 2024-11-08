# setup.py

from setuptools import setup, find_packages
from pathlib import Path

# Read the long description from README.md
with open(Path(__file__).parent / 'README.md', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setup(
    name='repo2text',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pathspec>=0.9.0',
        'colorama>=0.4.4',
        'pyperclip>=1.8.2',
    ],
    entry_points={
        'console_scripts': [
            'repo2text=repo2text:main',
        ],
    },
    description='A tool to convert entire repositories into an LLM-friendly text format and copy it to the clipboard.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
