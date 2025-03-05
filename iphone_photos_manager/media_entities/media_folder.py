"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 2025-03-04
"""

import datetime
from typing import List, Optional, Union

from iphone_photos_manager.media_entities.media_album import MediaAlbum


class MediaFolder:
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
        self.data: List[Union[MediaFolder, MediaAlbum]] = []

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __repr__(self):
        s = f"<{self.__class__.__name__}:{self.title} [{len(self)}]>"
        return s

    def add_data(self, data: Union["MediaFolder", MediaAlbum]):
        self.data.append(data)

    def view_structure(self, level: int = 0):
        """
        Prints a directory-like tree structure.
        """
        indent = " " * (level * 4)  # Indentation for hierarchy levels
        print(f"{indent}📂 {self.title}")  # Print folder name

        for item in self.data:
            if isinstance(item, MediaFolder):
                item.view_structure(level + 1)  # Recursive call for subfolders
            elif isinstance(item, MediaAlbum):
                print(f"{indent}    📖 {item.title}")

    def get_all_albums(self) -> List[MediaAlbum]:
        result = []
        for d in self:
            if isinstance(d, MediaAlbum):
                result.append(d)

            elif isinstance(d, MediaFolder):
                result.append(d.get_all_albums())

        return result


if __name__ == "__main__":
    pass
