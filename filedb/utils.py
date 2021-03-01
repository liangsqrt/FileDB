import os


def closest_file_db_cfg(path='.', prevpath=None):
    """Return the path to the closest scrapy.cfg file by traversing the current
    directory and its parents
    """
    if path == prevpath:
        return ''
    path = os.path.abspath(path)
    cfgfile = os.path.join(path, 'filedb.cfg')
    if os.path.exists(cfgfile):
        return cfgfile
    return closest_file_db_cfg(os.path.dirname(path), path)

