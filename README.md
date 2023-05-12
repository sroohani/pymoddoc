# pymoddoc
Simple Python script to extract docstrings from Python modules

## Disclaimer
I am not a Python developer. There may be better ways to extract the documentation, but this script is the outcome of googling and some trial and error.

## Motivation
Since I wasn't able to find Bitbake Python API documentation, I wrote this script to extract docstrings from Bitbake modules. But it should be usable to extract docstrings from any Python module.

## Usage
Simply clone the repository or download pymoddoc.py and place it somewhere in your OS path.Then you can run it from a shell prompt.

Here is a description of how you can invoke it:

```
$ pymoddoc COMMAND PARAMETERS
``` 

### COMMAND
COMMAND can be one of the following:

#### list
Lists all available modules.

#### gen
Generates text based on the docstrings in the modules

### PARAMETERS
For  **list** there can be only one of the following parameters:

- *name* List all module names
- *ispkg* List whether or not the module is a package (True/False)
- *all* List all module properties. Currently only *name* and *ispkg*

For **gen** it can be a list of module names to extract the documentation

## Examples

Extracting the documentation of all modules:

```
$ pymoddoc gen
```

Listing the names of installed modules:

```
$ pymoddoc list name
```

Listing the all properties of installed modules:

```
$ pymoddoc list all
```

Listing all properties of Bitbake *bb* and *bblayers* modules:

```
$ pymoddoc list bb bblayers
```

Extracting the documentation of Bitbake *bb* and *bblayers* modules:

```
$ pymoddoc gen bb bblayers
```
 
## Notes
- The script prints to STDOUT. So, you might want to redirect its output to a file:

```
$ pymoddoc list bb bblayers > modules-doc
```
- The structure of the output is as follows:

> ======== MODULE_NAME ========
>
> MODULE DOCUMENTATION
>
> ======== MODULE_NAME ========
>
> MODULE DOCUMENTATION
>
> .  
> .  
> .

In case it cannot find a module, instead of MODULE DOCUMENTATION, it will print the following message:

> Module not found

- This script has only been tested on a Debian 11 machine with Python 3.9.2.
