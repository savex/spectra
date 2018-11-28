import spectra.utils.file as file_utils


def get_file_info(filepath):
    with open(filepath) as fd:
        raw_info = file_utils.get_file_info_fd(fd)

    return raw_info
