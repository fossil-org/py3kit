def render(obj):
    from .checks import is_renderable
    if is_renderable(obj):
        return obj.__render__()
    else:
        from ..errors import RenderingError

        raise RenderingError(f"Cannot render object {obj}")