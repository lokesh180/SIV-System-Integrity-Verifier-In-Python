"""
In this module the Initialization is defined, where all the information of files and directories are saved to verfication file and details in report file.
"""
#importing Required modules and packages
import os
import sys
import stat
import time
import json
from required_functions import isdirexist, creating_files, get_information, hash_message #importing the required function module

# Initialization Function
def initialization(arguments):
    
    # Declaration of Required Variables
    file_count = 0
    directory_count = 0
    json_file = ""
    file_information_dict = {}
    message = ""

    #checking if the given directory is exists or not
    if not isdirexist(arguments.Directory):
        #if not exit
        sys.exit()

    #Cheking the verification and report files existance, Creating if not while Initialization.
    creating_files(arguments.Directory,arguments.Verification_file, arguments.Report_file,"init")

    #starting the time before iterating between files and directories..    
    start = time.time()  
    #This is main Heart of the Initailization module.
    """
    The below "Nested for loop" will be make iteration between all files and directories in the Given Monitery Directory.
    The first "for loop" is doing the operations on all files.
    The second "for loop" will be working on all the directories.
    Intially If we consider one file then the file path is stored in a variable and then the size, owner, group, permissions, last modified date and hash message of the 
    file is stored to variables. Then dumping the data of file to json (data structure).
    Similarly, If we consider one directory then the file path is stored in a variable and then the size, owner, group, permissions, and last modified date of the 
    file is stored to variables. Then dumping the data of file to json file (data structure).
    After writing the details of all files and directories to json file then those details are transfered to Verification File.
    In the middle of loop the count of both files and directories are stored and then used for Report File.
    The path of directory and verification file, count of directories and files, time for Intialization will be stored in Report File
    """
    for subdirs, dirs, files in os.walk(arguments.Directory):
        #Iteration for all files
        for filename in files:
            file_path = subdirs + os.sep + filename
            size,owner,group,permission,last_modified = get_information(file_path)
            message=hash_message(arguments.Hash_function,file_path)
            file_information_dict[file_path] = {"File Path": file_path,"File Size": size,"File Owner": owner,"File Group": group,"File Permissions": permission,"File Last Modified Date": last_modified,"Message": message,"Hash Function": arguments.Hash_function}
            file_count += 1
            json_file = json.dumps(file_information_dict, indent=4)

        #Iteration for all directories
        for dir in dirs:
            directory_path = subdirs + os.sep + dir
            size,owner,group,permission,last_modified = get_information(directory_path)
            file_information_dict[directory_path] = {"Directory Path": directory_path,"Directory Size": size,"Directory Owner": owner,"Directory Group": group,"Directory Permissions": permission,"Directory Last Modification Date": last_modified}
            directory_count += 1
            json_file = json.dumps(file_information_dict, indent=4)

    #Time end
    end = time.time()   
    #Opening verification file and writing json file in it
    with open(arguments.Verification_file,  "w") as the_file:
        the_file.write(json_file)
        print("Verification file Generated-->",end='')

    #Dumping the report details to json file
    json_report = json.dumps({"Directory Path": arguments.Directory,"Verification File Path": os.path.abspath(arguments.Verification_file) ,"Number of Directories": directory_count,"Number of Files": file_count,"Time to finish the initialization mode": (end-start)*1000}, indent=4)

    #Opening report file and writing json file in it
    with open(arguments.Report_file, "w") as the_file:
        the_file.write(json_report)
        print("Report file Generated")
        
