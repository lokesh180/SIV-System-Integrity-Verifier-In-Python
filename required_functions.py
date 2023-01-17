"""
In this Module the required functions were defined, those functions were isdirexists(checking if directory exists or not), Creating Files(creates verification 
and report files if not exists),hash_message(getting hexdigest of given file and only md5 or sha1) and getinformantion(gives the information about the given file) 
"""
#importing Required Modules
import os
import sys
import stat
import time
from pwd import getpwuid
from grp import getgrgid
from hashlib import sha1, md5

#This function will check if directory exists or not.
def isdirexist(Directory):
    if os.path.exists(Directory):
        print("Given Directory Exists-->",end='')
        return True
    else:
        print("Directory does not exist. Give an existing directory or create new one.")
    return False

# This function will create verification and report files if not exists
def creating_files(Directory,Verification_file,Report_file,Mode):
    # Checking the current working directory with given directory path
    if os.getcwd() == Directory:
        print('The path should be out of the directory')
        sys.exit()
    # Checking the verification file path with given directory path
    elif Directory == Verification_file.split('/')[0]:
        print('The path of the Verification File should be out of given directory')
        sys.exit()
    # Checking the report file path with given directory path
    elif Directory == Report_file.split('/')[0]:
        print('The path of the Report File should be out of given directory')
        sys.exit()
    
    else:

        if Mode == "init":
            #Checking the verification file and creating if not exist
            if os.path.exists(Verification_file):
                print("Verification File Exists-->",end='')
                #os.open(Verification_file, os.O_CREAT, mode=0o0777)
            else:
                os.open(Verification_file, os.O_CREAT, mode=0o0777)
                print("New Verification File Created-->",end='')

            #Checking the report file and creating if not exist
            if os.path.exists(Report_file):
                print("Report File exist-->",end='')
            else:
                os.open(Report_file, os.O_CREAT, mode=0o0777)
                print("New Report File Created-->",end='')
            
        if Mode == "verify":
            if os.path.exists(Verification_file):
                print("Verification File Exists-->",end='')
            else:
                
                print("The Verification File doesn't exists! \n Try Initialization first")
                sys.exit()

            if os.path.exists(Report_file):
                print("Report File Exists-->",end='')
                #os.open(Report_file, os.O_CREAT, mode=0o0777)
            else:
                print("New Report File Created-->",end='')
                os.open(Report_file, os.O_CREAT, mode=0o0777)

def get_information(path):
    # return the required details of files
    st = os.stat(path) 
    sizeofpath = os.path.getsize(path) #getting size of file
    ownerofpath = getpwuid(os.stat(path).st_uid).pw_name #getting owner of file
    groupofpath = getgrgid(os.stat(path).st_gid).gr_name #getting group of file
    permissionsofpath = stat.filemode(st.st_mode) #getting permissions of file
    last_modifiedofpath = time.ctime(os.path.getmtime(path)) #getting last modified of file
    return (sizeofpath,ownerofpath,groupofpath,permissionsofpath,last_modifiedofpath)

#This function will return hexdigest msg to verification module and Initialization module.
def hash_message(arguments,file_path):
    #Checking the given hash function
    if arguments in ["sha1"]:
        #creating object for sha1
        sha1_function = sha1()
        #reading the file bytes
        with open(file_path, 'rb') as filee:
            data = filee.read()
            #updating the file bytes to sha1
            sha1_function.update(data)
            #storing the hexdigest to a variable and added to verification file
            msg = sha1_function.hexdigest()

    if arguments in ["md5"]:
        #creating object for md5
        md5_function = md5()
        #reading the file bytes
        with open(file_path, 'rb') as filee:
            data = filee.read()
            #updating the file bytes to sha1
            md5_function.update(data)
            #storing the hexdigest to a variable and added to verification file
            msg = md5_function.hexdigest()
    return msg