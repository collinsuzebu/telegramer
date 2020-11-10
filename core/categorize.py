import os
from pathlib import Path
from collections import defaultdict

from phrydy import MediaFile
from phrydy.mediafile import FileTypeError, UnreadableFileError

from core.telegramer import delete_media_host


group_options = ["album", "artist", "art", "custom", "format", "year"]


class GroupFiles:
    def group_album(self, directory, groupby, custom_title):
        """Run Album Grouping.

		Group music audio based on format specified
		Positional Arguments:
		directory              -- String indicating username that report
		                          should be created against.
		groupby       	       -- Perform grouping based on the following attributes
									--	album
									--	artist
									--	art (music cover)
									--	type (e.g mp3)
									--	year
									--	custom

									--	Use groupby='custom' when all files 
										in a directory shares common info

		custom_title           -- Creates a directory with a custom name.
		                          If no name is given, it defaults to 'CustomFolder'.

		Return Value:		   -- String

		"""
        audio_names = [
            os.path.join(directory, audio)
            for audio in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, audio))
        ]
        album_names = defaultdict(list)
        groupby_name = custom_title

        for audio in audio_names:
            try:
                if groupby != "custom":
                    groupby_name = str(getattr(MediaFile(audio), groupby))
                    if groupby == "art":
                        groupby_name = len(groupby_name)
                        groupby_name = "{} {}".format("Art", groupby_name)

                album_name = delete_media_host(groupby_name)
                album_name = "random" if album_name == "" else album_name.strip()
                album_names[album_name].append(audio)
            except (AttributeError, TypeError, FileTypeError, UnreadableFileError) as e:
                print(f"[-] {audio} has no {groupby} attribute")

        for album_name, v in album_names.items():
            album_dir = Path(os.path.join(directory, album_name))  # Make directory path
            if (
                not os.path.isdir(album_dir)
                and len(v) >= 3
                and os.path.basename(album_dir) != "None"
            ):
                album_dir.mkdir(exist_ok=False)  # create directory if it does not exist
                for aud in v:
                    file = os.path.join(album_dir, os.path.basename(aud))
                    if not os.path.isfile(file):
                        # print('[+] Moved {} to {}'.format(aud, album_dir))
                        os.rename(aud, file)
            else:
                for aud in v:
                    file = os.path.join(album_dir, os.path.basename(aud))
                    if not os.path.isfile(file) and os.path.isdir(album_dir):
                        # print('Moved {} to {}'.format(file, album_dir))
                        os.rename(aud, file)
        return "[+] successfully grouped files"

    def run(self, args):
        directory = args.directory
        groupby = args.groupby
        custom_folder = args.custom_folder

        return self.group_album(directory, groupby, custom_folder)


# TODO - Include deep search, to search inner directories
