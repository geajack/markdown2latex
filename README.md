# markdown2latex

This is a script to convert markdown files to LaTeX. The use case for me is that I like to type up math in [Typora](https://typora.io/), but then it needs to be converted to LaTeX so that the final PDF looks the way people expect it to look. So this script should handle markdown written in Typora fine.

Currently supports headings, bold and italics, and inline and displayed math. **This script assumes that displayed math is wrapped in `$$`**, which I believe is not the default in Typora.

Usage: pipe the markdown into stdin. The LaTeX is in stdout. i.e.:

```
$ cat paper.md | markdown2latex > paper.tex
```

To install this script:

```
$ pip install git+https://github.com/geajack/markdown2latex.git
```

This script relies on the [marko](https://github.com/frostming/marko) library.