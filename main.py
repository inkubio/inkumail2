from markdown import markdown
from markdown.extensions.toc import TocExtension
from bs4 import BeautifulSoup
from premailer import transform


def main():
    # Read template.html to memory and convert to soup
    with open("template.html", "r") as f:
        template = f.read()
    template_soup = BeautifulSoup(template, "html.parser")

    # Read content.md file to memory.
    with open("content.md", "r") as f:
        content = f.read()

    # Convert markdown -> html -> soup
    content_html = markdown(content, extensions=['attr_list', TocExtension(title="Sisältö", toc_depth="2-6")])
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
    with open("output/viikkomaili.html", "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
        output_file.write(output_html)

if __name__ == '__main__':
    main()