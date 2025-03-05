"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 2025-03-04
"""

import datetime
from typing import Optional


class MediaAlbum:
    def __init__(
        self,
        title: str,
        uuid: str,
        pk_in_z_generic_album: Optional[int] = None,
        created_datetime: Optional[datetime.datetime] = None,
        photo_count: Optional[int] = None,
    ):
        self.title = title
        self.uuid = uuid
        self.pk_in_z_generic_album = pk_in_z_generic_album
        self.created_datetime = created_datetime
        self.photo_count = photo_count

    def __repr__(self):
        s = f"<{self.__class__.__name__}:{self.title} [{self.photo_count}]>"
        return s

    def view_info(self):
        print(f"📖 {self.title}")
