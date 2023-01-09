import re
import numpy as np
from class_def.Naive_Spectra import Naive_Spectra

class Naive_Spectrum_List:
    def __init__(self):
        self.__sorted = False
        self.spectrum_list = []
        self.metal_options = set()
        self.fcov_options = set()
        self.age_options = set()
        self.__metal_matcher = re.compile('Z=(\d+\.?\d*)')
        self.__fcov_matcher = re.compile('fcov_(\d+\.?\d*)')
        self.__age_matcher = re.compile('Age(\d+e\d)')

    def add_spectra(self, fname, spectrum_info):
        try:
            metal_param = self.__metal_matcher.search(fname).group(1)
            fcov_param = self.__fcov_matcher.search(fname).group(1)
            age_param = self.__age_matcher.search(fname).group(1)
            self.metal_options.add( metal_param )
            self.fcov_options.add( fcov_param )
            self.age_options.add( age_param )
            self.spectrum_lst.append(
                Naive_Spectra( metal_param, fcov_param, age_param, spectrum_info )
            )
        except:
            errmsg = "Error: Cannot parse the metallicity, covering factor and age information from the file name: "
            #correct_format = " Correct format of file name should include Z=<metallicity>_ , fcov_<covering_factor>, > for "
            print(errmsg , fname)

    def get_spectrum(self, param_tuple):
        '''
        The function takes a tuple of parameters, in the form of (metal, fcov, age) (in string),
        and return the required spectrum
        '''
        return filter(
            lambda entry:
                entry.get_param() == param_tuple
            , self.spectrum_list
        )[0]


    def sort_spectrum(self):
        # self.spectrum_arr = np.ones(len(self.fcov_options), len(self.metal_options), len(self.age_options), )

        self.__sorted = True
