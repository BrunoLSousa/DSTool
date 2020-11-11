#extractor.py

import os

class Logger:
    
    # write the initial date and final date of a given release in a specific directory
    def release_time_frame(self, initial_date, final_date, path, filename, release_number):
        directory = (path + "/" + filename) if not path.endswith('/') else (path + filename)
        f = open(directory, "a")
        f.write("----------------------- Version " + str(release_number) + " ----------------------")
        f.write("\n")
        f.write("Initial Date --------------- " + initial_date)
        f.write("\n")
        f.write("Final Date --------------- " + final_date)
        f.write("\n")
        f.write("--------------------------------------------------------")
        f.write("\n")
        f.write("\n")
        f.close()
    
    # write a message in case it is not able to download a given file to the local directory
    def file_not_downloaded(self, dict_files, path, filename):
        if len(dict_files) > 0:
            directory = (path + "/" + filename) if not path.endswith('/') else (path + filename)
            f = open(directory, "w")
            for release in dict_files:
                f.write("------------------------ Release " + release + " ------------------------\n")
                for key in dict_files[release]:
                    f.write("File not downloaded...: " + key + " --- " + dict_files[release][key] + "\n")
            f.close
                

    

    

    