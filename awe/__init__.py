import os

from . import resources

try:
    from .api import Page  # noqa
    from .decorators import inject  # noqa
    from .view import CustomElement
    from .chart import Chart as _Chart
except ImportError:
    if not os.environ.get('AWE_BUILD'):
        raise
    Page = None
    inject = None
    CustomElement = None
    _Chart = None

__version__ = resources.get('VERSION')
