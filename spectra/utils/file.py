import grp
import os
import pwd
import time

from config_file import inspector_config

_default_time_format = inspector_config.get_default_time_format()


def remove_file(filename):
    os.remove(filename)
    # open('filename', 'w').close()


def write_str_to_file(filename, _str):
    with open(filename, 'w') as fo:
        fo.write(_str)


def append_str_to_file(filename, _str):
    with open(filename, 'a') as fa:
        fa.write(_str)


def append_line_to_file(filename, _str):
    with open(filename, 'a') as fa:
        fa.write(_str+'\n')


def read_file(filename):
    _buf = None
    with open(filename, 'rb') as fr:
        _buf = fr.read()
    return _buf


def read_file_as_lines(filename):
    _list = []
    with open(filename, 'r') as fr:
        for line in fr:
            _list.append(line)
    return _list


def get_file_info_fd(fd, time_format=_default_time_format):

    def format_time(unixtime):
        return time.strftime(
            time_format,
            time.gmtime(unixtime)
        )

    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = \
        os.fstat(fd.fileno())

    _dict = {
        'fd': fd.fileno(),
        'mode': oct(mode & 0777),
        'device': hex(dev),
        'inode': ino,
        'hard_links': nlink,
        'owner_id': uid,
        'owner_name': pwd.getpwuid(uid).pw_name,
        'owner_group_name': grp.getgrgid(gid).gr_name,
        'owner_group_id': gid,
        'size': size,
        'access_time': format_time(atime),
        'modification_time': format_time(mtime),
        'creation_time': format_time(ctime)
    }

    return _dict
