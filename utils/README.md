# Utils overview

The utils folder contains all (or at least, as many as possible) of the functions 
that aren't tied to a specific script, and are likely to be reused between scripts.

They have broadly been split up by function:
* __init__ - various enums relating to HTML, punctuation, etc. It also 
contains a method for creating an argument parser to handle optional arguments on 
the commandline.
* file_utils - functions relating to files such as writing to file.
* html_utils - functions relating to manipulating html via lxml.html
* number_utils - functions relating to handling numbers, such as converting into 
roman numerals
* popup_utils - functions relating to tkinter popups used in some of the scripts
* string_utils - functions relating to string manipulation

## How to use
Import into a script located on the same level:  
```import <filename>```

Import into a script located one level up:  
```import utils/<filename>```  
or for functions in the init file:  
```import utils.<function>```

If you want to import into a script that is not located in a folder somewhere on 
filepath leading to the utils folder (e.g. if the path is /a/b/c/utils, and you want 
to import to /a/b/d) then you will need to amend the configured python path in your 
computer settings.