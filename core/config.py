import os, json
from configparser import ConfigParser

def read_config():
    HOME = os.environ['HOME']
    path = os.path.join(HOME, '.config', 'resounds', 'config.ini')
    config = ConfigParser()
    config.read(path, encoding="utf-8")
    return config

def move_from_save_dir_to_read_dir():
    config = read_config()
    if 'Example' not in config:
        raise LookupError("no found [Example] in config.ini")
    Example = config['Example']
    if 'save_dir' not in Example:
        raise AttributeError("no found save_dir of [Example] in config.ini")
    if 'read_dir' not in Example:
        raise AttributeError("no found read_dir of [Example] in config.ini")
    if Example['save_dir'] == Example['read_dir']:
        raise AssertionError("save_dir and read_dir can't be the same directory")
    os.system(f"mv {Example['save_dir']}/* {Example['read_dir']}")

def save_example(example, ext = '.jsonl'):
    config = read_config()
    fname = example['func_name'] + ext
    path = os.path.join(config['Example']['save_dir'], fname)
    try:
        with open(path, 'a', encoding="utf-8") as f:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')
    except:
        pass

def read_example(func_name, ext = '.jsonl'):
    config = read_config()
    fname = func_name + ext
    path = os.path.join(config['Example']['read_dir'], fname)
    try:
        with open(path, 'r', encoding="utf-8") as f:
            return [json.loads(example) for example in f.readlines()]
    except:
        return []

def save_stats(stats):
    config = read_config()
    fname = stats['func_name'] + '.stats'
    path = os.path.join(config['Example']['save_dir'], fname)
    try:
        with open(path, 'w', encoding="utf-8") as f:
            f.write(json.dumps(stats, ensure_ascii=False))
    except:
        pass

def read_stats(func_name):
    config = read_config()
    fname = func_name + '.stats'
    path = os.path.join(config['Example']['read_dir'], fname)
    try:
        with open(path, 'r', encoding="utf-8") as f:
            return json.loads(f.read())
    except:
        return {
            'func_name': func_name,
            'instructions': {}
        }
