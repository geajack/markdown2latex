import marko

class Renderer:
    
    def render_emphasis(self, element):
        return "<test>" + self.render_children(element) + "</test>"

class Extension:
    renderer_mixins = [Renderer]

markdown = marko.Markdown(extensions=[Extension])
with open("examples/input.md") as file:
    text = file.read()
    html = markdown.convert(text)
    print(html)