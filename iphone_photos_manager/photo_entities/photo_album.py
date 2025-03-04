"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 2025-03-04
"""

import datetime
from typing import Optional


class PhotoAlbum:
    def __init__(self, title: str, uuid: str, created_datetime: Optional[datetime.datetime]):
        self.title = title
        self.uuid = uuid
        self.created_datetime = created_datetime
