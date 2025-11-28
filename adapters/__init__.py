from ..core.config import read_config
import logging

def basicConfig():
    config = read_config()
    kwargs = {
        'format': '%(asctime)s %(levelname)s %(funcName)s\n%(message)s',
        'level': logging.INFO
    }
    if 'logging' in config and 'filename' in config['logging']:
        kwargs['filename'] = config['logging']['filename']
    logging.basicConfig(**kwargs)

basicConfig()
