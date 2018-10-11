#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 11:08:24 2018

Usage:
    

python create_logsheet.py \
-i /data-dcm-srv/dicom/warehouse/RESEARCH^colcombe/A132_20160808_2016-08-08_135921 \
-o /output_folder/name_output.csv

Note: only works for dicoms that are organized in the wkarehouse

@author: afranco
alexandre.franco@nki.rfmh.org
"""

# importing packages
import pydicom as dicom
import os
import csv
import argparse

# object to get dicom info
class dicom_info:
    def __init__(self, num, name):
        self.num = num
        self.name = name


# Main routine
def main(in_prefix, csv_prefix):
    
    #in_dir = '/projects/afranco/ScanSheetMonkey/A132_20151116_2015-11-16_134940'
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
        #print(dcm_files)
     
        # Get the name of the first dicom on the list. Doesn't matter which one you get
        dcm_file_path = (folder_path + "/" + dcm_files[0])
        #print(dcm_file_path)
        
        # now read header info 
        dcm_in = dicom.read_file(dcm_file_path)
        #print(dcm_in.SeriesNumber)
        #print(dcm_in.SeriesDescription)
        #print(type(dcm_in.SeriesNumber))
        #print(type(dcm_in.SeriesDescription))
        
        #num = dcm_in.SeriesNumber
        #print(num )
        
        pointer.append(dcm_in.SeriesNumber)
        names.append(dcm_in.SeriesDescription)
        times.append(dcm_in.SeriesTime)
        ii = ii+1
    
    
    #print(pointer[0])
    #print(names)
    
    
    #loc = pointer[0]-1
    #print(loc)
    #print(type(loc))
    #print(names[pointer[pointer[0]-1]])

    # create a new list with the size of the number of folders
    n = len(folders)
    ordered_Description = [None]*n
    ordered_time = [None]*n
    
    ii = 0 
    for p in pointer:
        ordered_Description[p-1] = names[ii]
        ordered_time[p-1] = times[ii]
        ii = ii+1
    
    
    #print(names)
    print("series ordered: ")
    print(ordered_Description)
    
    # get numbers ordered to put on table
    order = list(range(1,n+1,1))
    print(order)

    # writing csv file
    # with open('output.csv', mode='w') as output_file:
    
    with open(csv_prefix, mode='w') as output_file:
        output_file = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # write the header
        output_file.writerow(['Number', 'Name', 'Time'])
        for ii in range(n):
            output_file.writerow([order[ii],ordered_Description[ii],ordered_time[ii]])
        


# Run main by default
if __name__ == '__main__':

    # Init argparser
    parser = argparse.ArgumentParser(description=__doc__)
    # Required arguments
    parser.add_argument('-i', '--input', nargs=1, required=True,
                        help='Input file directory where DICOMs are read in. Note: Folders must be organized in warehouse')
    parser.add_argument('-o', '--output', nargs=1, required=True,
                        help='name of csv file')
    args = parser.parse_args()
    '''
    # Will keep this for now to set input parameters
    class Namespace: 
        def __init__(self, **kwargs): 
            self.__dict__.update(kwargs) 
    args=Namespace(input='/projects/afranco/ScanSheetMonkey/A132_20151116_2015-11-16_134940', output='csv_output.csv')     
    in_prefix=args.input
    out_prefix=args.warehouse
    '''
    # Init argument variables
   # in_prefix = os.path.abspath(args.input[0])
    in_dir = args.input[0]
    #war_prefix = os.path.abspath(args.output[0])
    csv_prefix = args.output[0]
    
    print("will read folders that are located here:")
    print(in_dir)
    print("output file will be located here:")
    print(csv_prefix)
  
    # Call main function
    main(in_dir, csv_prefix)



