#!/usr/bin/env python3
"""
This is the main module with main function and need to execute with this module..
"""
#importing the required modules
from argparse import ArgumentParser #Using Argument Parser to get command line arguments and do computations.
from Initialization import initialization # importing the modules Initaliation and 
from Verification import verification    # Verification (both are defined modules)
import sys

def main():
    #Storing the command line arguments
    argument_parser = ArgumentParser()
    groupofargs = argument_parser.add_mutually_exclusive_group()
    groupofargs.add_argument("-i", "--initmode", action="store_true",help="Initialization Mode.")
    groupofargs.add_argument("-v", "--verifymode", action="store_true",help="Verification Mode.")
    argument_parser.add_argument("-D", "--Directory",type=str, help="Given directory is monitored.")
    argument_parser.add_argument("-V", "--Verification_file", type=str,help="The verification data will be stored in this file but should be out of monitered directory.")
    argument_parser.add_argument("-R", "--Report_file", type=str,help="The report will be stored in this file and should be out of monitered directory as well.")
    argument_parser.add_argument("-H", "--Hash_function", type=str,help="Use the Hash function as md5 or sha1.")
    arguments = argument_parser.parse_args()

    """
    The below lines makes the user provide correct input while Intialization and Verification
    For Intialization All input flags are expected but for 
    Verfication All input flags except hash function are expected by the program.
    """
    if arguments.initmode and arguments.Directory and arguments.Verification_file and arguments.Report_file and arguments.Hash_function:
        print("---Initialization Started---")
        #Checking the provided hash function is sha1 or md5.
        if arguments.Hash_function not in ["sha1", "md5"]:
            print("The Hash Function should be sha1 or md5")
            sys.exit()
        #Control over to  Intialization Module-->
        initialization(arguments)
        print("---Initialization Completed---")

    elif arguments.verifymode and arguments.Directory and arguments.Verification_file and arguments.Report_file and not arguments.Hash_function:
        print("---Verification Started---")
        #Control over to  Verification Module-->
        verification(arguments)
        print("---Verification Completed---")
    else:
        #If the user provide the input flags, which other than expected then the below print statements will be shown.. 
        print("---The Given Format is Wrong---")
        #print("-h,     ->       Help Message Displayed.\n")
        print(" For Initalization mode:\nusage: ./siv -i [-D Monitered_Directory] [-V Verification_file] [-R Report_file] [-H Hash_function]")
        print(" For Verification mode:\nusage: ./siv -i [-D Monitered_Directory] [-V Verification_file] [-R Report_file]")
        print("Try using python3 siv.py -h / ./siv.py -h for all options")


if __name__ == "__main__":
    main()