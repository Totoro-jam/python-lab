"""pylab02 — collections, itertools, functools 实战。"""

from .containers import top_n_words, group_by_key, sliding_window
from .lazy_stream import stream_large_file, chunked

__all__ = [
    "top_n_words",
    "group_by_key",
    "sliding_window",
    "stream_large_file",
    "chunked",
]
