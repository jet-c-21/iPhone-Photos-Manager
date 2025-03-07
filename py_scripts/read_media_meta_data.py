"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 2025-03-05
"""
# >>> Dynamic Changing `sys.path` in Runtime by Adding Project Directory to Path >>>
import pathlib
import sys

THIS_FILE_PATH = pathlib.Path(__file__).absolute()
THIS_FILE_PARENT_DIR = THIS_FILE_PATH.parent
PROJECT_DIR = THIS_FILE_PARENT_DIR.parent
sys.path.append(str(PROJECT_DIR))
print(f"[*INFO*] - append directory to path: {PROJECT_DIR}")
# <<< Dynamic Changing `sys.path` in Runtime by Adding Project Directory to Path <<<

import datetime
import shutil

from tqdm.auto import tqdm

if __name__ == "__main__":
    dir_to_organize = pathlib.Path("/media/puff/TOSHIBA-4T/iphone-Photos/iCareFone-Album-Export_2025-03-05/22.05到25.03 未整理/")

    # img_type_set = {'JPEG', 'heic', 'PNG'}
    # video_type_set = {'MP4', 'MOV'}

    # {'.HEIC', '.mov', '.jpg', '.MOV', '.MP4', '.JPEG', '.JPG', '.PNG', '.heic'}
    # image_ext_set = {".heic", ".HEIC", ".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG"}
    # video_ext_set = {".mov", ".MOV", ".mp4", ".MP4"}

    for fp in tqdm(dir_to_organize.iterdir()):
        if fp.is_file():
            stat_info = fp.stat()
            created_datetime = datetime.datetime.fromtimestamp(stat_info.st_ctime)

            # Create directory based on year and month (e.g., "2025-03")
            year_month_dir_name = f"{created_datetime.year}-{str(created_datetime.month).zfill(2)}"
            year_month_dir = dir_to_organize / year_month_dir_name
            year_month_dir.mkdir(parents=True, exist_ok=True)

            # Destination file path
            new_fp = year_month_dir / fp.name

            # Move the file
            shutil.move(str(fp), str(new_fp))

            print(f"Moved: {fp.name} → {new_fp}")


