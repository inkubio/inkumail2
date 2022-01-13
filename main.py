import argparse
import configparser
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


from markdown import markdown
from markdown.extensions.toc import TocExtension

from bs4 import BeautifulSoup
from premailer import transform


def create_html(output_file: str = "output.html", template_file: str = "template.html",
                markdown_file: str = "example.md") -> (str, str, str):
    # Read template file to memory and convert to soup
    with open(template_file, "r") as f:
        template = f.read()
    template_soup = BeautifulSoup(template, "html.parser")

    # Read content file to memory.
    with open(markdown_file, "r") as f:
        content = f.read()

    # Convert markdown -> html -> soup
    content_html = markdown(content, extensions=["attr_list", TocExtension(title="Sisältö", toc_depth="2-6")])
    content_soup = BeautifulSoup(content_html, "html.parser")

    # Find and insert the content to the template
    content_div = template_soup.find("div", {"id": "content"})
    content_div.contents = content_soup

    # Set title
    title = content_soup.find("h1").string
    template_soup.title.string = title

    # Change back to string and make css inline
    output_html = template_soup.prettify()
    output_html = transform(output_html)

    # Write modified data to file
    with open(f"output/{output_file}", "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
        output_file.write(output_html)

    return output_html, content, title


def send_email(from_field: str, to_field: str, subject: str, html_content: str, text_content: str,
               smtp_server: str, port: int, user: str, pwd: str):
    msg = MIMEMultipart('alternative')
    msg["Subject"] = subject
    msg["From"] = from_field
    msg["To"] = to_field

    text = text_content
    html = html_content

    text_mime = MIMEText(text, 'plain')
    html_mime = MIMEText(html, 'html')

    msg.attach(text_mime)
    msg.attach(html_mime)

    mail = smtplib.SMTP(smtp_server, port)
    mail.starttls()
    mail.login(user, pwd)
    mail.sendmail(from_field, to_field, msg.as_string())
    mail.quit()


def main():
    parser = argparse.ArgumentParser(description="InkuMail2 newsletter generator")
    parser.add_argument("--dry-run", action="store_true", help="Only generate html file. Do not send email")

    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read('config.ini')

    output_html, markdown_content, title = create_html(output_file=config["newsletter"]["output"], template_file=config["newsletter"]["template"], markdown_file=config["newsletter"]["content"])

    if args.dry_run:
        return

    send_email(from_field=config["email"]["from"], to_field=config["email"]["to"], subject=title,
               html_content=output_html, text_content=markdown_content, smtp_server=config["email"]["smtp_server"],
               port=int(config["email"]["port"]), user=config["email"]["username"], pwd=config["email"]["password"])


if __name__ == "__main__":
    main()
