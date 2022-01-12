import argparse

from markdown import markdown
from markdown.extensions.toc import TocExtension

from bs4 import BeautifulSoup
from premailer import transform


def create_html(output_file: str = "output.html", template_file: str = "template.html",
                markdown_file: str = "example.md") -> None:
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
    template_soup.title.string = content_soup.find("h1").string

    # Change back to string and make css inline
    output_html = template_soup.prettify()
    output_html = transform(output_html)

    # Write modified data to file
    with open(f"output/{output_file}", "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
        output_file.write(output_html)


def main():
    parser = argparse.ArgumentParser(description="InkuMail2 newsletter generator")
    parser.add_argument("-o", "--output", type=str, help="Output file name", default="viikkomaili.html")
    parser.add_argument("-t", "--template", type=str, help="Template file name", default="template.html")
    parser.add_argument("-f", "--file", type=str, help="Markdown content file", default="example.md")

    args = parser.parse_args()
    create_html(output_file=args.output, template_file=args.template, markdown_file=args.file)


if __name__ == "__main__":
    main()
