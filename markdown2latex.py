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
    pattern = re.compile("\\$\\$", re.MULTILINE)

    def __init__(self, match):
        self.children = [marko.inline.RawText(match)]

    @classmethod
    def match(cls, source):
        match = source.expect_re("\\$\\$")
        return match

    @classmethod
    def parse(cls, source):
        source.next_line()
        source.consume()
        lines = []
        while not source.exhausted:
            line = source.next_line()
            if line != "$$":
                lines.append(line)
            source.consume()
        return "".join(lines)

class ExampleBlock(marko.block.BlockElement):
    priority = 8
    pattern = re.compile(r"( {,3})(`{3,}|~{3,})[^\n\S]*(.*?)$", re.M)
    _parse_info = ("", "", "", "")  # type: Tuple[str, str, str, str]

    def __init__(self, match):  # type: (Tuple[str, str, str]) -> None
        self.lang = marko.inline.Literal.strip_backslash(match[0])
        self.extra = match[1]
        self.children = [marko.inline.RawText(match[2])]

    @classmethod
    def match(cls, source):  # type: (Source) -> Optional[Match]
        m = source.expect_re(cls.pattern)
        if not m:
            return None
        prefix, leading, info = m.groups()
        if leading[0] == "`" and "`" in info:
            return None
        lang, extra = (info.split(None, 1) + [""] * 2)[:2]
        cls._parse_info = prefix, leading, lang, extra
        return m

    @classmethod
    def parse(cls, source):  # type: (Source) -> Tuple[str, str, str]
        source.next_line()
        source.consume()
        lines = []
        while not source.exhausted:
            line = source.next_line()
            if line is None:
                break
            source.consume()
            m = re.match(r" {,3}(~+|`+)[^\n\S]*$", line, flags=re.M)
            if m and cls._parse_info[1] in m.group(1):
                break

            prefix_len = source.match_prefix(cls._parse_info[0], line)
            if prefix_len >= 0:
                line = line[prefix_len:]
            else:
                line = line.lstrip()
            lines.append(line)
        return cls._parse_info[2], cls._parse_info[3], "".join(lines)

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
        return "HI" + "\n\n"

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