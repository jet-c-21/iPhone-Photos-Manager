"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 2025-03-05
"""

import pathlib
import shutil
from typing import Union


def copy_dir_entries_to_another_dir(
    src_dir: pathlib.Path,
    another_dir: pathlib.Path,
    create_another_dir=False,
):
    """
    Copies all directory entries (files and subdirectories) from `src_dir` to `another_dir`.

    :param src_dir: The source directory containing the entries to be copied.
    :param another_dir: The destination directory where the entries will be copied.
    :param create_another_dir: If True, creates `another_dir` if it does not exist.
    :return: None
    """
    assert src_dir.is_dir(), f"Source directory {src_dir} does not exist or is not a directory."

    if create_another_dir:
        another_dir.mkdir(parents=True, exist_ok=True)

    assert another_dir.is_dir(), f"Destination {another_dir} does not exist or is not a directory."

    for entry in src_dir.iterdir():
        dest_entry = another_dir / entry.name
        if entry.is_dir():
            shutil.copytree(entry, dest_entry)
        else:
            shutil.copy2(entry, dest_entry)


def copy_dir(
    orig_dir: Union[pathlib.Path, str],
    dest_dir: Union[pathlib.Path, str],
    ignore_dest_dir_existed=False,
) -> pathlib.Path:
    """
    Copies an entire directory (`orig_dir`) to a new location (`dest_dir`).
    If `ignore_dest_dir_existed` is True, deletes `dest_dir` first if it exists.

    :param orig_dir: The source directory to copy.
    :param dest_dir: The target directory where it will be copied.
    :param ignore_dest_dir_existed: If True, deletes `dest_dir` if it already exists.
    :return: The path of the copied destination directory.
    """
    orig_dir = pathlib.Path(orig_dir)
    dest_dir = pathlib.Path(dest_dir)

    if not orig_dir.is_dir():
        raise ValueError(f"The original directory {orig_dir} does not exist or is not a directory.")

    if ignore_dest_dir_existed and dest_dir.exists():
        shutil.rmtree(dest_dir)

    if dest_dir.exists():
        raise ValueError(f"The destination directory {dest_dir} already exists.")

    shutil.copytree(orig_dir, dest_dir)
    return dest_dir
