"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 2025-03-05
"""
import datetime
import pathlib
from typing import Optional


class Photo:
    def __init__(self,
                filename:str,
                file_path:pathlib.Path,
                uuid,
                width,
                height,
                orientation,
                file_size,
                is_favorite:bool,
                latitude,
                longitude,
                location_data,
                pk_in_z_asset_album: Optional[int] = None,
                created_datetime:Optional[datetime.datetime]=None,
                modified_datetime:Optional[datetime.datetime]=None,
                ):
        pass
