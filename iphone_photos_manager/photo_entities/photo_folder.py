"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 2025-03-04
"""

import datetime
from typing import List, Optional, Union

from iphone_photos_manager.photo_entities.photo_album import PhotoAlbum


class PhotoFolder:
    def __init__(
        self,
        title: str,
        uuid: str,
        pk_in_z_generic_album: Optional[int] = None,
        created_datetime: Optional[datetime.datetime] = None,
    ):
        self.title = title
        self.uuid = uuid
        self.pk_in_z_generic_album = pk_in_z_generic_album
        self.created_datetime = created_datetime
        self.data: List[Union[PhotoFolder, PhotoAlbum]] = []

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        s = f"<{self.__class__.__name__}:{self.title} [{len(self)}]>"
        return s

    def add_data(self, data: Union["PhotoFolder", PhotoAlbum]):
        self.data.append(data)
