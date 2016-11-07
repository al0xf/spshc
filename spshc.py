#  Copyright 2013 Christoffer
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

#spshc - Simple Python Site Hash Checker
#Prerequisite: execute "pip install requests"
import requests
import hashlib
import pickle
from time import sleep
from tkinter import *

class Site_node(object):
    def __init__(self, url, response_text):
        self.url = url
        self.response_text = response_text.encode("utf-8")

def show_notification(url):
    #Pops up a window to notify the user of a site change.
    master = Tk()
    master.title("Update found")
    a = Label(master, text="A site was updated.", font=("Helvetica", 14)).pack()
    b = Label(master, text=url).pack()
    master.mainloop()

def download(url_list):
    # Downloads the specified sites.
    new_download = []
    print("Visiting sites...")
    for url in url_list:
        try:
            userdata = {"User-Agent" : "spshc 1.0"} #Avoid HTTP error 429 Too Many Requests.
            resp = requests.get(url, data=userdata)
            response_text = resp.text
            print("Got a response from", url, end="")
            site = Site_node(url, response_text)
            new_download.append(site)
        except:
            print("Could not visit", url, end="")

    return(new_download)

def compare(new_download, old_hash):
    #Hashes the new downloads, and compare them against the old one.
    print("\nComparing new site data against old download")
    new_hash = []
    notification_text = ""
    update_found = False
    for site in new_download:
        site_hash = hashlib.md5(site.response_text).hexdigest()
        new_hash.append(site_hash)

        if site_hash not in old_hash and old_hash != []:
            print("Site update found at", site.url)
            notification_text += (site.url+"\n")
            update_found = True

    pickle.dump(new_hash, open("old_hash.dat", "wb"))
    print("Saved hashes for current sites.")
    
    if update_found:
        show_notification(notification_text)


def read_data():
    # Reads old saved site hashes, and the list of sites to check.
    print("Reading saved hash data")
    try:
        old_hash = pickle.load(open("old_hash.dat", "rb"))
        print("Loaded saved hash data")
            
    except FileNotFoundError:
        print("old_hash.dat not found, assuming first run and creating a new file.")
        old_hash = []

    print("Reading the URL list")
    try:
        with open("url_list.txt", "r") as url_list_file:
            url_list = []
            for line in url_list_file:
                if line[0] != "#":
                    url_list.append(line)

    except FileNotFoundError:
        print("Empty url_list.txt file! Put some sites in a plain text file named 'url_list.txt' and try again.")
        quit()

    return old_hash, url_list

def read_wait_time():
	#Reads the wait time after each check if it exists. 
    try:
        time_file = open("wait_time.txt", "r")
        wait_time = int(time_file.readline())
        if wait_time > 0:
            return wait_time
        else:
            raise ValueError("We can't work with negative time... yet.")
    except:
        print("No valid wait time specified. The file 'wait_time.txt' should only cointain a positive integer: the number of seconds to wait.\nDefaulting to 15 minutes.")
        return 15*60

def main():
    #The main loop.
    wait_time = read_wait_time()
    while True:
        old_hash, url_list = read_data()
        new_download = download(url_list)
        compare(new_download, old_hash)
        print("Loop completed. Going to sleep for ", end="")
        if(wait_time < 60):
            print(wait_time, "seconds...\n")
        else:
            print(wait_time//60, "minutes...\n")
        sleep(wait_time)
    
main()
