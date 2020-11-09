#extractor.py

from github import Github
from datetime import datetime, timedelta, timezone
# import wget
import urllib.request
import os
import shutil
from logger import Logger

AUTH_TOKEN = ""

class Extractor:

    def __init__(self, repo_name, interval):
        self.repo_name = repo_name
        self.interval = interval
        self.load_repo(self.repo_name)
        self.dictionary_files = dict()
        self.dictionary_files_not_downloaded = dict()
        self.first_commit = None
        self.last_commit = None

    def load_repo(self, repo_name):
        g = Github(AUTH_TOKEN)
        self.repo = g.get_repo(repo_name)

    def identify_first_commit(self):
        commits_tmp = self.repo.get_commits().reversed
        # totalCommits = commits_tmp.totalCount
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
        # print(commits_tmp[0].commit.committer.date)
        # print(commits_tmp[0].sha)
        # print(commits_tmp[1].commit.committer.date)
        try:
            return commits_tmp[0].sha
        except Exception as e:
            return None

    def get_commits_timeframe(self, begin, end):
        commits_tmp = self.repo.get_commits(since=begin, until=end)
        return commits_tmp

    # def process_commits_list(self, commits_list):
    #     for commit in commits_list:
    #         try:
    #             files = commit.files
    #             file_datetime = commit.commit.committer.date
    #             for cfile in files:
    #                 self.manage_file_dictionary(cfile, file_datetime)
    #         except Exception as e:
    #             print("Exception occurred...:", commit.html_url, e)
    #     return self.dictionary_files
    
    # def manage_file_dictionary(self, file, fdate):
    #     fstatus = file.status
    #     if fstatus == 'renamed':
    #         filename = None

    #         if self.dictionary_files.get(file.filename) != None:
    #             filename = file.filename
    #         elif self.dictionary_files.get(file.previous_filename) != None:
    #             filename = file.previous_filename

    #         if filename != None:
    #             if self.dictionary_files[filename]['date'] < fdate:
    #                 self.dictionary_files.pop(filename)
    #                 self.dictionary_files[file.filename] = {}
    #                 self.dictionary_files[file.filename]['file'] = file
    #                 self.dictionary_files[file.filename]['date'] = fdate

    #     elif self.dictionary_files.get(file.filename) != None:
    #         if self.dictionary_files.get(file.filename)['date'] < fdate:
    #             self.dictionary_files.pop(file.filename)
    #             self.dictionary_files[file.filename] = {}
    #             self.dictionary_files[file.filename]['file'] = file
    #             self.dictionary_files[file.filename]['date'] = fdate            
    #     else:
    #         self.dictionary_files[file.filename] = {}
    #         self.dictionary_files[file.filename]['file'] = file
    #         self.dictionary_files[file.filename]['date'] = fdate

    def create_directory_system(self, path):
        system_name = self.repo_name.rsplit("/", 1)[1]
        system_dir_name = (path + "/" + system_name) if not path.endswith('/') else (path + system_name)
        if not os.path.exists(system_dir_name):
            os.makedirs(system_dir_name)
            return system_dir_name
        return None
    
    # def reset_dictionary_files(self):
    #     self.dictionary_files = dict()

    # def get_files_not_downloaded(self):
    #     return self.dictionary_files_not_downloaded

    # def download_list_files(self, dict_files, project_dir):
    #     project_dir = (project_dir + "/") if not project_dir.endswith('/') else project_dir
    #     for key in dict_files:
    #         if dict_files[key]['file'].status == 'renamed':

    #             if os.path.exists(project_dir + dict_files[key]['file'].previous_filename):
    #                 os.remove(project_dir + dict_files[key]['file'].previous_filename)

    #                 dir_file = (project_dir + dict_files[key]['file'].previous_filename.rsplit("/", 1)[0]) if "/" in dict_files[key]['file'].previous_filename else (project_dir)
    #                 if not os.listdir(dir_file):
    #                     os.rmdir(dir_file)
    #             if os.path.exists(project_dir + dict_files[key]['file'].filename):
    #                 os.remove(project_dir + dict_files[key]['file'].filename)

    #                 dir_file = (project_dir + dict_files[key]['file'].filename.rsplit("/", 1)[0]) if "/" in dict_files[key]['file'].filename else (project_dir)
    #                 if not os.listdir(dir_file):
    #                     os.rmdir(dir_file)

    #             self.download_file(dict_files[key]['file'], project_dir)
                
    #         elif dict_files[key]['file'].status == 'removed':
                
    #             if os.path.exists(project_dir + dict_files[key]['file'].filename):
    #                 os.remove(project_dir + dict_files[key]['file'].filename)
                    
    #                 dir_file = (project_dir + dict_files[key]['file'].filename.rsplit("/", 1)[0]) if "/" in dict_files[key]['file'].filename else (project_dir)
    #                 if not os.listdir(dir_file):
    #                     os.rmdir(dir_file)

    #         else:
    #             if os.path.exists(project_dir + dict_files[key]['file'].filename):
    #                 os.remove(project_dir + dict_files[key]['file'].filename)
                    
    #                 dir_file = (project_dir + dict_files[key]['file'].filename.rsplit("/", 1)[0]) if "/" in dict_files[key]['file'].filename else (project_dir)
    #                 if not os.listdir(dir_file):
    #                     os.rmdir(dir_file)

    #             self.download_file(dict_files[key]['file'], project_dir)
    
    # def download_file(self, file, project_dir):
    #     file_dir = file.filename.rsplit("/", 1)[0] if "/" in file.filename else ""
    #     path = (project_dir + "/" + file_dir) if not project_dir.endswith('/') else (project_dir + file_dir)
    #     number_release = project_dir.rsplit("/", 1)[1] if not project_dir.endswith('/') else project_dir.rsplit("/", 2)[1]

    #     if not os.path.exists(path):
    #         os.makedirs(path)
            
    #     try:
    #         filename = (path + "/" + file.filename.rsplit("/", 1)[1]) if "/" in file.filename else (path + file.filename)
    #         # print(filename)
    #         urllib.request.urlretrieve(file.raw_url, filename)
    #         # wget.download(file.raw_url, path)
    #     except:
    #         filename = (path + "/" + file.filename.rsplit("/", 1)[1]) if "/" in file.filename else (path + file.filename)
    #         print(file.raw_url)
    #         print(filename)
    #         if(self.dictionary_files_not_downloaded.get(number_release) != None):
    #           self.dictionary_files_not_downloaded[number_release][file.filename] = file.raw_url
    #         else:
    #           self.dictionary_files_not_downloaded[number_release] = {}
    #           self.dictionary_files_not_downloaded[number_release][file.filename] = file.raw_url
    #         print("Could not download of the file.....:", file.filename)
