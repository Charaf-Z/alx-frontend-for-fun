#!/usr/bin/python3
"""Markdown to HTML Converter."""

from re import findall, match, sub
from sys import argv, stderr
from os import path
from hashlib import md5


def handle_headers(func):
    """Decorate a function to handle Markdown headers."""

    def wrapper(line, _):
        """Converte Markdown headers to HTML."""
        header_level = match(r"^(#{1,6})([\w\s ]+?)$", line)
        if header_level:
            line = "<h{0}>{1}</h{0}>\n".format(
                len(header_level.group(1)), header_level.group(2).strip()
            )
        return func(line, _)

    return wrapper


# def handle_list(func):
#     """Decorate a function to handle Markdown lists."""
#
#     def wrapper(line, options):
#         """Converte Markdown lists to HTML."""
#         ordered_list = options.get("ordered_list", False)
#         unordered_list = options.get("unordered_list", False)
#         ordered_list_value = match(r"^\*([\w<>\/ ]+)$", line)
#         unordered_list_value = match(r"^\-([\w<>\/ ]+)$", line)
#
#         if not match(r"^([-*][\w<>\/ ]+|)$", line):
#             return func(line, options)
#
#         if not ordered_list and ordered_list_value:
#             line = "<ol>\n<li>{}</li>\n".format(line.strip("* \n"))
#             options["ordered_list"] = True
#             return func(line, options)
#         if len(line) == 1 and ordered_list:
#             line = "</ol>\n"
#             options["ordered_list"] = False
#             return func(line, options)
#
#         if not unordered_list and unordered_list_value:
#             line = "<ul>\n<li>{}</li>\n".format(line.strip("- \n"))
#             options["unordered_list"] = True
#             return func(line, options)
#         if len(line) == 1 and unordered_list:
#             line = "\n</ul>\n"
#             options["unordered_list"] = False
#             return func(line, options)
#
#         if unordered_list_value or ordered_list_value:
#             line = "<li>{}</li>\n".format(line.strip("*- \n"))
#         return func(line, options)
#
#     return wrapper


# def handle_paragraph(func):
#     """Decorate a function to handle Markdown paragraphs."""
#
#     def wrapper(line, options):
#         """Converte Markdown paragraphs to HTML."""
#         start_paragraph = options.get("paragraph", False)
#         line_length = len(line)
#         if not match(r"^(?!<\/?(?:h\d|ul|ol|li)>).*$", line):
#             return func(line, options)
#         if not start_paragraph and line_length > 1:
#             line = "<p>\n{}".format(line)
#             options["paragraph"] = True
#             return func(line, options)
#         if line_length == 1 and start_paragraph:
#             line = "</p>\n"
#             options["paragraph"] = False
#             return func(line, options)
#         if start_paragraph:
#             line = "<br />\n{}".format(line)
#         return func(line, options)
#
#     return wrapper


# def handle_typography(func):
#     """Decorate a function to handle Markdown typography."""
#
#     def wrapper(line, _):
#         """Convert Markdown typography to HTML."""
#         item_reg = r"(\*\*[\w\s]+?\*\*|__[\w\s]+?__)"
#         bold_reg = r"\*{2}([\w\s]+?)\*{2}"
#         for item in findall(item_reg, line):
#             if not match(item_reg, item):
#                 continue
#             line = line.rstrip("\n")
#             line = line.replace(
#                 item,
#                 "<{0}>{1}</{0}>".format(
#                     "b" if match(bold_reg, item) else "em",
#                     findall(item_reg, item)[0].strip("*_"),
#                 ),
#                 1,
#             )
#         return func(line, _)
#
#     return wrapper


# def convert_md5(func):
#     """Decorate a function to convert Markdown MD5 hashes."""
#
#     def wrapper(line, _):
#         """Convert Markdown MD5 hashes to hexadecimal."""
#         for item in findall(r"\[\[[\w\s]+?\]\]", line):
#             line = line.rstrip("\n")
#             line = line.replace(
#                 item,
#                 md5(
#                     findall(r"\[\[([\w\s]+?)\]\]", item)[0].encode()
#                 ).hexdigest(),
#                 1,
#             )
#         return func(line, _)
#
#     return wrapper


# def remove_c(func):
#     """Decorate a function to remove Markdown 'c' tags."""
#
#     def wrapper(line, _):
#         """Remove Markdown 'c' tags."""
#         for item in findall(r"\(\([\w\s]+?\)\)", line):
#             line = line.rstrip("\n")
#             line = line.replace(item, sub(r"[cC()]+", "", item), 1)
#         return func(line, _)
#
#     return wrapper


# @handle_typography
# @convert_md5
# @remove_c
@handle_headers
# @handle_list
# @handle_paragraph
def process_line(line, options=None):
    """Processe a Markdown line into HTML."""
    return line


if __name__ == "__main__":
    if len(argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=stderr)
        exit(1)

    if not path.isfile(argv[1]):
        print("Missing {}".format(argv[1]), file=stderr)
        exit(1)

    with open(argv[1]) as read:
        with open(argv[2], "w") as html:
            options = {
                "paragraph": False,
                "ordered_list": False,
                "unordered_list": False,
            }
            for line in read:
                line = process_line(line, options)
                if len(line) > 1:
                    html.write(line)
                # length = len(line)
                # headings = line.lstrip("#")
                # heading_num = length - len(headings)
                # if 1 <= heading_num <= 6:
                #     line = (
                #         "<h{}>".format(heading_num)
                #         + headings.strip()
                #         + "</h{}>\n".format(heading_num)
                #     )
                # if length > 1:
                #     html.write(line)
            if options.get("ordered_list"):
                html.write("</ol>")
            if options.get("unordered_list"):
                html.write("</ul>")
            if options.get("paragraph"):
                html.write("\n</p>")
    exit(0)
