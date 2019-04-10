import configparser
import sys
import os


def get_chatterbot_version():
    config = configparser.ConfigParser()

    current_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
    config_file_path = os.path.join(parent_directory, 'setup.cfg')

    config.read(config_file_path)

    return config['chatterbot']['version']


if __name__ == '__main__':
    if '--version' in sys.argv:
        print(get_chatterbot_version())
