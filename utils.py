
from config import CONFIG

import os


def relpath(file_relpath, rootpath=CONFIG.ROOT_DIR):
    return os.path.join(rootpath, file_relpath)