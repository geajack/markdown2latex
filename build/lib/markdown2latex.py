import marko
import marko.block
import marko.inline
from marko.md_renderer import MarkdownRenderer

from sys import stdin
import re
class BlockFormula(marko.block.BlockElement):
    pattern = re.compile(r"\$\$ *\n([\s\S]+?)^\$\$ *$", re.MULTILINE)

    def __init__(self, match):
        self.children = [marko.inline.RawText(match.group(1))]

    @classmethod
    def match(cls, source):
        return source.expect_re(cls.pattern)

    @classmethod
    def parse(cls, source):
        match = source.match
        source.consume()
        return match

class Paragraph(marko.block.Paragraph):
    override = True

    @classmethod
    def break_paragraph(cls, source, lazy=False):
        if BlockFormula.match(source):
            return True
        return super().break_paragraph(source, lazy=lazy)


class Renderer:
    
    def render_document(self, element):
        preamble = \
r"""\documentclass[10pt,a4paper]{article}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{float}
\usepackage[bookmarks]{hyperref}

\begin{document}
"""
        return preamble + "\n" + self.render_children(element).strip() + "\n\n\\end{document}"
    
    def render_paragraph(self, element):
        return self.render_children(element) + "\n"

    def render_heading(self, element):
        heading_level = element.level
        if heading_level == 1:
            return \
r"""\title{""" + self.render_children(element) + r"""}
\maketitle
"""
        else:
            if heading_level == 2:
                tag = "section"
            elif heading_level == 3:
                tag = "subsection"
            else:
                tag = "subsubsection"
            return f"\{tag}{{" + self.render_children(element) + "}\n"

    def render_strong_emphasis(self, element):
        return "\\textbf{" + self.render_children(element) + "}"

    def render_emphasis(self, element):
        return "\\textit{" + self.render_children(element) + "}"

    def render_block_formula(self, element):
        return "\n\\begin{equation*}\n" + self.render_children(element) + "\\end{equation*}\n"

    def render_list(self, element):
        if element.ordered:
            tag = "enumerate"
        else:
            tag = "itemize"
        
        return f"\\begin{{{tag}}}\n\n" + self.render_children(element) + f"\\end{{{tag}}}\n"

    def render_list_item(self, element):
        return "\item " + self.render_children(element) + "\n"

    def render_image(self, element):
        return f"""
\\begin{{figure}}[H]
\\includegraphics[width=\linewidth]{{{element.dest}}}
\\caption{{This is an image.}}
\\end{{figure}}
"""

class Extension:
    elements = [BlockFormula, Paragraph]
    renderer_mixins = [Renderer]

def main():
    markdown = marko.Markdown(renderer=MarkdownRenderer, extensions=[Extension])
    text = stdin.read()
    output = markdown.convert(text)
    print(output)

if __name__ == "__main__":
    main()