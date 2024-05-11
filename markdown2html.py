#!/usr/bin/python3
"""Markdown to HTML Converter."""

from re import findall
from sys import argv, stderr
from os import path
from hashlib import md5


if __name__ == "__main__":
    if len(argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=stderr)
        exit(1)

    if not path.isfile(argv[1]):
        print("Missing {}".format(argv[1]), file=stderr)
        exit(1)

    with open(argv[1]) as read:
        with open(argv[2], "w") as html:
            start_ul, start_ol, pr = False, False, False
            for line in read:
                line = line.replace("**", "<b>", 1)
                line = line.replace("**", "</b>", 1)
                line = line.replace("__", "<em>", 1)
                line = line.replace("__", "</em>", 1)

                md5_item = findall(r"\[\[.+?\]\]", line)
                md5_inside = findall(r"\[\[(.+?)\]\]", line)
                if md5_item:
                    line = line.replace(
                        md5_item[0], md5(md5_inside[0].encode()).hexdigest()
                    )

                c_string = findall(r"\(\(.+?\)\)", line)
                c_content = findall(r"\(\((.+?)\)\)", line)
                if c_string:
                    c_content = "".join(
                        c for c in c_content[0] if c not in "Cc"
                    )
                    line = line.replace(c_string[0], c_content)

                length = len(line)
                header = line.lstrip("#")
                header_level = length - len(header)
                ul = line.lstrip("-")
                ul_nbr = length - len(ul)
                ol = line.lstrip("*")
                ol_nbr = length - len(ol)
                if 1 <= header_level <= 6:
                    line = (
                        "<h{}>".format(header_level)
                        + header.strip()
                        + "</h{}>\n".format(header_level)
                    )

                if ul_nbr:
                    if not start_ul:
                        html.write("<ul>\n")
                        start_ul = True
                    line = "<li>" + ul.strip() + "</li>\n"
                if start_ul and not ul_nbr:
                    html.write("</ul>\n")
                    start_ul = False

                if ol_nbr:
                    if not start_ol:
                        html.write("<ol>\n")
                        start_ol = True
                    line = "<li>" + ol.strip() + "</li>\n"
                if start_ol and not ol_nbr:
                    html.write("</ol>\n")
                    start_ol = False

                if not (header_level or start_ul or start_ol):
                    if not pr and length > 1:
                        html.write("<p>\n")
                        pr = True
                    elif length > 1:
                        html.write("<br/>\n")
                    elif pr:
                        html.write("</p>\n")
                        pr = False

                if length > 1:
                    html.write(line)

            if start_ul:
                html.write("</ul>\n")
            if start_ol:
                html.write("</ol>\n")
            if pr:
                html.write("</p>\n")
    exit(0)
