#!/usr/bin/python2.7
# sort_dicom.py
#
# Author: Daniel Clark, 2014
# Adapted by Carlos G.Candano

'''
This module reads in DICOM files, sorts and archives their raw content,
then modifies their headers, and stores those in a temp directory.

Usage: python sort_dicom.py -i <input_directory> -w <warehouse_directory>
       -e <error_directory> -l <log_directory>
'''

import dicom
import argparse
import os

# Main routine
def main(in_prefix, war_prefix):
    '''
    Function to perform the main dicom receive, copy, archive and
    send process.

    Parameters
    ----------
    in_prefix : string
        the base input directory prefix for all of the input files to 
        process
    war_prefix : string
        the base directory where all of the non-modified input files
        get renamed, restructured, and saved to

    '''
        
    file_paths = []
    #in_prefix="/data/dicom/warehouse/" -->root --> All folders and subFolders FULL Paths.
    for root, dirs, files in os.walk(in_prefix):
        if files:
            file_list = ["%s/%s"%(root,f) for f in files]
            file_paths.extend(file_list)
    file_paths.sort()
    i = 0
    war_paths = []
    # Now read each dcm in from file list, modify header, create filepath
    for fp in file_paths:
        print(fp)
        i += 1
        # Try and read in the DICOM file
        try: dcm_in = dicom.read_file(fp)
        except: pass
        # Get header information
        patient_id = dcm_in.PatientID
        try: study_desc = dcm_in.StudyDescription
        except: study_desc = dcm_in.ReferringPhysicianName
        series_no = dcm_in.SeriesNumber
        instance_no = dcm_in.InstanceNumber
        study_date = dcm_in.StudyDate
        study_time = dcm_in.StudyTime
        # Insert null for echo_nums if not there
        echo_nums = str(dcm_in.EchoNumbers) \
            if 'EchoNumbers' in dcm_in else "null" 
        # Strip < > from series description
        series_desc = dcm_in.SeriesDescription
        series_desc = series_desc.strip('<').strip('>')

        # --- Format and create output paths ---
        # Reorganize file and set up archived filepath
        formatted_date = '-'.join([study_date[0:4], study_date[4:6], study_date[6:]])
        formatted_time = study_time.split('.')[0]
        top_dir = study_desc
        sub_dir = '_'.join([patient_id, formatted_date, formatted_time])
        sub_sub_dir = series_desc + '_' + str(series_no).zfill(3)
        dcm_no = str(instance_no).zfill(6)
        # Remove unwanted characters from directory names
        top_dir = top_dir.translate(None, '`"~!#$%;&*/|\,(){}?<>')
        sub_dir = sub_dir.translate(None, '`"~!#$%;&*/|\,(){}?<>')
        sub_sub_dir = sub_sub_dir.translate(None, '`"~!#$%;&*/|\,(){}?<>')
        # Create filepath directories (for out and archive)
        war_fp = os.path.join(war_prefix, top_dir, sub_dir, sub_sub_dir)
        # Replace any spaces in the filename with '_'
        war_fp = war_fp.replace(' ', '_')
        if not os.path.exists(war_fp):
            os.makedirs(war_fp)
        war_file = war_fp + '/' + dcm_no + '-' + echo_nums + '.dcm'
        # Now save to the new dcm archived filepath
        try:
            dcm_in.save_as(war_file)
            war_paths.append(war_file)
            # Log successful archive
        except: pass


# Run main by default
if __name__ == '__main__':

    # Backup flag, if True, the archived file already exists, back up the existing one
    bak_flg = False
    # Init argparser
    parser = argparse.ArgumentParser(description=__doc__)
    # Required arguments
    parser.add_argument('-i', '--input', nargs=1, required=True,
                        help='Input file directory where DICOMs are read in')
    parser.add_argument('-w', '--warehouse', nargs=1, required=True,
                        help='Directory to warehouse the image files to before DCMRCV')
    args = parser.parse_args()
    '''
    class Namespace: 
        def __init__(self, **kwargs): 
            self.__dict__.update(kwargs) 
    args=Namespace(input='/home/cgutierrez/dicom_receive/archive', warehouse='/home/cgutierrez/dicom_receive/warehouse')     
    in_prefix=args.input
    war_prefix=args.warehouse
    '''
    # Init argument variables
    in_prefix = os.path.abspath(args.input[0])
    war_prefix = os.path.abspath(args.warehouse[0])
    # Call main function
    main(in_prefix, war_prefix)
