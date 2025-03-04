"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 2025-03-04
"""
# >>> Dynamic Changing `sys.path` in Runtime by Adding Project Directory to Path >>>
import pathlib
import sys

THIS_FILE_PATH = pathlib.Path(__file__).absolute()
THIS_FILE_PARENT_DIR = THIS_FILE_PATH.parent
PROJECT_DIR = THIS_FILE_PARENT_DIR.parent.parent
sys.path.append(str(PROJECT_DIR))
print(f"[*INFO*] - append directory to path: {PROJECT_DIR}")
# <<< Dynamic Changing `sys.path` in Runtime by Adding Project Directory to Path <<<

import pathlib
from pprint import pp

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

    # folders_and_albums = psc.get_user_created_folders_and_albums()
    # folders = folders_and_albums["folders"]
    # for folder in folders:
    #     folder.view_structure()

    psc.view_user_created_folders_and_albums()