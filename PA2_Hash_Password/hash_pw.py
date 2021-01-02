# 2020/12 Data structure PA#2
# Author: Chien-Kai Ma

from os import listdir
from os.path import isfile, join

# Read all passwords
pw_filename = input("Enter the name of password file: ")
pw_file = open(pw_filename, 'r')
pw_str = pw_file.read()
pw_list = pw_str.splitlines()
pw_list = [pw for pw in pw_list if len(pw) == 6]

# Generate all possible 3-digit salt
salt_list = range(0, 1000)
salt_list = ['{:>03}'.format(str(salt)) for salt in salt_list]

def hash_cal(salt, pw_left, pw_right):
    return (24300000 * int(salt) + 243 * int(pw_left) + int(pw_right)) % 85767489

# Generate dictionary file
pw_hash_dict = {}
for pw in pw_list:
    pw_num = ""
    for c in pw:
        pw_num += str(ord(c))
    pw_hash_dict[pw] = []
    for salt in salt_list:
        hash_val = hash_cal(salt, pw_num[:5], pw_num[5:])
        pw_hash_dict[pw].append(hash_val)

DictOut = open("Dictionary.txt", "w")
for pw in pw_list:
    for i in range(1000):
        DictOut.write(pw)
        DictOut.write(" ")
        DictOut.write(salt_list[i])
        DictOut.write(" ")
        DictOut.write(str(pw_hash_dict[pw][i]))
        DictOut.write("\n")
DictOut.close()

def hash_search(hash_val_in):
    search_count = 0
    for pw in pw_list:
        for i in range(1000):
            search_count += 1
            if pw_hash_dict[pw][i] == int(hash_val_in):
                return (pw, i, search_count)
    return False

test_prompt = input("Do you want to test hash value file? (Yes/No) ")
if test_prompt == "Yes":
    test_file = open("list_pa2.txt", 'r')
    test_str = test_file.read()
    test_list = test_str.splitlines()
    result_file = open("result_pa2.txt", 'w')
    # TODO Search and write out
    
    for hash_val_in in test_list:
        search_result = hash_search(hash_val_in)
        if (search_result != 0):
            result_file.write(hash_val_in)
            result_file.write(" ")
            result_file.write(search_result[0])
            result_file.write(" ")
            result_file.write(salt_list[search_result[1]])
            result_file.write(" ")
            result_file.write(str(search_result[2]))
        else:
            result_file.write(hash_val_in)
            result_file.write(" ")
            result_file.write("******")
            result_file.write(" ")
            result_file.write("***")
            print("Search failed!")
            print("Have Searched 100000 entries.")
        result_file.write("\n")
    result_file.close()
else:
    print("Skip the test file...")
    print()

hash_val_in = input("Enter a hash value: ")
while hash_val_in != "":
    search_result = hash_search(hash_val_in)
    if (search_result != 0):
        print("Search succeeded!")
        print("Password: {}".format(search_result[0]))
        print("Salt    : {}".format(salt_list[search_result[1]]))
        print("Have Searched {} entries.".format(search_result[2]))
        print()
    else:
        print("Search failed!")
        print("Have Searched 100000 entries.")
        print()
    hash_val_in = input("Enter a hash value: ")
