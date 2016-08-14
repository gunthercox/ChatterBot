import os
import sys

script_name = os.path.basename(sys.argv[0])

if script_name != 'setup.py' and 'egg_info' not in sys.argv:
    from .chatterbot import ChatBot

__version__ = '0.4.6'
__author__ = 'Gunther Cox'
__email__ = 'gunthercx@gmail.com'

