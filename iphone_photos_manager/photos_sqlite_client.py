"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 2025-03-04
"""
import pathlib
import sqlite3
from typing import Dict, List, Union

from iphone_photos_manager.photo_entities import PhotoAlbum, PhotoFolder


class PhotosSqliteClient:
    def __init__(self, photos_sqlite_path: pathlib.Path):
        self.photos_sqlite_path = photos_sqlite_path
        assert self.photos_sqlite_path.is_file(), f"{self.photos_sqlite_path} is not a file"

        # Persistent connection
        self.conn = sqlite3.connect(self.photos_sqlite_path)
        self.cursor = self.conn.cursor()

    def __del__(self):
        """Ensure the connection is closed properly."""
        if hasattr(self, "conn") and self.conn:
            self.conn.close()

    def __enter__(self):
        """Enable usage with 'with' statement."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Ensure proper cleanup when exiting the context."""
        if self.conn:
            self.conn.close()

    def get_table_name_ls(self) -> List[str]:
        """Retrieve a list of all table names in the database."""
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        self.cursor.execute(query)
        return [row[0] for row in self.cursor.fetchall()]

    def get_col_name_ls_of_table(self, table_name: str, sort_by_name=True) -> List[str]:
        """Retrieve column names of a given table."""
        query = f"PRAGMA table_info({table_name})"  # No parameterized query here
        self.cursor.execute(query)
        res = [row[1] for row in self.cursor.fetchall()]  # Column
        if sort_by_name:
            res.sort()

        return res

    def get_folders_and_albums(self) -> Dict[str, List[Union[PhotoFolder, PhotoAlbum]]]:
        """
        columns of ZGENERICALBUM:

            ZCACHEDCOUNT
            ZCACHEDPHOTOSCOUNT
            ZCACHEDVIDEOSCOUNT
            ZCLOUDALBUMSUBTYPE
            ZCLOUDCREATIONDATE
            ZCLOUDDELETESTATE
            ZCLOUDGUID
            ZCLOUDLASTCONTRIBUTIONDATE
            ZCLOUDLASTINTERESTINGCHANGEDATE
            ZCLOUDLOCALSTATE
            ZCLOUDMETADATA
            ZCLOUDMULTIPLECONTRIBUTORSENABLED
            ZCLOUDMULTIPLECONTRIBUTORSENABLEDLOCAL
            ZCLOUDNOTIFICATIONSENABLED
            ZCLOUDOWNEREMAILKEY
            ZCLOUDOWNERFIRSTNAME
            ZCLOUDOWNERFULLNAME
            ZCLOUDOWNERHASHEDPERSONID
            ZCLOUDOWNERISWHITELISTED
            ZCLOUDOWNERLASTNAME
            ZCLOUDPERSONID
            ZCLOUDPUBLICURLENABLED
            ZCLOUDPUBLICURLENABLEDLOCAL
            ZCLOUDRELATIONSHIPSTATE
            ZCLOUDRELATIONSHIPSTATELOCAL
            ZCLOUDSUBSCRIPTIONDATE
            ZCREATIONDATE
            ZCUSTOMKEYASSET
            ZCUSTOMQUERYPARAMETERS
            ZCUSTOMQUERYTYPE
            ZCUSTOMSORTASCENDING
            ZCUSTOMSORTKEY
            ZDUPLICATETYPE
            ZENDDATE
            ZHASUNSEENCONTENT
            ZIMPORTEDBYBUNDLEIDENTIFIER
            ZIMPORTSESSIONID
            ZISOWNED
            ZISPINNED
            ZISPROTOTYPE
            ZKEYASSET
            ZKEYASSETFACEIDENTIFIER
            ZKEYASSETFACETHUMBNAILINDEX
            ZKIND
            ZPARENTFOLDER
            ZPENDINGITEMSCOUNT
            ZPENDINGITEMSTYPE
            ZPRIVACYSTATE
            ZPROCESSINGVERSION
            ZPROJECTDATA
            ZPROJECTDOCUMENTTYPE
            ZPROJECTEXTENSIONIDENTIFIER
            ZPROJECTRENDERUUID
            ZPUBLICURL
            ZSEARCHINDEXREBUILDSTATE
            ZSEARCHINDEXREBUILDSTATE1
            ZSECONDARYKEYASSET
            ZSTARTDATE
            ZSYNCEVENTORDERKEY
            ZSYNDICATE
            ZTERTIARYKEYASSET
            ZTITLE
            ZTRASHEDDATE
            ZTRASHEDSTATE
            ZUNSEENASSETSCOUNT
            ZUSERQUERYDATA
            ZUUID
            Z_ENT
            Z_FOK_PARENTFOLDER
            Z_OPT
            Z_PK


        :return:
        """

        target_table = "ZGENERICALBUM"

if __name__ == "__main__":
    pass