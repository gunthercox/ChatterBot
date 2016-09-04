import os
import sys

if 'install' not in sys.argv and 'egg_info' not in sys.argv:
    from .chatterbot import ChatBot

__version__ = '0.4.8'
__author__ = 'Gunther Cox'
__email__ = 'gunthercx@gmail.com'

