# InkuMail2

Simple script for building html newsletter email from html template and markdown file, 
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

 - `template.html` contains the base html template.
 - `example.md` contains example markdown file used for content of the newsletter.

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
Final html file can be found in the output directory, 
which is automatically created if it does not exist.


## Creating markdown content

Example of markdown content is provided in `example.md`. 
The top level heading is used as the email subject (Viikkomaili x/yy, in the example)


In addition to basic markdown, `[TOC]` marker can be used to include table of contents
in the desired spot. Table of contents includes all the headings between h2-h6. 
If the heading is bolded using markdown syntax the corresponding title is bolded in the table of contents.

Guide for basic markdown syntax can be found [here](https://www.markdownguide.org/basic-syntax/).


