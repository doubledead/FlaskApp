import os


def get_app_base_path():
    return os.path.dirname(os.path.realpath(__file__))


def get_instance_folder_path():
    return os.path.join(get_app_base_path(), 'instance')


# Helper/util function for integer check.
def representsint(object):
    try:
        int(object)
        return True
    except ValueError:
        return False
