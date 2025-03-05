"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 2025-03-04
"""

import datetime
import pathlib
from typing import List, Optional

from iphone_photos_manager.media_entities.media_asset import MediaAsset


class MediaAlbum:
    CLS_EMOJI = "📖"

    def __init__(
        self,
        title: str,
        uuid: str,
        pk_in_z_generic_album: Optional[int] = None,
        created_datetime: Optional[datetime.datetime] = None,
        media_asset_data: Optional[List[MediaAsset]] = None,
    ):
        self.title = title
        self.uuid = uuid
        self.pk_in_z_generic_album = pk_in_z_generic_album
        self.created_datetime = created_datetime

        if media_asset_data is None:
            media_asset_data = []
        self.media_asset_data = media_asset_data

    def __len__(self):
        return len(self.media_asset_data)

    def __iter__(self):
        return iter(self.media_asset_data)

    def __repr__(self):
        s = f"<{self.__class__.__name__}:{self.title} [{len(self)}]>"
        return s

    def view_info(self):
        print(f"{self.CLS_EMOJI} {self.title} [{len(self)}]")

    def view_assets_info(self):
        if len(self) == 0:
            msg = f"[*INFO*] - {self.CLS_EMOJI} {self.title} has 0 media asset\n"
            print(msg)
            return

        msg = f"[*INFO*] - {self.title} assets info:"
        print(msg)
        for ma in self:
            ma.view_info()
        print()

    def add_media_asset(self, media_asset: MediaAsset):
        self.media_asset_data.append(media_asset)

    def export(self, export_root_dir:pathlib.Path):
        """
        in the end there will be a dir path like:

        export_root_dir / self.title

        :param export_root_dir:
        :return:
        """
        dest_dir = export_root_dir / self.title
        dest_dir.mkdir(parents=True, exist_ok=True)

        for ma in self:
            ma:MediaAsset
            ma.export_to_dir(dest_dir)
