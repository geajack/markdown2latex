import marko
import marko.block
import marko.inline

import re
from sys import stdin

class InlineFormula(marko.inline.InlineElement):
    pattern = re.compile("\\$\\$(.*?)\\$\\$", re.MULTILINE)
    parse_children = False

    def __init__(self, match):
        self.content = match.group(1)

class BlockFormula(marko.block.BlockElement):
    def __init__(self, match):
        self.children = [marko.inline.RawText(match)]

    @classmethod
    def match(cls, source):
        pattern = re.compile("\\$\\$.*?$", re.M)
        match = source.expect_re(pattern)
        return match

    @classmethod
    def parse(cls, source):
        source.next_line()
        source.consume()
        lines = []
        while not source.exhausted:
            line = source.next_line()
            source.consume()
            if line.strip() == "$$":
                break
            lines.append(line)
        return "".join(lines)

class ExampleBlock(marko.block.BlockElement):
    priority = 8

    def __init__(self, match):  # type: (Tuple[str, str, str]) -> None
        self.children = [marko.inline.RawText(match)]

    @classmethod
    def match(cls, source):  # type: (Source) -> Optional[Match]
        pattern = re.compile(r"```.*?$", re.M)
        match = source.expect_re(pattern)
        return match

    @classmethod
    def parse(cls, source):  # type: (Source) -> Tuple[str, str, str]
        source.next_line()
        source.consume()
        lines = []
        while not source.exhausted:
            line = source.next_line()
            source.consume()
            if line.strip() == "```":
                break
            lines.append(line)
        return "".join(lines)

class Renderer:

    def render_document(self, element):
#         preamble = \
# r"""\documentclass[10pt,a4paper]{article}
# \usepackage{amsmath}
# \usepackage{amsfonts}
# \usepackage{amssymb}

# \begin{document}
# """
#         return preamble + "\n" + self.render_children(element) + "\\end{document}"
        return self.render_children(element)
    
    def render_paragraph(self, element):
        return self.render_children(element) + "\n\n"

    def render_example_block(self, element):
        return "[" + self.render_children(element) + "]\n"

    # def render_heading(self, element):
    #     heading_level = element.level
    #     if heading_level == 1:
    #         tag = "section"
    #     elif heading_level == 2:
    #         tag = "subsection"
    #     elif heading_level == 3:
    #         tag = "subsubsection"
    #     return f"\{tag}{{" + self.render_children(element) + "}\n\n"

    # def render_strong_emphasis(self, element):
    #     return "\\textbf{" + self.render_children(element) + "}"

    # def render_emphasis(self, element):
    #     return "\\textit{" + self.render_children(element) + "}"

    def render_inline_formula(self, element):
        return f"<INLINE FORMULA ({element.content})>"

    def render_block_formula(self, element):
        return "\\begin{equation*}\n" + self.render_children(element) + "\\end{equation*}\n\n"

class Extension:
    elements=[BlockFormula, InlineFormula, ExampleBlock]
    renderer_mixins = [Renderer]

markdown = marko.Markdown(extensions=[Extension])
text = stdin.read()
output = markdown.convert(text)
print(output)