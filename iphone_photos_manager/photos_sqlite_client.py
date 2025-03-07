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
from tqdm.auto import tqdm

from iphone_photos_manager.media_entities import MediaAlbum, MediaAsset, MediaFolder
from iphone_photos_manager.utils.general import apple_ts_to_datetime


class PhotosSqliteClient:
    def __init__(self, photos_sqlite_path: pathlib.Path):
        self.photos_sqlite_path = photos_sqlite_path
        assert self.photos_sqlite_path.is_file(), f"{self.photos_sqlite_path} is not a file"

        self.dcim_dir = self.photos_sqlite_path.parent.parent / "DCIM"
        assert self.dcim_dir.is_dir(), f"{self.dcim_dir} is not a directory"

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

    def find_album_media_asset_related_table_name_ls(self) -> List[str]:
        """Finds tables that likely map albums to photos."""
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'Z_%ASSETS';"
        self.cursor.execute(query)
        return [row[0] for row in self.cursor.fetchall()]

    def get_media_asset_count_per_album(self) -> Dict[int, int]:
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

    def get_assets_df(self) -> pd.DataFrame:
        """
        Retrieves all media asset data from the database and returns it as a Pandas DataFrame.

        :return: A DataFrame containing all assets with metadata.
        """
        query = """
            SELECT 
                Z_28ALBUMS AS album_id, 
                Z_3ASSETS AS asset_id,
                ZUUID,
                ZDIRECTORY, 
                ZFILENAME,
                ZDATECREATED,
                ZMODIFICATIONDATE,
                ZWIDTH,
                ZHEIGHT,
                ZORIENTATION,
                ZFAVORITE,
                ZHIDDEN,
                ZLATITUDE,
                ZLONGITUDE,
                ZLOCATIONDATA,
                ZUNIFORMTYPEIDENTIFIER,
                ZVIDEOCPDURATIONVALUE,
                ZDURATION
            FROM Z_28ASSETS
            JOIN ZASSET ON Z_3ASSETS = ZASSET.Z_PK
        """

        df = pd.read_sql_query(query, self.conn)

        # Convert timestamp columns to readable datetime format
        df["ZDATECREATED"] = df["ZDATECREATED"].apply(apple_ts_to_datetime)
        df["ZMODIFICATIONDATE"] = df["ZMODIFICATIONDATE"].apply(apple_ts_to_datetime)

        # Convert boolean columns
        df["ZFAVORITE"] = df["ZFAVORITE"].astype(bool)
        df["ZHIDDEN"] = df["ZHIDDEN"].astype(bool)

        # we dont need fillna so far, and avoid using try

        return df

    def get_all_media_assets(self) -> List[MediaAsset]:
        """
        Converts the asset DataFrame into a list of `MediaAsset` objects.

        :return: A list of `MediaAsset` instances.
        """
        assets_df = self.get_assets_df()

        media_assets = []
        for _, row in assets_df.iterrows():
            if row["ZDIRECTORY"]:
                dcim_sub_dir_name = pathlib.Path(row["ZDIRECTORY"]).name
                file_path = self.dcim_dir / dcim_sub_dir_name / row["ZFILENAME"]
            else:
                file_path = None

            duration = row["ZVIDEOCPDURATIONVALUE"] or row["ZDURATION"]

            media_asset = MediaAsset(
                filename=row["ZFILENAME"],
                file_path=file_path,
                uuid=row["ZUUID"],
                album_id=row["album_id"],
                width=row["ZWIDTH"],
                height=row["ZHEIGHT"],
                orientation=row["ZORIENTATION"],
                file_size=None,  # No file size column available
                is_favorite=row["ZFAVORITE"],
                latitude=row["ZLATITUDE"],
                longitude=row["ZLONGITUDE"],
                location_data=row["ZLOCATIONDATA"],
                media_type=row["ZUNIFORMTYPEIDENTIFIER"],
                duration=duration,
                pk_in_z_asset_album=row["asset_id"],
                created_datetime=row["ZDATECREATED"],
                modified_datetime=row["ZMODIFICATIONDATE"],
            )
            media_assets.append(media_asset)

        return media_assets

    def get_album_id_to_media_asset_ls(self) -> Dict[int, List[MediaAsset]]:
        """
        Retrieves a list of media assets (photos/videos) per album.
        """
        result = {}
        for ma in self.get_all_media_assets():
            if ma.album_id not in result:
                result[ma.album_id] = [ma]
            else:
                result[ma.album_id].append(ma)

        return result

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

    def get_user_created_folders_and_albums(self) -> Dict[str, List[Union[MediaFolder, MediaAlbum]]]:
        albums_df = self.get_albums_df()

        # !@# for debug
        albums_df = albums_df[albums_df["ZTITLE"] != "22.05到25.03 未整理"]

        user_created_folder_z_kind = 4000
        _root_media_folder_df: pd.DataFrame = albums_df[
            (albums_df["ZKIND"] == user_created_folder_z_kind) & (albums_df["ZPARENTFOLDER"] == 1)
        ].copy()

        # Remove extracted folders from albums_df
        albums_df = albums_df[~albums_df["Z_PK"].isin(_root_media_folder_df["Z_PK"])]

        user_created_folder_res_ls = []
        pk_to_obj = {}
        for _row_idx, _row in _root_media_folder_df.iterrows():
            pk = _row["Z_PK"]
            created_datetime = _row["ZCREATIONDATE"]
            media_folder = MediaFolder(
                _row["ZTITLE"],
                _row["ZUUID"],
                pk_in_z_generic_album=pk,
                created_datetime=created_datetime,
            )
            user_created_folder_res_ls.append(media_folder)
            pk_to_obj[pk] = media_folder

        while user_created_folder_z_kind in albums_df["ZKIND"].unique():
            _rest_folder_df = albums_df[albums_df["ZKIND"] == user_created_folder_z_kind].copy()
            albums_df = albums_df[~albums_df["Z_PK"].isin(_rest_folder_df["Z_PK"])]

            for _row_idx, _row in _rest_folder_df.iterrows():
                pk = _row["Z_PK"]
                created_datetime = _row["ZCREATIONDATE"]
                parent_pk = _row["ZPARENTFOLDER"]
                assert parent_pk in pk_to_obj
                parent_media_folder: MediaFolder = pk_to_obj[parent_pk]

                media_folder = MediaFolder(
                    _row["ZTITLE"],
                    _row["ZUUID"],
                    pk_in_z_generic_album=pk,
                    created_datetime=created_datetime,
                )

                parent_media_folder.add_data(media_folder)
                pk_to_obj[pk] = media_folder

        user_created_album_z_kind = 2
        _user_created_album_df = albums_df[albums_df["ZKIND"] == user_created_album_z_kind]

        user_created_album_res_ls = []
        _standalone_album_df = _user_created_album_df[_user_created_album_df["ZPARENTFOLDER"] == 1].copy()

        _user_created_album_df = _user_created_album_df[
            ~_user_created_album_df["Z_PK"].isin(_standalone_album_df["Z_PK"])
        ]

        album_id_to_media_asset_ls = self.get_album_id_to_media_asset_ls()

        for _row_idx, _row in _standalone_album_df.iterrows():
            _media_assets = album_id_to_media_asset_ls.get(_row["Z_PK"], None)
            media_album = MediaAlbum(
                _row["ZTITLE"],
                _row["ZUUID"],
                pk_in_z_generic_album=_row["Z_PK"],
                created_datetime=_row["ZCREATIONDATE"],
                media_asset_data=_media_assets,
            )
            user_created_album_res_ls.append(media_album)

        for _row_idx, _row in _user_created_album_df.iterrows():
            parent_pk = _row["ZPARENTFOLDER"]
            assert parent_pk in pk_to_obj
            parent_media_folder: MediaFolder = pk_to_obj[parent_pk]

            _media_assets = album_id_to_media_asset_ls.get(_row["Z_PK"], None)
            media_album = MediaAlbum(
                _row["ZTITLE"],
                _row["ZUUID"],
                pk_in_z_generic_album=_row["Z_PK"],
                created_datetime=_row["ZCREATIONDATE"],
                media_asset_data=_media_assets,
            )

            parent_media_folder.add_data(media_album)

        return {
            "folders": user_created_folder_res_ls,
            "albums": user_created_album_res_ls,
        }

    def get_user_created_albums(self) -> List[MediaAlbum]:
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

    def export_user_created_folders_and_albums(self, export_root_dir: pathlib.Path):
        folders_and_albums = self.get_user_created_folders_and_albums()

        for folder in tqdm(folders_and_albums["folders"], desc="exporting user created folders"):
            folder.export(export_root_dir)
            # break

        for album in tqdm(folders_and_albums["albums"], desc="exporting user created albums"):
            album.export(export_root_dir)
            # break
