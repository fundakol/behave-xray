import pluggy

from .formatter import XrayCloudFormatter, XrayFormatter  # noqa: F401


hookimpl = pluggy.HookimplMarker('xray')
