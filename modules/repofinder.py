import os
from ConfigParser import ConfigParser
from StringIO import StringIO

class RepoFinder:
    """Looks for git repositories in a given directory"""

    __repos = {}
    __root = None

    def __init__(self, projectroot):
        self.__root = projectroot
        self.__scan_dir(self.__root)

    def __scan_dir(self, dir):
        """Recursively looks in a directory for git repositories"""
        if self.is_git_repo(dir):
            self.__add_repo(os.path.basename(dir), dir)
            return

        for file_name in os.listdir(dir):
            path = dir+file_name
            if self.is_git_repo(path):
                self.__add_repo(file_name, path)
            elif os.path.isdir(path) and os.path.islink(path) is False:
                self.__scan_dir(path+'/')

    def __add_repo(self, dir, path):
        config_path = path+'/.git/config'
        if os.path.isfile(config_path) is False:
            IOError('Path is not a git directory')

        remote = None
        with open(config_path) as f:
            c = f.readlines()
        config_parser = ConfigParser()
        # This one liner is needed, since git config files are indented with a tab
        config_parser.readfp(StringIO(''.join([l.lstrip() for l in c])))
        for section in config_parser.sections():
            if section.startswith('remote'):
                remote = config_parser.get(section, 'url')

        self.__repos[self.normalize_repo(dir)] = (path, remote)

    def contains_repo(self, name):
        try:
            self.__repos[self.normalize_repo(name)]
            return True
        except IndexError:
            return False

    def get_repos(self):
        return self.__repos

    def get_repo(self, name):
        if self.contains_repo(name):
            return self.__repos[self.normalize_repo(name)]
        return None

    @staticmethod
    def normalize_repo(repo):
        return repo.lower().strip()

    @staticmethod
    def is_git_repo(dir):
        if os.path.isdir(dir) is False:
            return False
        for fname in os.listdir(dir):
            if fname == '.git':
                return True
        return False
