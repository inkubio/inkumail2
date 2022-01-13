# InkuMail2

Simple script for building newsletter email from html template and markdown file, 
and sending it using smtp relay.

## Prerequisities
Python 3 (Tested with python3.9)

## Installation
1. (Optional) Create new virtual environment

~~~
python3 -m venv env
~~~

1.1 Activate virtual environment

~~~    
source env/bin/activate
~~~

2. Install required packages

~~~
pip3 install -r requirements.txt
~~~

## Configuration
Script is configured using `config.ini` file, which contains 
all configuration options. All fields are required.

## Usage
To create and send the file run:
~~~
python3 main.py
~~~
Sending email is currently only possible using SMTP auth with TLS.


To only create output html file without sending it as email:
~~~
python3 main.py --dry-run
~~~

## Creating markdown content
Example of markdown content is provided in `example.md`. 

Normal markdown syntax can be used.
Guide for basic markdown syntax can be found [here](https://www.markdownguide.org/basic-syntax/).

In addition to basic markdown, `[TOC]` marker can be used to include table of contents
in the desired spot.

