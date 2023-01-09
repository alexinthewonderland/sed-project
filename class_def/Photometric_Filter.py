import numpy as np
class Photometric_Filter:
    def __init__(self, filter_info, filter_peak_wavelength, redshift):
        self.filter_info = filter_info
        self.num_of_filter = len( self.filter_info )
        filter_peak_wavelength /= redshift
        filter_peak_wavelength = np.flip(filter_peak_wavelength, axis=0)
        self.filter_peak_wavelength = filter_peak_wavelength

    def get_filter_passband(self, filter_idx):
        return self.filter_info[filter_idx][:,0]
    def get_filter_transmission(self, filter_idx, observed_wavelength):
        return np.interp( observed_wavelength, self.get_filter_passband(filter_idx), self.filter_info[filter_idx][:,1] )
    def get_filter_peak_wavelength(self):
        return self.filter_peak_wavelength
