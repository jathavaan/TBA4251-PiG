# TBA4251 Programming in Geomatics - Speed bump detection

_Authors:_ Jathavaan Shankarr

_Date:_ 2021-05-10

## Description

This README file contains the necessary information requrired to run the code. The method and disussion has been presented in the report. The code is written in Python 3.10.8 and has only been tested on a Windows computer running Windows 11. The program should also work for MacOS and Linux, but has not been tested for these operating systems.

## Installation

### Cloning the reposotory

The repository can be cloned by running the following command in the terminal:

```powershell
git clone https://github.com/jathavaan/TBA4251-PiG.git
```

And open the project folder by executing the following command in the terminal:

```powershell
cd TBA4251-PiG
```

### Creating a virtual enviorment and installing dependencies

It is higlhy recommended that you create a virtual enviorment before installing the dependencies. This can be done by running the following command in the terminal:

```powershell
python -m venv venv
```

And then activating the virtual enviorment by running the following command in the terminal:

```powershell
.\venv\Scripts\activate
```

The virtual enviorment has now been activated and the dependencies can be installed by running the following command in the terminal:

```powershell
pip install -r requirements.txt
```

### Adding the LAS- and shapefiles

It is essential that the LAS- and shapefiles are added to the project folder to even be able to run the program. The files have to be inserted into specific directories. The point cloud file to be processed have to be inserted into the following directory:

```powershell
.\resources\point_clouds\raw_files\
```

And the shapefiles have to be inserted into the following directory:

```powershell
.\resources\shapefiles\
```

> **Note** <br>
> The shapefiles and las files are not included in the repository due to the filesize being too large. You have to add the files yourself. The filenames in the [configuration file](src/config.py) has to be updated accordinly if the filenames are different.

The program should now be ready to run.

## Running the program

By default the script will perform the following tasks:

- Pre-processing
- Segmentation
- Detection
- Merging
- Saving the results as a LAS file

The saved LAS file will be saved in the following directory:

```powershell
.\resources\point_clouds\processed_files\
```

To run the program, execute the following command in the terminal:

```powershell
python main.py
```

## Changing the configuration

There are multiple parameters that the user can change in the configuration file. The values have been decided after trial and error, and should not be changed unless the user knows what they are doing.
