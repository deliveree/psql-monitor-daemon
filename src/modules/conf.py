from os import listdir
from toml import load


def load_conf(folder_path="../conf"):
    filenames = listdir(folder_path)
    conf = [folder_path + "/" + filename for filename in filenames]
    return load(conf)
