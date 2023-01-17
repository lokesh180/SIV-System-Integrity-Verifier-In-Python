"""
In this module the verification is defined, where all the information of files and directories are verified with verfication file and detailed in report file.
"""
#importing Required modules and packages
import os
import json
import time
from pwd import getpwuid
from grp import getgrgid
import sys
import stat
from hashlib import sha1, md5
from required_functions import isdirexist, creating_files, get_information, hash_message

# Verification Function
def verification(arguments):
    file_count = 0
    directory_counter = 0
    changes = 0
    message_digest = ""

    #checking if the given directory is exists or not
    isdirexist(arguments.Directory)

    #Cheking the verification and report files existance, Creating if not while Initialization.
    creating_files(arguments.Directory,arguments.Verification_file,arguments.Report_file,"verify")

    #The below code is main part in the verification file.
    """
    After Intialization The details of files and subdirectories were stored to the verification file. The created verification file is used to verify 
    if any changes detected. Similar to intilalization we use "nested for loop" for iteration and gather the same details of the files and directories again and 
    comparing the details with verification file. If any changes detected then write the particular change detected and what change to the report file.
    For comparison json is used. Intially verification file is loaded in to json file and then for every file comparing the key values like file size , file owner,...
    and checking the current details, if doesnt match write to report file. The same procedure is repeated for the directories and updated in report file if changes 
    detected. The detailed informantion will be added to report file for changes. Finally The path of directory and verification file, count of directories and files, 
    time for Verification will be stored in Report File
    """
    #Opening Verification file and storing to json file
    with open(arguments.Verification_file) as verification_file:
        verification_json = json.load(verification_file)

    #Opening Report File and write the details of changes.
    with open(arguments.Report_file, "w") as report_file:
        #Start Time 
        start = time.time() 

        for subdir, dirs, files in os.walk(arguments.Directory):
            #Iteration for all files
            for filename in files:
                file_path = subdir + os.sep + filename
                #getting current state and info of the file
                size,owner,group,permission,last_modified = get_information(file_path)

                #Checking the file exists in verification 
                if file_path in verification_json.keys():
                    # if yes Storing the old values of the file.    
                    oldsize = verification_json[file_path]["File Size"]
                    oldowner = verification_json[file_path]["File Owner"]
                    oldgroup = verification_json[file_path]["File Group"]
                    oldpermissions = verification_json[file_path]["File Permissions"]
                    oldlastmodified = verification_json[file_path]["File Last Modified Date"]
                    old_hash_type = verification_json[file_path]["Hash Function"]
                    old_message_digest = verification_json[file_path]["Message"]

                    #If the current info is not same as old info then the following will execute and made detailed info in report file
                    if size != oldsize:
                        report_file.write(
                            "Change Detected : The file " + file_path + " size has been changed\n Old Size : " +str(oldsize)+"\n New Size : "+str(size)+"\n\n")
                        changes += 1
                    
                    if owner != oldowner:
                        report_file.write(
                            "Change Detected : The owner of file " + file_path + " has been changed\n Old Owner : " + oldowner+"\n New Owner : "+ owner+"\n\n")
                        changes += 1
                    if group != oldgroup:
                        report_file.write(
                            "Change Detected : The group of file " + file_path + " has been changed\n Old Group : " + oldgroup+"\n New Group : "+ group+"\n\n")
                        changes += 1
                    if permission != oldpermissions:
                        report_file.write(
                            "Change Detected : The File " + file_path + " has different accesss rights\n Old Permissions : " + oldpermissions +"\n New Permissions : "+ permission+"\n\n")
                        changes += 1
                    if last_modified != oldlastmodified:
                        report_file.write("Change Detected :The File " +file_path + " has different last modified Date or Time\n Old Last Modified : " + oldlastmodified +"\n New Last Modified : "+ last_modified+"\n\n")
                        changes += 1
                    #calling hash message function.
                    message_digest = hash_message(old_hash_type,file_path)
                    if message_digest != old_message_digest:
                        report_file.write("Change Detected :" + file_path + " has different message digest\n Old Message Digest : " + old_message_digest+"\n New Digest Message : "+ message_digest+"\n\n")
                        changes += 1

                else:
                    #If not then it is new file (also a change)
                    report_file.write("Change Detected : The New File " +file_path + " has been added.\n")
                    changes = changes+1
                #file count
                file_count += 1

            #Iteration for all directories
            for dir in dirs:
                #Iteration for all directories
                directory_path = subdir + os.sep + dir
                #getting current state and info of the directory
                dirsize,dirowner,dirgroup,dirpermission,dir_last_modified = get_information(directory_path)

                #Checking the directory exists in verification 
                if directory_path in verification_json.keys():
                    # if yes then Storing the old values of the directories. 
                    olddirsize = verification_json[directory_path]["Directory Size"]
                    olddirowner = verification_json[directory_path]["Directory Owner"]
                    olddirgroup = verification_json[directory_path]["Directory Group"]
                    olddirpermissions = verification_json[directory_path]["Directory Permissions"]
                    olddirlastmodified = verification_json[directory_path]["Directory Last Modification Date"]

                    #If the current info is not same as old info then the following will execute and made detailed info in report file
                    if dirsize != olddirsize:
                        report_file.write("Change Detected : The directory " + directory_path + " has different size\n Old Size : " +str(olddirsize)+"\n New Size : "+str(dirsize)+"\n\n")
                        changes += 1
                    if dirowner != olddirowner:
                        report_file.write("Change Detected : The owner of directory " + directory_path + " has been changed\n Old Owner : " + olddirowner+"\n New Owner : "+ dirowner+"\n\n")
                        changes += 1
                    if dirgroup != olddirgroup:
                        report_file.write("Change Detected : The group of file " + directory_path + " has been changed\n Old Group : " + olddirgroup+"\n New Group : "+ dirgroup+"\n\n")
                        changes += 1
                    if dirpermission != olddirpermissions:
                        report_file.write("Change Detected :" +directory_path + " has different permissions\n Old Permissions : " + olddirpermissions +"\n New Permissions : "+ dirpermission+"\n\n")
                        changes += 1
                    if dir_last_modified != olddirlastmodified:
                        report_file.write("Change Detected :" +directory_path + " has different last modified date\n Old Last Modified : " + olddirlastmodified +"\n New Last Modified : "+ dir_last_modified+"\n\n")
                        changes += 1
                else:
                    #If not then it is new directory (also a change)
                    report_file.write("Change Detected :The New Directory " + directory_path + " has been added.\n")
                    changes += 1
                #directory count
                directory_counter += 1
        #Checking the file/directory is not exist now but in verfication file then file / directory is deleted
        for pat in verification_json.keys():
            if os.path.exists(pat) == 0:
                report_file.write("Change Detected :The File/Directory " + pat + " has been deleted\n")
                changes += 1
    #End Time
    end = time.time()  

    #Storing the report values to json file
    json_report = json.dumps({"Directory Path": arguments.Directory,"Verification File Path": os.path.abspath(arguments.Verification_file),"Number of Directories": directory_counter,"Number of Files": file_count,"Time to finish the verification mode": (end-start)*1000,"Number of changes detected": changes}, indent=4)

    #Appending json file to Report file
    with open(arguments.Report_file, "a") as final_report:
        final_report.write(json_report)
        print("Report file Generated")
