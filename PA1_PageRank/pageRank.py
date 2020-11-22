# 2020/11 Data structure PA#1
# Author: Chien-Kai Ma

from os import listdir
from os.path import isfile, join
mypath = "web-search-files2"
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# Read pages
# TODO: handle page500
# TODO: produce PageRank
# TODO: produce ReverseIndex
pageCount = len(files)
reverseIndex = dict()
for file in files:
    #print(file)
    pageIdx = file[4:]
    # Open file
    page = open(join(mypath, file), "r")
    data_string = page.read()
    data = data_string.split()
    divider = len(data)
    for i in range(len(data)):
        s = data[i]
        if "page" in s and i < divider:
            # Extract page number
            s = s[4:]
            if int(s) > pageCount-1:
                # Handle page500
                print(s, " didn't exist in previous data!")
        elif s == "---------------------":
            divider = i
        else:
            # TODO: read words
            # TODO: handle strange words
            # like Trincomalee, observer--excellent, high-power, page97
            # TODO: Sort the list inside after pageRank is calculated?
            if s in reverseIndex.keys():
                reverseIndex[s].append(pageIdx)
            else:
                reverseIndex[s] = [pageIdx]

# TODO: Output reverseIndex

# Search engine
command = input("PageRank> ")
while (command != "*end*"):
    if True:
        # single input
        # TODO: print the top ten hits
        print("true")
    else:
        # TODO: print the top ten hits AND
        print("else")
        # TODO: print the top ten hits OR
    command = input("PageRank> ")
