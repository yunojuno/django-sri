import os.path
from typing import Optional

from django import template
from django.templatetags.static import static
from django.utils.safestring import mark_safe

from sri.utils import (
    DEFAULT_ALGORITHM,
    USE_SRI,
    Algorithm,
    attrs_to_str,
    calculate_integrity_of_static,
)

register = template.Library()


def sri_js(attrs: dict, path: str, algorithm: Algorithm):
    attrs.update({"type": "text/javascript", "src": static(path)})
    return mark_safe(f"<script {attrs_to_str(attrs)}></script>")


def sri_css(attrs: dict, path: str, algorithm: Algorithm):
    attrs.update({"rel": "stylesheet", "type": "text/css", "href": static(path)})
    return mark_safe(f"<link {attrs_to_str(attrs)}/>")


EXTENSIONS = {"js": sri_js, "css": sri_css}


@register.simple_tag
def sri_static(path: str, algorithm: Optional[str] = None):
    algorithm_type = Algorithm(algorithm or DEFAULT_ALGORITHM)
    extension = os.path.splitext(path)[1][1:]
    sri_method = EXTENSIONS[extension]
    attrs = {}
    if USE_SRI:
        attrs.update(
            {
                "integrity": calculate_integrity_of_static(path, algorithm_type),
                "crossorigin": "anonymous",
            }
        )
    return sri_method(attrs, path, algorithm_type)


@register.simple_tag
def sri_integrity_static(path: str, algorithm: Optional[str] = None):
    return calculate_integrity_of_static(
        path, Algorithm(algorithm or DEFAULT_ALGORITHM)
    )
