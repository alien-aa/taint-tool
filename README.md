## **taint-tool**

This repository contains materials on a practical task dedicated to exploring the possibilities of static taint analysis for Android applications.

The purpose of the assignment is to study and practice the methods of static taint analysis to identify security vulnerabilities in Android applications.

**Repository structure**

- [analysis.py](http://analysis.py/) -developed Python script.
- config/ - folder with configuration files such as
the default file is "SourcesAndSinks".txt"
- platform-tools/ - the default "platforms" directory for Android
- FlowDroid-2.13/ - FlowDroid tool

## **Installation Instructions**

**Before the installation**

Before installing, make sure that you have Java Runtime Environment (JRE) version 8 or higher and Python version 3.10 or higher installed.

**Installation**

The software does not require special installation, you only need to download all the directories and files that are in the repository.

You can check the correctness of the installation by executing the command to call help from the directory where all directories and project files are downloaded:

```
 python analysis.py -h
```

```
 python analysis.py --help
```
You can also run the program on the test apk file, which is located in the "examples/" directory using the command:
```
python analysis.py -apk $REPO_LOCATION\examples\air.com.CandySlacking-00019D870F0F42F0803214BE4BF290428CFD6C7290918E6CF8823F318D3BF620.apk
```

## **Instructions for working with software**

To work with the program, you need to run the script from the directory where you downloaded all the directories and files of the project using the command:

```
 python analysis.py -apk <apk-path>
```

Be sure to specify either the -h option to get help or -apk to get started on.

**Available options:**

-h or --help: Displays help about available options.

Required options:

-apk <apk_path>: The path to the APK file to be analyzed.

Optional options:

-p <platform_tools_path>: Path to the platform-tools folder containing the Android SDK tools.

-s <sources_and_links_path>: Path to the file SourcesAndSinks.txt , which defines the sources and sinks of data for analysis.

## **Contact**

If you experience any issues, you can ask for help or contact me at *butina.aa@outlook.com*.
