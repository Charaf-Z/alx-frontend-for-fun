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
            ul, ol, p = False, False, False
            for line in read:
                line = line.replace("**", "<b>", 1)
                line = line.replace("**", "</b>", 1)
                line = line.replace("__", "<em>", 1)
                line = line.replace("__", "</em>", 1)

                md5_item = findall(r"\[\[.+?\]\]", line)
                md5_inside = findall(r"\[\[(.+?)\]\]", line)
                if md5:
                    line = line.replace(
                        md5_item[0], md5(md5_inside[0].encode()).hexdigest()
                    )

                remove_c = findall(r"\(\(.+?\)\)", line)
                remove_c_inside = findall(r"\(\((.+?)\)\)", line)
                if remove_c:
                    remove_c_inside = "".join(
                        c for c in remove_c_inside[0] if c not in "Cc"
                    )
                    line = line.replace(remove_c[0], remove_c_inside)

                length = len(line)
                header = line.lstrip("#")
                header_level = length - len(header)
                if 1 <= header_level <= 6:
                    line = "<h{0}>{1}</h{0}>\n".format(
                        header_level, header.strip()
                    )

                ul_li = line.lstrip("-")
                ul_nbr = length - len(ul_li)
                if ul_nbr:
                    if not ul:
                        html.write("<ul>\n")
                        ul = True
                    line = "<li>{}</li>\n".format(ul_li.strip())
                if ul and not ul_nbr:
                    html.write("</ul>\n")
                    ul = False

                ol_li = line.lstrip("*")
                ol_nbr = length - len(ol_li)
                if ol_nbr:
                    if not ol:
                        html.write("<ol>\n")
                        ol = True
                    line = "<li>{}</li>".format(ol_li.strip())
                if ol and not ol_nbr:
                    html.write("</ol>\n")
                    ol = False

                if not (header_level or ol or ul):
                    if not p and length > 1:
                        html.write("<p>\n")
                        p = True
                    elif length > 1:
                        html.write("<br/>\n")
                    elif p:
                        html.write("</p>\n")
                        p = False

                if length > 1:
                    html.write(line)

            if ul:
                html.write("</ul>\n")
            if ol:
                html.write("</ol>\n")
            if p:
                html.write("</p>\n")

    exit(0)
