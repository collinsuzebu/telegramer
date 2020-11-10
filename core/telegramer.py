import os, sys, re
from pathlib import Path

from phrydy import MediaFile
from phrydy.mediafile import FileTypeError, UnreadableFileError
from PIL import Image


def delete_media_host(string):
    if not string:
        return None
    substitute = re.compile(
        r"""
							(\s*?(?:\[|\(|\{|)?@\w*\s*\w+(?:\)|\]|\})?	#@mention
							|\s?\|?\|?\-?\s*\#?
							\[?(?:\w{3}\.)?\w+\.\w{2,3}(?:\.\w{2})?\b\]? 	#website
							|\[?\s*\bBB\w{0,3}\s*\-?(CHANNEL)?\s*?\-?\s*\w+\s*\]?	#bbm
							|\s+\|s*
							|\||\\|\/|\?|\<|\>|\:|\*|)""",
        re.VERBOSE | re.IGNORECASE,
    )
    string = re.sub(r"\s+", " ", string)
    string = re.sub('"', "'", string)
    string = re.sub(":", ";", string)
    string = re.sub("/", "-", string)
    return re.sub(substitute, "", string).strip()


def word_count(string):
    return len(string.split())


def modify_metatag(media_file):
    media_file.title = delete_media_host(media_file.title)
    media_file.artist = delete_media_host(media_file.artist)
    media_file.album = delete_media_host(media_file.album)
    media_file.save()
    return media_file


def set_art_metatag(media_file, img):
    img = Image.open(img).tobytes()
    media_file.art = img
    media_file.save()

    return media_file


def get_audio_title(audio_path, default=False, title=False):
    if default:
        # Get the original file name
        return os.path.splitext(os.path.basename(audio_path))[0]

    try:
        media_file = MediaFile(audio_path)
        media_file = modify_metatag(media_file)

        if title:
            return delete_media_host("{}".format(media_file.title))

        audio_name = delete_media_host(
            "{} - {}".format(media_file.artist, media_file.title)
        )
        return audio_name

    except (FileTypeError, UnreadableFileError) as e:
        base = os.path.splitext(os.path.basename(audio_path))[0]
        print(f'File format not supported: "{base}"')
        return base


def rename_audio(audio_name, audio_path, custom=False):
    audio_ext = os.path.splitext(audio_path)[1]
    old_audio_name = audio_path
    if custom:
        audio_name = custom
    new_audio_name = os.path.join(os.path.dirname(audio_path), audio_name + audio_ext)

    if "None" in new_audio_name:
        print("[-] Empty metatag")

    elif word_count(new_audio_name) > 23:
        print("[-] Cannot rename | Text too long")

    else:
        if not os.path.exists(new_audio_name):
            os.rename(old_audio_name, new_audio_name)
            # print(f'[+] Successfully renamed {new_audio_name}')

    return new_audio_name


def main(args):
    directory = args.directory

    if args.custom_title:
        r = input(
            "\nConfirm you want to rename all files in "
            "this directory with the same name (y/n): "
        )

        r = True if r.strip().lower().startswith("y") else False

    for audio in os.listdir(directory):
        audio_path = os.path.join(directory, audio)

        if os.path.isfile(audio_path):
            audio_name = get_audio_title(audio_path, title=False)
            rename_audio(audio_name, audio_path)

            # Use Customized tile
            if args.custom_title:
                audio_name = get_audio_title(audio_path, default=True)
                custom = "{} - {}".format(audio_name[-3:], args.custom_title)
                if custom[:3].isdigit() and r:
                    rename_audio(audio_name, audio_path, custom=custom)
                elif r:
                    rename_audio(audio_name, audio_path, custom=args.custom_title)
