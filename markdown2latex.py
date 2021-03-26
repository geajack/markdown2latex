import marko
import marko.block
import marko.inline as inline

import re

class Formula(marko.block.BlockElement):
    priority = 8
    pattern = re.compile(r"( {,3})(`{3,}|~{3,})[^\n\S]*(.*?)$", re.M)
    _parse_info = ("", "", "", "")  # type: Tuple[str, str, str, str]

    def __init__(self, match):  # type: (Tuple[str, str, str]) -> None
        self.lang = inline.Literal.strip_backslash(match[0])
        self.extra = match[1]
        self.children = [inline.RawText(match[2])]

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
        return "FORMULA"

class Extension:
    elements=[Formula]
    renderer_mixins = [Renderer]

markdown = marko.Markdown(extensions=[Extension])
with open("examples/input.md") as file:
    text = file.read()
    html = markdown.convert(text)
    print(html)