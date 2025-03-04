"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 2025-03-04
"""

import datetime
from typing import Optional


class PhotoAlbum:
    def __init__(self, title: str, uuid: str, pk_in_z_generic_album: Optional[int] = None,
        created_datetime: Optional[datetime.datetime] = None,):
        self.title = title
        self.uuid = uuid
        self.pk_in_z_generic_album = pk_in_z_generic_album
        self.created_datetime = created_datetime

    def __repr__(self):
        s = f"<{self.__class__.__name__}:{self.title}>"
        return s
