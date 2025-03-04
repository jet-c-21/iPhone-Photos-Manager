"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 2025-03-04

Notes:
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

"""

import pathlib
import sqlite3
from typing import Dict, List, Union

import pandas as pd

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

    def get_table_name_ls(self) -> list[str]:
        """Retrieve a list of all table names in the database."""
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        self.cursor.execute(query)
        return [row[0] for row in self.cursor.fetchall()]

    def get_col_name_ls_of_table(self, table_name: str, sort_by_name=True) -> list[str]:
        """Retrieve column names of a given table."""
        query = f"PRAGMA table_info({table_name})"  # No parameterized query here
        self.cursor.execute(query)
        res = [row[1] for row in self.cursor.fetchall()]  # Column
        if sort_by_name:
            res.sort()

        return res

    def get_df_from_table_name(self, table_name: str) -> pd.DataFrame:
        """
        Retrieves all data from a given table and returns it as a Pandas DataFrame.

        :param table_name: The name of the table to retrieve.
        :return: A Pandas DataFrame containing the table's data.
        """
        query = f"SELECT * FROM {table_name}"

        try:
            df = pd.read_sql_query(query, self.conn)
            return df
        except Exception as e:
            print(f"[*ERROR*] Failed to fetch data from {table_name}: {e}")
            return pd.DataFrame()

    def find_album_photo_related_table_name_ls(self) -> List[str]:
        """Finds tables that likely map albums to photos."""
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'Z_%ASSETS';"
        self.cursor.execute(query)
        return [row[0] for row in self.cursor.fetchall()]

    def get_photo_count_per_album(self) -> Dict[int, int]:
        """
        Retrieves the number of photos in each album.

        :return: A dictionary where keys are album PKs and values are photo counts.
        """
        query = """
            SELECT Z_28ALBUMS AS album_id, COUNT(Z_3ASSETS) AS photo_count
            FROM Z_28ASSETS
            GROUP BY Z_28ALBUMS;
        """
        self.cursor.execute(query)
        return {row[0]: row[1] for row in self.cursor.fetchall()}

    def get_photos_per_album(self) -> Dict[int, List[Dict[str, str]]]:
        """
        Retrieves a list of photo details per album, including UUID and file path.

        :return: A dictionary where keys are album PKs, values are lists of photo metadata (UUID, path).
        """
        query = """
            SELECT 
                Z_28ALBUMS AS album_id, 
                Z_3ASSETS AS asset_id,
                ZUUID,
                ZDIRECTORY, 
                ZFILENAME
            FROM Z_28ASSETS
            JOIN ZASSET ON Z_3ASSETS = ZASSET.Z_PK
        """
        self.cursor.execute(query)

        album_photo_map = {}
        for row in self.cursor.fetchall():
            album_id, asset_id, uuid, directory, filename = row
            photo_info = {
                "uuid": uuid,
                "path": f"{directory}/{filename}" if directory and filename else None
            }
            if album_id not in album_photo_map:
                album_photo_map[album_id] = []
            album_photo_map[album_id].append(photo_info)

        return album_photo_map

    def get_albums_df(self) -> pd.DataFrame:
        """
        Retrieves album data from the ZGENERICALBUM table and returns it as a Pandas DataFrame.

        :return: A DataFrame containing album details.
        """
        target_table = "ZGENERICALBUM"
        query = f"""
            SELECT Z_PK, ZUUID, ZTITLE, ZKIND, ZPARENTFOLDER, Z_FOK_PARENTFOLDER, ZCREATIONDATE, ZSTARTDATE, ZENDDATE,  
                   ZTRASHEDSTATE, ZTRASHEDDATE 
            FROM {target_table}
        """

        # Execute the query and fetch all rows
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        # Define column names based on the query
        columns = [
            "Z_PK",
            "ZUUID",
            "ZTITLE",
            "ZKIND",
            "ZPARENTFOLDER",
            "Z_FOK_PARENTFOLDER",
            "ZCREATIONDATE",
            "ZSTARTDATE",
            "ZENDDATE",
            "ZTRASHEDSTATE",
            "ZTRASHEDDATE",
        ]

        # Create a Pandas DataFrame
        df = pd.DataFrame(rows, columns=columns)

        # Convert columns to integers while keeping NaN as NaN
        df["ZKIND"] = pd.to_numeric(df["ZKIND"], errors="coerce").astype("Int64")
        df["ZPARENTFOLDER"] = pd.to_numeric(df["ZPARENTFOLDER"], errors="coerce").astype("Int64")

        return df

    def get_user_created_folders_and_albums(self) -> Dict[str, List[Union[PhotoFolder, PhotoAlbum]]]:
        albums_df = self.get_albums_df()

        # !@# for debug
        albums_df = albums_df[albums_df["ZTITLE"] != "22.05到25.03 未整理"]

        user_created_folder_z_kind = 4000
        _root_photo_folder_df: pd.DataFrame = albums_df[
            (albums_df["ZKIND"] == user_created_folder_z_kind) & (albums_df["ZPARENTFOLDER"] == 1)
        ].copy()

        # Remove extracted folders from albums_df
        albums_df = albums_df[~albums_df["Z_PK"].isin(_root_photo_folder_df["Z_PK"])]

        user_created_folder_res_ls = []
        pk_to_obj = {}
        for _row_idx, _row in _root_photo_folder_df.iterrows():
            pk = _row["Z_PK"]
            created_datetime = _row["ZCREATIONDATE"]
            photo_folder = PhotoFolder(
                _row["ZTITLE"],
                _row["ZUUID"],
                pk_in_z_generic_album=pk,
                created_datetime=created_datetime,
            )
            user_created_folder_res_ls.append(photo_folder)
            pk_to_obj[pk] = photo_folder

        while user_created_folder_z_kind in albums_df["ZKIND"].unique():
            _rest_folder_df = albums_df[albums_df["ZKIND"] == user_created_folder_z_kind].copy()
            albums_df = albums_df[~albums_df["Z_PK"].isin(_rest_folder_df["Z_PK"])]

            for _row_idx, _row in _rest_folder_df.iterrows():
                pk = _row["Z_PK"]
                created_datetime = _row["ZCREATIONDATE"]
                parent_pk = _row["ZPARENTFOLDER"]
                assert parent_pk in pk_to_obj
                parent_photo_folder: PhotoFolder = pk_to_obj[parent_pk]

                photo_folder = PhotoFolder(
                    _row["ZTITLE"],
                    _row["ZUUID"],
                    pk_in_z_generic_album=pk,
                    created_datetime=created_datetime,
                )

                parent_photo_folder.add_data(photo_folder)
                pk_to_obj[pk] = photo_folder

        user_created_album_z_kind = 2
        _user_created_album_df = albums_df[albums_df["ZKIND"] == user_created_album_z_kind]

        user_created_album_res_ls = []
        _standalone_album_df = _user_created_album_df[_user_created_album_df["ZPARENTFOLDER"] == 1].copy()

        _user_created_album_df = _user_created_album_df[
            ~_user_created_album_df["Z_PK"].isin(_standalone_album_df["Z_PK"])
        ]

        for _row_idx, _row in _standalone_album_df.iterrows():
            photo_album = PhotoAlbum(
                _row["ZTITLE"],
                _row["ZUUID"],
                pk_in_z_generic_album=_row["Z_PK"],
                created_datetime=_row["ZCREATIONDATE"],
                # photo_count=?,
            )
            user_created_album_res_ls.append(photo_album)

        for _row_idx, _row in _user_created_album_df.iterrows():
            parent_pk = _row["ZPARENTFOLDER"]
            assert parent_pk in pk_to_obj
            parent_photo_folder: PhotoFolder = pk_to_obj[parent_pk]

            photo_album = PhotoAlbum(
                _row["ZTITLE"],
                _row["ZUUID"],
                pk_in_z_generic_album=_row["Z_PK"],
                created_datetime=_row["ZCREATIONDATE"],
                # photo_count=?,
            )

            parent_photo_folder.add_data(photo_album)

        return {
            "folders": user_created_folder_res_ls,
            "albums": user_created_album_res_ls,
        }

    def get_user_created_albums(self) -> List[PhotoAlbum]:
        result = []
        d = self.get_user_created_folders_and_albums()
        for folder in d["folders"]:
            result.append(folder.get_all_albums())

        result.extend(d["albums"])
        return result

    def view_user_created_folders_and_albums(self):
        d = self.get_user_created_folders_and_albums()

        msg = "[*INFO*] - user created folders:"
        print(msg)
        for folder in d["folders"]:
            folder.view_structure()
        print()

        msg = "[*INFO] - user created albums:"
        print(msg)
        for album in d["albums"]:
            album.view_info()
        print()
