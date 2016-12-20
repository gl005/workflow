import os
import Repo


class RepoManager:
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
        self.__repos[self.normalize_repo(dir)] = Repo(path)

    def contains_repo(self, name):
        try:
            self.__repos[self.normalize_repo(name)]
            return True
        except IndexError:
            return False

    def get_repos(self):
        return self.__repos

    def search_repo(self, name):
        """todo: implement"""

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
            if fname == '.git' and os.path.isdir(dir+fname):
                return True
        return False
