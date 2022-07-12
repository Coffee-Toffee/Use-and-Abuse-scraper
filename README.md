U&A Curlie scraper
=================================================

This scraper, for the Use and Abuse of Personal Information project, is designed to comprehensively and recursively scraper curlie.org


Table of contents
-----------------

* [Introduction](#introduction)
* [Installation](#installation)
* [Usage](#usage)
* [Known issues and limitations](#known-issues-and-limitations)
* [Getting help](#getting-help)
* [License](#license)
* [Authors and history](#authors-and-history)
* [Acknowledgments](#acknowledgments)


Introduction
------------

The scraper was designed to get the contents of Curlie, a very large directory of websites, and to then provide a readable output of the
external sites, and the catagories under which they fall.

Installation
------------

Required Operating System:
Linux
(Both Manjaro and Ubuntu are confirmed to work).
Windows is not supported.

Installing dependences:

with pip:
```bash
pip (or pip3) install beautifulsoup4
```

Usage
-----

Run this command first, setting the stack size.
```bash
ulimit -s 2000000
```

Then, to run:
```bash
python (or python3) main.py
```
(You care about the dict_a_b.txt files, in the output)

### Basic operation
(If you have multiple machines, then for each machine)

1. Clone/Download the repository
2. Download dependancies
3. Set the stack size 
4. Make sure that the catagory and subcatagory id numbers are correct
5. Run it.

Known issues and limitations
----------------------------

The dict.txt currently is not fully functional
(Am fixing it now)

Getting help
------------

Email me at jackbh@vt.edu, or jbharrison@wm.edu

License
-------

GNU General Public License v3.0

Authors and history
---------------------------

I wrote all of it, except for in the backup_parser, the get_path function, which was written by Joe Harrison.

Any contributions are welcome, however.

Acknowledgments
---------------

Funding provided by:
Virginia Tech National Security Institute

Main external library used:
Beautiful soup
