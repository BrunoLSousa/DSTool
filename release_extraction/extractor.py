#extractor.py

from github import Github
from datetime import datetime, timedelta, timezone
import os

class Extractor:

    def __init__(self, repo_name, interval, github_token):
        self.repo_name = repo_name
        self.interval = interval
        self.load_repo(self.repo_name, github_token)
        self.dictionary_files = dict()
        self.dictionary_files_not_downloaded = dict()
        self.first_commit = None
        self.last_commit = None

    def load_repo(self, repo_name, github_token):
        g = Github(github_token)
        self.repo = g.get_repo(repo_name)

    def identify_first_commit(self):
        commits_tmp = self.repo.get_commits().reversed
        return commits_tmp[0]

    def identify_last_commit(self):
        commits_tmp = self.repo.get_commits()
        return commits_tmp[0]

    def get_first_commit_date(self):
        if(self.first_commit == None):
            self.first_commit = self.identify_first_commit()
        return self.first_commit.commit.committer.date
    
    def get_last_commit_date(self):
        if(self.last_commit == None):
            self.last_commit = self.identify_last_commit()
        return self.last_commit.commit.committer.date
    
    def get_clone_url(self):
        return self.repo.clone_url

    def define_timeframe(self, since):
        time_frame = {}
        since = since.replace(hour=0, minute=0, second=0)
        until = since + timedelta(days=self.interval)
        until = until.replace(hour=23, minute=59, second=59)
        time_frame["since"] = since
        time_frame["until"] = until
        return time_frame

    def get_commit_most_recent(self, begin, end):
        commits_tmp = self.repo.get_commits(since=begin, until=end)
        try:
            return commits_tmp[0].sha
        except Exception as e:
            return None

    def get_commits_timeframe(self, begin, end):
        commits_tmp = self.repo.get_commits(since=begin, until=end)
        return commits_tmp

    def create_directory_system(self, path):
        system_name = self.repo_name.rsplit("/", 1)[1]
        system_dir_name = (path + "/" + system_name) if not path.endswith('/') else (path + system_name)
        if not os.path.exists(system_dir_name):
            os.makedirs(system_dir_name)
            return system_dir_name
        return None
