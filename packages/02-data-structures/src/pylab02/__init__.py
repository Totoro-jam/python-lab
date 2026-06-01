"""pylab02 — collections, itertools, functools 实战。"""

from .containers import group_by_key, sliding_window, top_n_words
from .lazy_stream import chunked, stream_large_file

__all__ = [
    "top_n_words",
    "group_by_key",
    "sliding_window",
    "stream_large_file",
    "chunked",
]
