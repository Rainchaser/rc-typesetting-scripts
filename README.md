# Utility Scripts for Typesetting Books

This is a collection of python scripts intended to help with preparing documents for 
typesetting, in particular for use alongside Scribus.

A number of these scripts are refactored versions of ones created by 
[notwhelmedyet](https://github.com/notwhelmedyet) which can be found in  
their [Scribus Typesetting](https://github.com/notwhelmedyet/ScribusTypesetting) repository.

Additional Scribus scripts can be found in 
[Ale's Scribus Script repository](https://github.com/aoloe/scribus-script-repository)

## Python version
The commandline scripts have been developed using python 3.14  
The scribus scripts have been developed using python 3.8

## Dependencies
The commandline scripts use the lxml 6.0.2 library, which is not currently bundled with Scribus
(as of version 1.6.5). Some options to try enabling lxml within scribus are:

1. Follow the instructions [here](https://wiki.scribus.net/canvas/Windows_Full_Python_Integration) 
to install python on your machine and disable the bundled version of python so that Scribus
will use the system installation instead.
2. In the Scribus script console run the following script.  
On Windows this may result in lxml being installed into 
<user>\appdata\roaming\python\<version>\site-packages - if the scripts fail to run, try copying 
the lxml folders from this location into Program Files\Scribus\python\lib
```
import pip
pip.main(['install', 'lxml'])
```

## Running the scripts
At a minimum you will need to download the script you want to use plus the utils folder. 
The simplest option is to download the entire repository via Code -> Download zip and then
delete the files that you don't want to keep.

Once downloaded, the scripts can either be launched from the commandline via 
`python <script name> <arguments>` from the directory containing the script that you wish to run.

### AO3 scripts
These are intended to work with files downloaded from [AO3](https://archiveofourown.org/).

#### clean_ao3_html
This script takes two arguments:  
    source file - path (local or absolute) to the html file that is to be processed  
    output directory - the destination folder where processed files should be generated