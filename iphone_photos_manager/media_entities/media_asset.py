"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 2025-03-05
"""

import datetime
import pathlib
import shutil
from typing import ClassVar, List, Optional


class MediaAsset:
    VIDEO_TYPE_LS: ClassVar[List[str]] = [
        "public.mpeg-4",
        "com.apple.quicktime-movie",
    ]

    IMAGE_TYPE_LS: ClassVar[List[str]] = [
        "public.jpeg",
        "public.heic",
        "public.png",
        "public.heif",
        "org.webmproject.webp",
    ]

    def __init__(
        self,
        filename: str,
        file_path: Optional[pathlib.Path],
        uuid: str,
        album_id: int,
        width: Optional[int],
        height: Optional[int],
        orientation: Optional[int],
        file_size: Optional[int],
        is_favorite: bool,
        latitude: Optional[float],
        longitude: Optional[float],
        location_data: Optional[str],
        media_type: str,  # "image" or "video"
        duration: Optional[float] = None,  # Video duration
        pk_in_z_asset_album: Optional[int] = None,
        created_datetime: Optional[datetime.datetime] = None,
        modified_datetime: Optional[datetime.datetime] = None,
    ):
        self.filename = filename
        self.file_path = file_path
        self.uuid = uuid
        self.album_id = album_id
        self.width = width
        self.height = height
        self.orientation = orientation
        self.file_size = file_size
        self.is_favorite = is_favorite
        self.latitude = latitude
        self.longitude = longitude
        self.location_data = location_data
        self.media_type = media_type
        self.duration = duration
        self.pk_in_z_asset_album = pk_in_z_asset_album
        self.created_datetime = created_datetime
        self.modified_datetime = modified_datetime

        self.media_emoji = ""

        if self.media_type in MediaAsset.VIDEO_TYPE_LS:
            self.media_emoji = "🎞️"
        elif self.media_type in MediaAsset.IMAGE_TYPE_LS:
            self.media_emoji = "🖼️"
        else:
            msg = (
                f"[*WARN*] - media asset: {self.filename}, path: {self.file_path}, "
                f"is a unknown type of media: {self.media_type}, please check"
            )
            print(msg)
            self.media_emoji = "❓"

    def __repr__(self):
        return f"<MediaAsset {self.media_emoji} {self.filename}>"

    def view_info(self):
        print(f"{self.media_emoji} {self.filename} : {self.file_path}")

    def export(self, export_path: pathlib.Path):
        if isinstance(self.file_path, pathlib.Path):
            shutil.copy(self.file_path, export_path)

    def export_to_dir(self, export_dir: pathlib.Path, mkdir=True):
        if mkdir:
            export_dir.mkdir(parents=True, exist_ok=True)

        dest_path = export_dir / self.filename
        self.export(dest_path)
