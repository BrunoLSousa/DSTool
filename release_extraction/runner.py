# runner.py

from github import Github
from datetime import datetime, timedelta, timezone
import os
import shutil
from logger import Logger
from extractor import Extractor
import sys
from validator import Validator
import subprocess

try:
    from subprocess import DEVNULL, STDOUT, check_call
except ImportError:
    DEVNULL = open(os.devnull, 'wb')

class Runner:

    def __init__(self, repo_name, interval, output):
        self.repo_name = repo_name
        self.interval = interval
        self.root = output
        self.ex = Extractor(repo_name, interval)

    def start(self):
        project_path = self.ex.create_directory_system(self.root)
        if project_path != None:
            # Fazer o clone do projeto aqui como um .nome_do_projeto
            clone_project_dir = self.clone_repository(project_path)
            self.identify_project_lifetime()
            time_frames_project = self.extract_time_frames()
            self.construct_releases(clone_project_dir, time_frames_project, project_path)
            # print("ok")
        else:
            print("Warning.....: Directory already existing at", self.root, "!!!")

    def extract_time_frames(self):
        print("Identifying the time frame of the project releases...")

        since = self.begin
        release = 0
        time_frame_releases = dict()

        while (since + timedelta(days=self.interval)) < self.end:

            time_frame = self.ex.define_timeframe(since)
            time_frame_releases[release] = {}
            time_frame_releases[release]['since'] = time_frame["since"]
            time_frame_releases[release]['until'] = time_frame["until"]
            time_frame_releases[release]['commit_most_recent'] = self.ex.get_commit_most_recent(time_frame["since"], time_frame["until"])
            since = time_frame["until"] + timedelta(days=1)
            release = release + 1

            # if release == 1:
            #     print(time_frame_releases)
            #     break
        
        print("Done!\n")

        return time_frame_releases


    def construct_releases(self, clone_project_dir, time_frames, project_path):
        
        since = self.begin
        for key in time_frames:
            release_number = key + 1
            print("------------------------ Building the release " + str(release_number) + " out of " + str(len(time_frames)) + " ------------------------\n")

            # release_dir = self.create_release_directory(time_frames[key]["commit_most_recent"], clone_project_dir, project_path, release_number)

            # print("Identifying the commits list between", time_frames[key]["since"], "and", time_frames[key]["until"], "...")
            # print("Building the release", str(release_number), "of the project in", project_path, "...")

            release_dir = self.create_release(time_frames[key], clone_project_dir, project_path, release_number)
            # self.checkout_release(time_frames[key]["commit_most_recent"], release_dir)

            logger = Logger()
            logger.release_time_frame(time_frames[key]["since"].strftime("%Y-%m-%d %H:%M:%S"), time_frames[key]["until"].strftime("%Y-%m-%d %H:%M:%S"), release_dir, "timeframe.log")


            # commits_list = self.ex.get_commits_timeframe(time_frames[key]["since"], time_frames[key]["until"])
            # print("Done!\n")
            # print("Analyzing the source code files in the commits list", "...")
            # dict_files = self.ex.process_commits_list(commits_list)
            # print("Done!\n")
              
            # print("Building the release", str(release_number), "of the project in", project_path, "...")
            # self.ex.download_list_files(dict_files, release_dir)

            print("\nRelease built!!!\n")

        # print("\nSaving log...\n")
        # self.log_files_not_downloaded(project_path)
        print("\nBuilding of the project finished!!!\n")











    # alterar essa função para que ela possa copiar a pasta de backup para a respectiva versão e fazer o checkout com o commit mais recente detectado. 
    # def construct_releases(self, time_frames, project_path):
        
    #     since = self.begin
    #     for key in time_frames:
    #         release_number = key + 1
    #         print("------------------------ Release " + str(release_number) + " out of " + str(len(time_frames)) + " ------------------------\n")

    #         release_dir = self.create_release_directory(project_path, release_number)

    #         print("Identifying the commits list between", time_frames[key]["since"], "and", time_frames[key]["until"], "...")

    #         logger = Logger()
    #         logger.release_time_frame(time_frames[key]["since"].strftime("%Y-%m-%d %H:%M:%S"), time_frames[key]["until"].strftime("%Y-%m-%d %H:%M:%S"), release_dir, "timeframe.log")

    #         commits_list = self.ex.get_commits_timeframe(time_frames[key]["since"], time_frames[key]["until"])
    #         print("Done!\n")
    #         print("Analyzing the source code files in the commits list", "...")
    #         dict_files = self.ex.process_commits_list(commits_list)
    #         print("Done!\n")
              
    #         print("Building the release", str(release_number), "of the project in", project_path, "...")
    #         self.ex.download_list_files(dict_files, release_dir)

    #         print("\nRelease built!!!\n")

    #     print("\nSaving log...\n")
    #     self.log_files_not_downloaded(project_path)
    #     print("\nBuilding of the project finished!!!\n")


    def create_release(self, time_frame, clone_project, project_path, release_number):
        release_dir = (project_path + "/" + str(release_number)) if not project_path.endswith('/') else (project_path + str(release_number))
        if time_frame["commit_most_recent"] == None:
            # pass
            src = (project_path + "/" + str(release_number-1)) if not project_path.endswith('/') else (project_path + str(release_number-1))
            destination = shutil.copytree(src, release_dir) 
        else:
            destination = shutil.copytree(clone_project, release_dir) 
            self.checkout_release(time_frame["commit_most_recent"], release_dir)
        
        return release_dir
        
        
        
        
        



    # def create_release_directory(self, commit_sha, clone_project, project_path, release_number):
    #     release_dir = (project_path + "/" + str(release_number)) if not project_path.endswith('/') else (project_path + str(release_number))
    #     # print(clone_project)
    #     # print(release_dir)
    #     if commit_sha == None:
    #         pass
    #     else
    #         destination = shutil.copytree(clone_project, release_dir)  
    #     # if(release_number > 1):
    #         # src = (project_path + "/" + str(release_number-1)) if not project_path.endswith('/') else (project_path + str(release_number-1))
        
    #         # self.ex.reset_dictionary_files()
    #     # else:
    #         # os.makedirs(release_dir)
        
    #     return release_dir

    def clone_repository(self, project_path):
        print("\nGetting the project from GitHub!!!\n")
        clone_url = self.ex.get_clone_url()
        # print(clone_url)
        clone_dir = (project_path + "/." + project_path.rsplit("/", 1)[1]) if not project_path.endswith('/') else (project_path + "." + project_path.rsplit("/", 1)[1])
        # print(clone_dir)
        try:
            p = subprocess.Popen(['git', 'clone', clone_url, clone_dir], stdout=DEVNULL, stderr=DEVNULL)
            p.wait()
        except Exception as e:
            print("Exception occurred...: It was not possible to get the project from the GitHub!!!")
        
        return clone_dir
        
    def checkout_release(self, commit_sha, release_dir):

        try:
            p = subprocess.Popen(['git', 'checkout', commit_sha], cwd=release_dir, stdout=DEVNULL, stderr=DEVNULL)
            p.wait()
        except Exception as e:
            print("Exception occurred...: It was not possible to build the release " + release_dir + "!!!")


        


    # def log_files_not_downloaded(self, project_path):
    #     dict_files_not_downloaded = self.ex.get_files_not_downloaded()
    #     logger = Logger()
    #     logger.file_not_downloaded(dict_files_not_downloaded, project_path, "files_not_downloaded.log")



    def identify_project_lifetime(self):
        print("Identifying the life time of the project in GitHub...")
        self.begin = self.ex.get_first_commit_date()
        self.end = self.ex.get_last_commit_date()
        print("Done!\n")



if __name__ == '__main__':

    args = sys.argv

    if len(args) != 4:
        print("Usage python3 runner.py <repository name on GitHub> <time frame of each release in days, 0=automatic selection (14 days)> <path to save the output files>")
    else:
        validator = Validator()
        time_frame = validator.validate_time_frame(args[2])
        if validator.validate_repository_name(args[1]) and time_frame != -1 and validator.validate_output_path(args[3]):
            runner = Runner(args[1], time_frame, args[3])
            runner.start()