# 2020/11 Data structure PA#1
# Author: Chien-Kai Ma

from os import listdir
from os.path import isfile, join

# Read query lists
test_file = open("list.txt", "r")
test_string = test_file.read()
test = test_string.splitlines()

# Read pages
# Handle page500
# Produce ReverseIndex
mypath = "web-search-files2"
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
pageCount = len(files)
reverseIndex = dict()
pageToLinks = [[] for _ in range(501)]
pageFromLinks = [[] for _ in range(501)]
prob_w = [0 for _ in range(501)]
prob_r = [1/501 for _ in range(501)]

for file in files:
    pageIdx = int(file[4:])
    # Open file
    page = open(join(mypath, file), "r")
    data_string = page.read()
    data = data_string.split()
    divider = len(data)
    for i in range(len(data)):
        s = data[i]
        if "page" in s and i < divider:
            # Extract page number
            s = int(s[4:])
            pageToLinks[pageIdx].append(s)
            pageFromLinks[s].append(pageIdx)
        elif s == "---------------------":
            divider = i
        else:
            # Read words
            if s in reverseIndex.keys():
                reverseIndex[s].append(pageIdx)
            else:
                reverseIndex[s] = [pageIdx]
        pageToLinks[pageIdx] = sorted(pageToLinks[pageIdx])

def PageRank(d, DIFF, prob_r):
    '''Calculate PageRank and output'''
    diff = 10
    prob_w = [0 for _ in range(501)]
    prob_r = [1/501 for _ in range(501)]
    while diff >= DIFF:
        diff = 0
        for i in range(501):
            prob_w[i] = 0
            for j in pageFromLinks[i]:
                prob_w[i] += d * prob_r[j] / len(pageToLinks[j])
            prob_w[i] += (1-d)/501
            diff += abs(prob_w[i] - prob_r[i])
        prob_r = prob_w
        #print(diff)
    # Produce PageRank
    myPageRank = dict()
    for i in range(len(prob_r)):
        myPageRank[i] = prob_r[i]
    myPageRank = sorted(myPageRank.items(), key=lambda x:x[1], reverse=True)

    # Output PageRank
    PageRankOut = open("pr_{}_{:0>3}.txt".format(int(d*100), int(DIFF*1000)), "w")
    for i in myPageRank:
        prob_str = round(prob_r[i[0]], 7)
        prob_str = '{:<09}'.format(prob_str)
        prob_str = prob_str[1:]
        PageRankOut.write("page{}\t{}\t{}\n".format(i[0], len(pageToLinks[i[0]]), prob_str))
    PageRankOut.close()
    searchAll(d, DIFF, prob_r)
    return prob_r

def search(command, testOut, prob_r):
    command = command.split()
    if len(command) == 1:
        if command[0] in reverseIndex:
            # TODO: Print the top ten hits
            count = 0
            values = dict()
            for j in reverseIndex[command[0]]:
                values[j] = prob_r[j]
            mySort = sorted(values.items(), key=lambda x:x[1], reverse=True)
            for j in mySort:
                if count < 10:
                    testOut.write("page{} ".format(j[0]))
                    count += 1
                else: break
            testOut.write("\n")
        else:
            testOut.write("none\n")
    else:
        init = False
        AND_set = set()
        OR_set = set()
        for word in command:
            if init == False:
                if word in reverseIndex:
                    AND_set = set(reverseIndex[word])
                init = True
            if word in reverseIndex:
                AND_set = AND_set & set(reverseIndex[word])
                OR_set = OR_set | set(reverseIndex[word])
            else:
                AND_set = set()
        # Print the top ten hits AND
        testOut.write("AND ")
        count = 0
        if AND_set is set():
            testOut.write("none")
        # Sort the pages
        AND_values = dict()
        for j in AND_set:
            AND_values[j] = prob_r[j]
        myAND = sorted(AND_values.items(), key=lambda x:x[1], reverse=True)
        for j in myAND:
            if count < 10:
                testOut.write("page{} ".format(j[0]))
                count += 1
            else: break
        testOut.write("\n")

        # Print the top ten hits OR
        testOut.write("OR ")
        count = 0
        if OR_set is set():
            testOut.write("none")
        # Sort the pages
        OR_values = dict()
        for j in OR_set:
            OR_values[j] = prob_r[j]
        myOR = sorted(OR_values.items(), key=lambda x:x[1], reverse=True)
        for j in myOR:
            if count < 10:
                testOut.write("page{} ".format(j[0]))
                count += 1
            else: break
        testOut.write("\n")
