"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 2025-03-04
"""
import pathlib
import sqlite3
import datetime

IFUSE_MOUNT_DIR = pathlib.Path("~/my_home/ifuse_iphone_link").expanduser()
PHOTOS_DB_FILE = IFUSE_MOUNT_DIR / "PhotoData" / "Photos.sqlite"

def convert_apple_timestamp(timestamp):
    """Convert Apple's Core Data timestamp to human-readable format."""
    if timestamp and timestamp > 0:  # Ensure timestamp is valid
        return (datetime.datetime(2001, 1, 1) + datetime.timedelta(seconds=timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    return "Unknown"

def fetch_album_metadata():
    assert IFUSE_MOUNT_DIR.is_dir(), f"Error: Mount directory {IFUSE_MOUNT_DIR} does not exist."
    assert PHOTOS_DB_FILE.is_file(), f"Error: Database file {PHOTOS_DB_FILE} not found."

    with sqlite3.connect(PHOTOS_DB_FILE) as conn:
        cursor = conn.cursor()

        # Fetch album metadata with explicit sorting
        cursor.execute("""
            SELECT ZTITLE, ZUUID, ZCREATIONDATE, ZCACHEDCOUNT
            FROM ZGENERICALBUM
            WHERE ZTITLE IS NOT NULL
            ORDER BY IFNULL(ZCREATIONDATE, 0) DESC, ZUUID ASC
        """)
        albums = cursor.fetchall()

        if not albums:
            print("\nNo albums found.")
            return

        print("\n📂 Albums Found:")
        print(f"{'Title':<40} | {'UUID':<36} | {'Created':<19} | {'Items'}")
        print("-" * 110)

        for title, uuid, creation_timestamp, cached_count in albums:
            # Filter out system-generated albums
            if title.lower().startswith(("progress-", "sync", "import")):
                continue

            creation_date = convert_apple_timestamp(creation_timestamp)
            uuid = uuid if uuid else "N/A"
            cached_count = cached_count if cached_count is not None else 0  # Default to 0 if NULL

            print(f"{title[:38]:<40} | {uuid:<36} | {creation_date:<19} | {cached_count}")

class PhotoAlbum:
    pass

class PhotoFolder:
    def __init__(self):
        self.photo_albums: List[PhotoAlbum] = [PhotoAlbum()]



def get_folders_and_albums_structure():
    """
    in iphone we can create folders and there will be albums inside the folders

    the fetch_album_metadata() is just a toy function, i think we can forget it

    but in the console we get before D App is actually a folder and there are several albums inside it

    try to create a dict with the structure

    {
        "folders": {
            "D App" :
        }
    }

    :return:
    """

if __name__ == '__main__':
    fetch_album_metadata()
