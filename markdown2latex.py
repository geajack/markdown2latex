import marko
import marko.block
import marko.inline as inline

import re

FENCE = "\\$\\$"
class Formula(marko.block.BlockElement):
    priority = 8
    pattern = re.compile("\\$\\$", re.M)

    def __init__(self, match):
        self.children = [inline.RawText(match)]

    @classmethod
    def match(cls, source):
        m = source.expect_re("\\$\\$")
        return m

    @classmethod
    def parse(cls, source):
        source.next_line()
        source.consume()
        lines = []
        while not source.exhausted:
            line = source.next_line()
            if line is None:
                break
            source.consume()
            m = re.match("\\$\\$", line)
            if m:
                break
            lines.append(line)
        return "".join(lines)

class Renderer:

    def render_document(self, element):
        preamble = r"""
        \documentclass[10pt,a4paper]{article}
        \usepackage{amsmath}
        \usepackage{amsfonts}
        \usepackage{amssymb}

        \begin{document}
        """
        return preamble + self.render_children(element) + "\n\\end{document}"
    
    def render_paragraph(self, element):
        return self.render_children(element) + "\n\n"

    def render_heading(self, element):
        heading_level = element.level
        if heading_level == 1:
            tag = "section"
        elif heading_level == 2:
            tag = "subsection"
        elif heading_level == 3:
            tag = "subsubsection"
        return f"\{tag}{{" + self.render_children(element) + "}\n\n"

    def render_strong_emphasis(self, element):
        return "\\textbf{" + self.render_children(element) + "}"

    def render_emphasis(self, element):
        return "\\textit{" + self.render_children(element) + "}"

    def render_formula(self, element):
        return "\\begin{equation*}\n" + self.render_children(element) + "\\end{equation*}\n\n"

class Extension:
    elements=[Formula]
    renderer_mixins = [Renderer]

markdown = marko.Markdown(extensions=[Extension])
with open("examples/input.md") as file:
    text = file.read()
    html = markdown.convert(text)
    print(html)