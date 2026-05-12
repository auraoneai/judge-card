__all__ = ["generate", "validate"]

def __getattr__(name):
    if name == "generate":
        from .generator import generate
        return generate
    if name == "validate":
        from .schema import validate
        return validate
    raise AttributeError(name)
