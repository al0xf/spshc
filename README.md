#spshc
###Simple Python Site Hash Checker
##Introduction
spshc, Simple Python Site Hash Checker, takes any number of websites from a list, and checks to see if these have been updated since the last check. This is accomplished by hashing the downloaded site, and comparing the new hash against an old one. If an update is found, a popup window is shown.
The script is written in Python 3, and should work in any environment capable of showing the TkInter GUI.
##Setup
[Install the Python library 'requests'.](https://github.com/kennethreitz/requests)
 Simply:
``` bash
    $ pip install requests
``` 
##How to use spshc
Create an empty .txt file named 'url_list.txt', and insert links to web pages, one on each line.
Optionally create an empty .txt file named 'wait_time.txt', and enter the number of seconds to wait between each check. The default wait time is 15 minutes if this file is not provided.
Run the script with:
``` bash
    $ python3 spshc.py
```
 