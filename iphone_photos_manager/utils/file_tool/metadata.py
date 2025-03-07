"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 2025-03-05
"""

import pathlib

from pymediainfo import MediaInfo


def get_media_info(media_file_path: pathlib.Path) -> MediaInfo:
    return MediaInfo.parse(media_file_path)
