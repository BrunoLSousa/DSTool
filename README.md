# DSTool

DSTool is a tool that supports to create time series of static software metrics extracted from open source Java systems hosted on GitHub. It is composed of three modules. The present documentation details each one of this module and how they can be run by the users.

## Module 1 - Release Extraction

To run the first module of the tool for extracting versioned systems from the GitHub, it is necessary run the python scripts existing in the `release_extraction` folder. To run this module, it must be used the following command:

```
python3 runner.py <repository name on GitHub> <time frame of each release in days, 0=automatic selection (14 days)> <path to save the output files>
```

`Repository name on GitHub` refers to the name of the project repository on GitHub. For instance, you need to provide "bethrobson/Head-First-Design-Patterns" if you want to download the project "https://github.com/bethrobson/Head-First-Design-Patterns". The `time frame of each release in days` parameter tells the tool the number of whose each extracted release will have. If you indicate "14" as a parameter, each release will have source code for a period of 14 days. Finally, `Path to save the output files` parameter refers to the directory where CK will export the versioned source code extracted from the GitHub.


**&ast;&ast;IMPORTANT&ast;&ast;:** 

Before running this module, we have to create a properties file inside the `config` folder. The file must be named as `ConfigFile.properties` and it must have the following content: 
```
[DatabaseSection]
config.token = d1a3419f5fc17376a6cacbb2a28c6c923cadb9f7
```

`Config token` is a personal access token that have to be generated on the GitHub platform. This token is individual and must not be shared with other people. 


## Module 2 - Metric Collection

To run the second module of the tool for measuring the bi-week releases extracted in the first module, it is necessary run the shell script existing in the `collect_metric` folder. To run this module, it is required the following command:

```
./extractMetrics.sh -i <path to project with source code of the releases> -o <path to save the output files>
```
The `extractMetrics.sh` is the main script of this module. It is responsible for identifying the directories with the releases' source code of the analyzed software and run the CKTool for each release to extract the static metrics values. `Path to project with source code of the releases` refers to the directory where the releases' source code are kept. The `path to save the output files` consists of the directory where the _CSV_ files with metrics value generated by the CKTool will be saved.


## Module 3 - Time Series Generation

To run the third module of the tool for generating the tim series, it is necessary run the python script, `extract_timeseries.py`, existing in the `generate_timeseries` folder. To run this module, it is required the following command:

```
python3 extract_timeseries.py <directory of the versions with system metrics> <path to save the output files>
```
The `extract_timeseries.py` reads the all _CSV_ files with metric values at class level extracted for the releases, and reorganizes the values to generate the time series of the system's classes. `Directory of the versions with system metrics` refers to the directory where the _CSV_ files obtained in the second module are kept. The `path to save the output files` consists of the directory where the _CSV_ files with time series will be saved.

The _CSV_ files with time series generated by this module contain the following pattern. Given a metric _M_ and a system _S_, this module builds a file, where the lines represent the classes of _S_, the columns represent the releases, and each cell _(c,r)_ consists of the metric value of the class _c_ extracted in the release _r_ of the system _S_.