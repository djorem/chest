"""Blueprint for the root path."""

from markdown2 import markdown

from flask import Blueprint

bp = Blueprint('index', __name__, url_prefix='/')


@bp.route('/')
def index():
    """Returns the contents of the README.md file"""
    return markdown(
        open("README.md", "r").read(), extras=["tables", "fenced-code-blocks"]
    )
