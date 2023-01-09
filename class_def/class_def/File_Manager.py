import numpy as np
import csv
import os
from class_def.Naive_Spectrum_List import Naive_Spectrum_List

class File_Manager:
    def __init__(self, homePath):
        self.homePath = homePath

    def __import_file(self, fname):
        ifile = open(fname,'rt')
        reader = csv.reader(ifile)
        # to detect how many columns are there
        firstLine = next(reader)[0].split()
        container = np.array([]).reshape(0,np.shape(firstLine)[0])
        firstLine = np.array([firstLine]).astype(np.float) #cast string type to float
        container = np.append(container,firstLine,axis=0)
        rowNum = 1
        for row in reader: #noted that this start from the second line, the first line is used to determine num of columns
            rowNum += 1
            if row:
                row = np.array([row[0].split()]).astype(np.float)
                container = np.append(container,row,axis=0)
        return container

    def read_model(self):
        sub_directory = self.homePath + 'model/'
        fpath = [ os.path.join(r,file) for r,d,f in os.walk(sub_directory) for file in f]
        spectrum_templates = Naive_Spectrum_List()
        for f in fpath:
            spectrum_templates.add_spectra(f, self.__import_file(f))
        # spectrum_templates.sort_spectrum()
        return spectrum_templates
        # return spectrum


    def read_filter_passband(self, fname_list):
        filter_info = []
        sub_directory = self.homePath + 'filter/'
        for i in fname_list[0:4]:
            fileFullName = str(sub_directory + i + '.UVIS1_plain.tab')
            data = self.__import_file(fileFullName)
            filter_info.append( data[:,1:3] )
        for i in fname_list[4:11]:
            fileFullName = str(sub_directory + 'wfc_' + i + '.dat')
            data = self.__import_file(fileFullName)
            filter_info.append( data[:,0:2] )
        for i in fname_list[11:16]:
            fileFullName = str(sub_directory + i + '.IR_plain.tab')
            data = self.__import_file(fileFullName)
            filter_info.append( data[:,1:3] )
        return filter_info
