# DSTool

To run the tool for extracting versioned systems from the GitHub, it is necessary run the python scripts existing in the `release_extraction` folder. To run this application, it must be used the following command:

```
python3 runner.py <repository name on GitHub> <time frame of each release in days, 0=automatic selection (14 days)> <path to save the output files>
```

`Repository name on GitHub` refers to the name of the project repository on GitHub. For instance, you need to provide "bethrobson/Head-First-Design-Patterns" if you want to download the project "https://github.com/bethrobson/Head-First-Design-Patterns". The `time frame of each release in days` parameter tells the tool the number of whose each extracted release will have. If you indicate "14" as a parameter, each release will have source code for a period of 14 days. Finally, `Path to save the output files` parameter refers to the directory where CK will export the versioned source code extracted from the GitHub.


**&ast;&ast;IMPORTANT&ast;&ast;:** 

Before running the tool, we have to create a properties file inside the `config` folder. The file must be named as `ConfigFile.properties` and it must have the following content: 
```
[DatabaseSection]
config.token = d1a3419f5fc17376a6cacbb2a28c6c923cadb9f7
```

`Config token` is a personal access token that have to be generated on the GitHub platform. This token is individual and must not be shared with other people. 