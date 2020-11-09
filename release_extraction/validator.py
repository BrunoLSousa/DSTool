# validator.py

from github import Github
import os

class Validator:

    def __init__(self):
        self.auth_github = ""

    def validate_repository_name(self, repository):
        g = Github(self.auth_github)

        try:
            repo = g.get_repo(repository)
        except Exception as e:
            print("Repository not found. Check if its name is correct!!!")
            return False
        return True

    def validate_time_frame(self, time_frame):
        try:
            tf = int(time_frame)
            if tf < 0:
                print("Time frame not supported!!!")
                return -1
            elif tf == 0:
                return 14
            else:
                return tf
        except Exception as e:
            print("Time frame not supported!!!")
            return -1

    def validate_output_path(self, output_path):
        if not os.path.exists(output_path):
            print("Directory not found!!!")
            return False
        return True

# if __name__ == '__main__':

    # validate number of input args

    # val = Validator()
    # print(val.validate_repository_name("PyGithub/PyGithu"))

    # a = "d"

    # print(val.validate_output_path("/home/bruno/Área de Trabalho"))

    # try:
    #     repo = g.get_repo("PyGithub/PyGithu")
    # except Exception as e:
    #     print("Repository not found. Check if its name is correct!!!")
    #     return False
    # return True


    # args = str(sys.argv)
    # if len(args) != 4:
    #     print("Usage python3 runner.py <repository name on GitHub> <time frame of each release in days, 0=automatic selection (14 days)> <path to save the output files>")
    # else: