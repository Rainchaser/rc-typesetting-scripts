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
The scribus scripts have been developed using python 3.8 (once available!)

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
The simplest option is to download the entire repository via Code → Download zip and then
delete the files that you don't want to keep.

Once downloaded, the scripts can be launched from the commandline via 
`python <script name> <arguments>` from the directory containing the script that you wish to run.

### AO3 scripts
These are intended to work with files downloaded from [AO3](https://archiveofourown.org/). The files must have been 
generated from the download option, rather than "view source" and then copy/paste, as the formatting 
is different.

#### ao3_clean_html
This script takes two arguments:  
* source file - path (local or absolute) to the html file that is to be processed  
* output directory - the destination folder where processed files should be generated

#### ao3_chapnum_format
This script edits the format of chapter headings in an html file that has been edited using the 
ao3_clean_html. It can:
* set the prefix (e.g. Chapter, Ch, or any other character)
* change the style of numbering (14, fourteen, XIV) 
* change the case (UPPER, lower or Title)
* remove the numbering and use title only (if present)
* remove the title and use numbering only
* split number and title onto separate lines
* skip a set number of chapters before starting to number OR start the chapter numbering at a higher
 value (e.g. number the second chapter as 1, or number the first chapter as 4. It can't do both together)
* add ornaments after the heading, and between chapter and title if they are split onto separate lines.

The script has two mandatory arguments and eight optional arguments. The mandatory arguments are: 
* source file - path (local or absolute) to the html file that is to be processed  
* output directory - the destination folder where processed files should be generated

These must be passed in the order source file, output directory.

To get a list of the optional arguments and the flags to use with them, you can run the script with 
no arguments to get a basic list. You can also pass -h or --help as an argument to get the full 
description of all the arguments. The argument flags all have a short and a long form, e.g.  
* python ao3_chapnum_format.py -h 
    * (to get the detailed argument list)  
* python ao3_chapnum_format.py /path/to/file.html /path/to/dir -p Chapter --suffix=:  
    * (to set the prefix to "Chapter" and the suffix to ":")

Some values may need to be wrapped in double-quotes (***not*** single quotes) to be passed as an 
argument, e.g. --suffix="|"