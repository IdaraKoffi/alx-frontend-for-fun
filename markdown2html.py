#!/usr/bin/python3
import sys
import hashlib


def apply_bold_emphasis(text):
    text = text.replace("**", "<b>", 1).replace("**", "</b>", 1)
    text = text.replace("__", "<em>", 1).replace("__", "</em>", 1)
    return text


def apply_special_syntax(text):
    start = text.find("[[")
    end = text.find("]]", start)
    if start != -1 and end != -1:
        to_hash = text[start + 2:end]
        hashed = hashlib.md5(to_hash.encode()).hexdigest()
        text = text.replace(f"[[{to_hash}]]", hashed)

    start = text.find("((")
    end = text.find("))", start)
    if start != -1 and end != -1:
        to_remove_c = text[start + 2:end]
        cleaned = to_remove_c.replace('c', '').replace('C', '')
        text = text.replace(f"(({to_remove_c}))", cleaned)

    return text


if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        exit(1)

    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    try:
        with open(markdown_file, 'r') as f:
            markdown_lines = f.readlines()
    except FileNotFoundError:
        print(f"Missing {markdown_file}", file=sys.stderr)
        exit(1)

    html_content = []
    in_list = None
    paragraph = []

    for line in markdown_lines:
        line = line.strip()

        if line.startswith("#"):
            if in_list:
                html_content.append(f"</{in_list}>")
                in_list = None
            if paragraph:
                html_content.append(f"<p>{'<br/>'.join(paragraph)}</p>")
                paragraph = []
            level = len(line.split(' ')[0])
            if 1 <= level <= 6:
                content = line[level + 1:].strip()
                html_content.append(f"<h{level}>{content}</h{level}>")
        elif line.startswith('- '):
            if in_list != "ul":
                if in_list:
                    html_content.append(f"</{in_list}>")
                html_content.append("<ul>")
                in_list = "ul"
            content = line[2:].strip()
            html_content.append(f"<li>{content}</li>")
        elif line.startswith('* '):
            if in_list != "ol":
                if in_list:
                    html_content.append(f"</{in_list}>")
                html_content.append("<ol>")
                in_list = "ol"
            content = line[2:].strip()
            html_content.append(f"<li>{content}</li>")
        else:
            if in_list:
                html_content.append(f"</{in_list}>")
                in_list = None
            if line:
                paragraph.append(line)
            elif paragraph:
                html_content.append(f"<p>{'<br/>'.join(paragraph)}</p>")
                paragraph = []

    if in_list:
        html_content.append(f"</{in_list}>")
    if paragraph:
        html_content.append(f"<p>{'<br/>'.join(paragraph)}</p>")

    for i in range(len(html_content)):
        html_content[i] = apply_bold_emphasis(html_content[i])
        html_content[i] = apply_special_syntax(html_content[i])

    try:
        with open(html_file, 'w') as f:
            for line in html_content:
                f.write(line + "\n")
    except IOError:
        print(f"Could not write to file {html_file}", file=sys.stderr)
        exit(1)

    exit(0)

