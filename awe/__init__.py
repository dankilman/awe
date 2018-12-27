import os

from . import resources

try:
    from .api import Page  # noqa
    from .decorators import inject  # noqa
except ImportError:
    if not os.environ.get('AWE_BUILD'):
        raise
    Page = None
    inject = None

__version__ = resources.get('VERSION')
