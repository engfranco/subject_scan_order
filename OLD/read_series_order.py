#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 11:08:24 2018

Usage:
    XXXXX

@author: afranco
"""

# importing packages
import pydicom as dicom
import os
import csv

# object to get dicom info
class dicom_info:
    def __init__(self, num, name):
        self.num = num
        self.name = name

in_dir = '/projects/afranco/ScanSheetMonkey/A132_20151116_2015-11-16_134940'
folders = os.listdir(in_dir)

print("Going to look at these folders:")

for folder in folders:
    print(folder)

names =[]
pointer = []
times = []
ii =0
# now we need to read the files within each folder
for folder in folders:
    # Get full path for each folder
    folder_path = os.path.abspath(in_dir +"/" + folder)
   # print(folder_path)
    
    # get files in folder 
    dcm_files = os.listdir(folder_path)
#   print(len(dcm_files))
    dcm_files.sort()
    print(dcm_files)
 
    # Get the name of the first dicom on the list. Doesn't matter which one you get
    dcm_file_path = (folder_path + "/" + dcm_files[0])
    print(dcm_file_path)
    
    # now read header info 
    dcm_in = dicom.read_file(dcm_file_path)
    print(dcm_in.SeriesNumber)
    print(dcm_in.SeriesDescription)
    print(type(dcm_in.SeriesNumber))
    print(type(dcm_in.SeriesDescription))
    
    num = dcm_in.SeriesNumber
    print(num +1 )
    
    pointer.append(dcm_in.SeriesNumber)
    names.append(dcm_in.SeriesDescription)
    times.append(dcm_in.SeriesTime)
    ii = ii+1


print(pointer[0])
print(names)

print(type(pointer[0]-1))
loc = pointer[0]-1
print(loc)
print(type(loc))
print(names[pointer[pointer[0]-1]])

# create a new list with the size of the number of folders
n = len(folders)
ordered_Description = [None]*n
ordered_time = [None]*n

ii = 0
for p in pointer:
    ordered_Description[p-1] = names[ii]
    ordered_time[p-1] = times[ii]
    ii = ii+1


print(names)
print(ordered_Description)

# get numbers ordered to put on table
order = list(range(1,n+1,1))
print(order)

# writing csv file
with open('output.csv', mode='w') as output_file:
    output_file = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # write the header
    output_file.writerow(['Number', 'Name', 'Time'])
    for ii in range(n):
        output_file.writerow([order[ii],ordered_Description[ii],ordered_time[ii]])
        



#with open('employee_file.csv', mode='w') as employee_file:
#    employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

#    employee_writer.writerow(['John Smith', 'Accounting', 'November'])
#    employee_writer.writerow(['Erica Meyers', 'IT', 'March'])
  