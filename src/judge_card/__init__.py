__all__ = ["generate", "validate", "markdown", "html"]

def __getattr__(name):
    if name == "generate":
        from .generator import generate
        return generate
    if name == "validate":
        from .schema import validate
        return validate
    if name == "markdown":
        from .render import markdown
        return markdown
    if name == "html":
        from .render import html
        return html
    raise AttributeError(name)
