# SIV-System-Integrity-Verifier-In-Python

The System integrity verifier is a tool that monitor and analysis the network or system. 
Alerting when vulnerable activities performed. 
The SIV detects the automated scripts if exists in folder and files. 
It also detects all kind of activities like renaming, file adding, file deleting, file size increase or decrease, 
and so on activities in the file directories.

The goal of this project is to implement a simple system integrity verifier (SIV) for Linux systems. 
This SIV need to monitor given directory and detects the file system modifications like file size change, 
folder added or removed, permissions, last modified date, and some other things (will discuss in further sections). 
The SIV need to make a report of all the modifications with the old values and new values. 
The SIV should be executed in two modes. They are Initialization and Verification modes.

In this project the goal of SIV is to mainly focus on modifications of
1. New or Removed files/directories.
2. Files/Directories with different sizes than recorded.
3. Files with different digest message than computed before while initialization.
4. Files/Directories with different user/group.
5. Files/Directories with modified access rights (permissions).
6. Files/Directories with different last modification dates.
