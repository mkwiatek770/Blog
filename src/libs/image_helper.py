"""
Library to manage images
"""
import os
import re
from typing import Union

from werkzeug.datastructures import FileStorage
from flask_uploads import UploadSet, IMAGES

IMAGE_SET = UploadSet(name="images", IMAGES)


def save_image(image: FileStorage, folder: str = None, name: str = None) -> str:
    """Saves image and return it's name in storage."""
    return IMAGE_SET.save(image, folder, name)


def get_path(filename: str, folder: str):
    """Get full path of file in storage"""
    return IMAGE_SET.path(filename, folder)


def find_image_any_format(filename: str, folder: str) -> Union[str, None]:
    """
    Given a format-less filename, try to find the file by appending each of the allowed formats to the given
    filename and check if the file exists
    """
    for _format in IMAGES:  # look for existing avatar and delete it
        avatar = f"{filename}.{_format}"
        avatar_path = IMAGE_SET.path(filename=avatar, folder=folder)
        if os.path.isfile(avatar_path):
            return avatar_path
    return None


def _retrieve_filename(file: Union[FileStorage, str]) -> str:
    """
    Make our filename related functions generic, able to deal with
    FileStorage object as well as filename str.
    """
    if isinstance(file, FileStorage):
        return file.filename
    return file


def is_filename_safe(file: Union[FileStorage, str]) -> bool:
    """
    Check if a filename is secure according to our definition
    - starts with a-z A-Z 0-9 at least one time
    - only contains a-z A-Z 0-9 and _().-
    - followed by a dot (.) and a allowed_format at the end
    """
    filename = _retrieve_filename(file)

    allowed_format = "|".join(IMAGES)
    # format IMAGES into regex, eg: ('jpeg','png') --> 'jpeg|png'
    regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$"
    return re.match(regex, filename) is not None


def get_basename(file: Union[FileStorage, str]) -> str:
    """
    Return full image name in the path
    """
    filename = _retrieve_filename(file)
    return os.path.split(filename)[1]


def get_extension(file: Union[FileStorage, str]) -> str:
    """Returns file extension with '.' character like: '.jpg'"""
    filename = _retrieve_filename(file)
    return os.path.splitext(filename)[1]  # .jpg / .png
