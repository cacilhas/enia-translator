from configparser import ConfigParser
import os.path as path

config = ConfigParser()
filename = path.join(path.dirname(__file__), 'info.ini')
config.read(filename)

__AUTHOR__ = '{name} <{contact}>'.format(**config['author'])
__VERSION__ = config['enia']['version']
