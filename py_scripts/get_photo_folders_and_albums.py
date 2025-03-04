import pathlib
import sqlite3
import datetime
from typing import List, Dict, Optional
from pprint import pp

def get_all_col_in_z_generic_album(photos_sqlite_file: pathlib.Path) -> List[str]:
    """
    get all columns in ZGENERICALBUM
    :return:
    """

class PhotoAlbum:
    def __init__(self, title: str, uuid: str, creation_date: Optional[str]):
        self.title = title
        self.uuid = uuid
        self.creation_date = creation_date

class PhotoFolder:
    def __init__(self, title: str, uuid: str, creation_date: Optional[str]):
        self.title = title
        self.uuid = uuid
        self.creation_date = creation_date
        self.photo_albums: List[PhotoAlbum] = []

def convert_apple_timestamp(timestamp: Optional[float]) -> Optional[str]:
    """Convert Apple's Core Data timestamp to human-readable format."""
    if timestamp:
        return (datetime.datetime(2001, 1, 1) + datetime.timedelta(seconds=timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    return None

def get_folders_and_albums_structure(photos_sqlite_file: pathlib.Path) -> Dict:
    """
    Extracts folder and album structure from iOS Photos.sqlite database.

    :param photos_sqlite_file: Path to the Photos.sqlite database.
    :return: Dictionary with folders and standalone albums.
    """
    assert photos_sqlite_file.is_file(), f"Error: Database file {photos_sqlite_file} not found."

    with sqlite3.connect(photos_sqlite_file) as conn:
        cursor = conn.cursor()

        # Fetch all albums and folders
        cursor.execute("""
            SELECT ZTITLE, ZUUID, ZPARENTFOLDER, ZCREATIONDATE, ZKIND
            FROM ZGENERICALBUM
            WHERE ZTITLE IS NOT NULL
        """)
        records = cursor.fetchall()

    folders = {}
    standalone_albums = []

    # First pass: Create album and folder objects
    for title, uuid, parent_uuid, creation_timestamp, kind in records:
        creation_date = convert_apple_timestamp(creation_timestamp)

        print(title, uuid, parent_uuid, creation_timestamp, kind)

        # if kind == 3:  # Folder
        #     folders[uuid] = PhotoFolder(title, uuid, creation_date)
        # elif kind == 2:  # Album
        #     album = PhotoAlbum(title, uuid, creation_date)
        #     if parent_uuid in folders:
        #         folders[parent_uuid].photo_albums.append(album)
        #     else:
        #         standalone_albums.append(album)

    return {
        "folders": list(folders.values()),
        "albums": standalone_albums,
    }

if __name__ == '__main__':
    IFUSE_MOUNT_DIR = pathlib.Path("~/my_home/ifuse_iphone_link").expanduser()
    PHOTOS_SQLITE_FILE = IFUSE_MOUNT_DIR / "PhotoData" / "Photos.sqlite"

    structure = get_folders_and_albums_structure(PHOTOS_SQLITE_FILE)
    # # Output or process the structure as needed
    # pp(structure)