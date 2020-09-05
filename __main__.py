import os
import sys
import logging
from argparse import ArgumentParser, HelpFormatter

from core import categorize
from core import telegramer


def _validate_input_args(args):
    if not os.path.isdir(args.directory):
        err_msg = ('A valid directory is required')

        print(f'{argparser.prog}: error: {err_msg}', file=sys.stderr)
        sys.exit()


argparser = ArgumentParser(
    prog='telegramer',
    description='Rename audio files gotten from Telegram channels',
    formatter_class=lambda prog: HelpFormatter(prog,width=120,max_help_position=55))


argparser.add_argument('--version',
    action='version',
    version='%(prog)s 1.0')

group1 = argparser.add_mutually_exclusive_group()

group1.add_argument("-v", "--verbose",
	help="Show operation output in stdout",
    action="store_const",
    dest="log",
    const=logging.INFO)


group1.add_argument(
    '--debug',
    help="Enable debug mode",
    action="store_const",
    dest="log",
    const=logging.DEBUG,
    default=logging.WARNING)

group2 = argparser.add_mutually_exclusive_group()

group2.add_argument("-t", "--title",
	help="Customize file name with your preference",
    dest="custom_title")

argparser.add_argument('-g', '--groupby',
    choices=categorize.group_options,
    required=False,
    dest='groupby',
    help=('Specify how the audio files in a directory '
    	  'are to be grouped.'))


argparser.add_argument('-r', '--rename',
    required=False,
    dest='rename',
    action="store_true",
    help=('Select option to begin renaming audio files'))

argparser.add_argument('-f', '--folder',
    required=False,
    dest='custom_folder',
    default='custom_folder',
    help='Specify a custom directory name. Use this where item '
         'could not be grouped with the groupby flag.')


directory = os.getcwd()

argparser.add_argument('-d', '--directory',
    dest='directory',
    default=directory,
    help='Specify the directory to perform the '
         'operation. Default is current directory')


args = argparser.parse_args()
_validate_input_args(args)

logging.basicConfig(level=args.log, format='%(message)s')

if args.rename:
	telegramer.main(args)

if args.groupby:
	result = categorize.GroupFiles().run(args)
	logging.info(result)