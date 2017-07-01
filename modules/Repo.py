import os
from ConfigParser import ConfigParser
from StringIO import StringIO


class Repo:

    __path = None
    __name = None
    __remote = None

    def __init__(self, path):
        self.__path = path
        self.__load_config()

    def __load_config(self):
        config_path = self.__path + '/.git/config'
        if os.path.isfile(config_path) is False:
            IOError('Path is not a git directory')

        with open(config_path) as f:
            c = f.readlines()
        config_parser = ConfigParser()
        # This one liner is needed, since git config files are indented with a tab
        config_parser.readfp(StringIO(''.join([l.lstrip() for l in c])))
        for section in config_parser.sections():
            if section.startswith('remote'):
                self.__remote = config_parser.get(section, 'url')

        if self.__remote is None:
            ImportError('could not find git remote url')

    def get_current_branch(self):
        """Todo: implement"""

    def branch_exists(self, branch_name):
        """Todo: implement"""

    def create_branch(self, branch_name):
        """Todo: implement"""

    def create_pr(self):
        """Todo: implement"""