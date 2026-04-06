"""The module contains the """

import gzip
from os.path import exists, join


def save_game(
        data,
        filename: str,
        directory: str = None,
        filetype: str = None
) -> None:
    from json import dump
    from os import makedirs
    if directory and not exists(directory):
        makedirs(directory)
    filepath = _get_savefile_path(filename, directory=directory, filetype=filetype)
    with gzip.open(filepath, 'wt', encoding='utf-8') as file:
        dump(data, file, indent=2)


def _get_savefile_path(
        filename: str,
        directory: str = None,
        filetype: str = None
) -> str:
    if filetype:
        filename += filetype
    if directory:
        return join(directory, filename)
    return filename


def load_game(
        filename: str,
        directory: str = None,
        filetype: str = None
) -> None:
    from json import load
    filepath = _get_savefile_path(filename, directory=directory, filetype=filetype)
    with gzip.open(filepath, 'rt', encoding='utf-8') as savefile:
        return load(savefile)


def delete_saved_game(
        filename: str,
        directory: str = None,
        filetype: str = None
) -> None:
    from os import remove
    filepath = _get_savefile_path(filename, directory=directory, filetype=filetype)
    if exists(filepath):
        remove(filepath)


def get_saved_game_existence(
        filename: str,
        directory: str = None,
        filetype: str = None
) -> bool:
    return exists(_get_savefile_path(filename, directory=directory, filetype=filetype))


def get_colored_message(message: str):
    pass


def quit_game(func):
    from sys import exit
    func()
    exit()
