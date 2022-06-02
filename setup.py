from setuptools import setup, find_packages
from pathlib import Path

version = __import__("horuz").__version__

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='horuz',
    version=version,
    description='Save and query your recon data on ElasticSearch.',
    url="https://horuz.misalabs.com",
    author='Misa G.',
    author_email="hi@misalabs.com",
    maintainer='Misa G.',
    maintainer_email='hi@misalabs.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT license',
    packages=find_packages(),
    keywords = ['recon', 'elasticsearch'],
    include_package_data=True,
    install_requires=[
        'click==7.1.2',
        'elasticsearch==7.12.0',
        'requests==2.23.0',
        'dpath==2.0.1',
        'rich==9.13.0',
    ],
    entry_points='''
        [console_scripts]
        hz=horuz.cli:cli
    ''',
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.9', 
        'Programming Language :: Python :: 3.10',
    ],
)
