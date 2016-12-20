#!/usr/bin/python
import os
from time import strftime
import yaml
import sys
from modules.RepoManager import RepoManager


def open_repo(project):
    if repos.contains_repo(project):
        print(str(repos.get_repo(project)))
    else:
        IOError("project not found")


with open("config/config.yml", 'r') as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

settings = config['workflow']
projects_root = settings['project_dir']
routine = None
config = None
repos = RepoManager(projects_root)

try:
    routine = sys.argv[1]
except IndexError:
    print('No routine provided')
    exit()

if routine == 'open':
    try:
        project = sys.argv[2]
    except IndexError:
        print('No project provided')
        exit()
    open_repo(project)

else:
    print('unknown routine')
    NotImplementedError('routine not supported')