def searchAll(d, DIFF, prob_r):
    testOut = open("result_{}_{:0>3}.txt".format(int(d*100), int(DIFF*1000)), "w")
    for cmd in test:
        search(cmd, testOut, prob_r)
    testOut.close()

prob_r = PageRank(0.25, 0.100, prob_r)
prob_r = PageRank(0.25, 0.010, prob_r)
prob_r = PageRank(0.25, 0.001, prob_r)
prob_r = PageRank(0.45, 0.100, prob_r)
prob_r = PageRank(0.45, 0.010, prob_r)
prob_r = PageRank(0.45, 0.001, prob_r)
prob_r = PageRank(0.65, 0.100, prob_r)
prob_r = PageRank(0.65, 0.010, prob_r)
prob_r = PageRank(0.65, 0.001, prob_r)
prob_r = PageRank(0.85, 0.100, prob_r)
prob_r = PageRank(0.85, 0.010, prob_r)
prob_r = PageRank(0.85, 0.001, prob_r)

# Output reverseIndex
ReverseIndexOut = open("reverseindex.txt", "w")
reverseIndex_keys = sorted(reverseIndex)
for i in reverseIndex_keys:
    '''
    # Sort the pages
    reverseIndex_values = dict()
    for j in reverseIndex[i]:
        reverseIndex_values[j] = prob_r[j]
    myReverseIndex = sorted(reverseIndex_values.items(), key=lambda x:x[1], reverse=True)
    reverseIndex[i] = [j[0] for j in myReverseIndex]
    '''
    # Write to the file
    ReverseIndexOut.write(i)
    ReverseIndexOut.write('\t')
    #for j in myReverseIndex:
    reverseIndex[i] = set(reverseIndex[i])
    for j in reverseIndex[i]:
        ReverseIndexOut.write("page{} ".format(j))
    ReverseIndexOut.write('\n')
ReverseIndexOut.close()


# Search engine
command = input("PageRank> ")
while (command != "*end*"):
    command = command.split()
    if len(command) == 1:
        if command[0] in reverseIndex:
            # TODO: Print the top ten hits
            count = 0
            values = dict()
            for j in reverseIndex[command[0]]:
                values[j] = prob_r[j]
            mySort = sorted(values.items(), key=lambda x:x[1], reverse=True)
            for j in mySort:
                if count < 10:
                    print("page{} ".format(j[0]), end='')
                    count += 1
                else: break
            print()
        else:
            print("none")
    else:
        init = False
        AND_set = set()
        OR_set = set()
        for word in command:
            if init == False:
                if word in reverseIndex:
                    AND_set = set(reverseIndex[word])
                init = True
            if word in reverseIndex:
                AND_set = AND_set & set(reverseIndex[word])
                OR_set = OR_set | set(reverseIndex[word])
            else:
                AND_set = set()
        # Print the top ten hits AND
        print("AND ", end='')
        count = 0
        if AND_set is set():
            print("none", end='')
        # Sort the pages
        AND_values = dict()
        for j in AND_set:
            AND_values[j] = prob_r[j]
        myAND = sorted(AND_values.items(), key=lambda x:x[1], reverse=True)
        for j in myAND:
            if count < 10:
                print("page{} ".format(j[0]), end='')
                count += 1
            else: break
        print()

        # Print the top ten hits OR
        print("OR ", end='')
        count = 0
        if OR_set is set():
            print("none", end='')
        # Sort the pages
        OR_values = dict()
        for j in OR_set:
            OR_values[j] = prob_r[j]
        myOR = sorted(OR_values.items(), key=lambda x:x[1], reverse=True)
        for j in myOR:
            if count < 10:
                print("page{} ".format(j[0]), end='')
                count += 1
            else: break
        print()
    command = input("PageRank> ")
