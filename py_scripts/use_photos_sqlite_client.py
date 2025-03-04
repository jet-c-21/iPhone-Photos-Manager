"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 2025-03-04
"""

import pathlib

from iphone_photos_manager import PhotosSqliteClient

IFUSE_MOUNT_DIR = pathlib.Path("~/my_home/ifuse_iphone_link").expanduser()
PHOTOS_DB_FILE = IFUSE_MOUNT_DIR / "PhotoData" / "Photos.sqlite"


if __name__ == "__main__":
    psc = PhotosSqliteClient(PHOTOS_DB_FILE)

    table_name_ls = psc.get_table_name_ls()
    for table_name in table_name_ls:
        if "album" in table_name.lower() or "folder" in table_name.lower():
            # print(table_name)
            pass

    col_name_ls = psc.get_col_name_ls_of_table("ZGENERICALBUM")
    for col_name in col_name_ls:
        # print(col_name)
        pass

    folders_and_albums = psc.get_folders_and_albums()
