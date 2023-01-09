from astropy.io import fits
import numpy as np

class Image_Fits(object):
    #an abstract class, observation_img and noise_img implements it
    def __init__(self, fits_path=None,img_data=None):
        #load the data in
        if fits_path is not None:
            self._data = self.read_fits(fits_path)
        elif img_data is not None:
            self._data = img_data
        else:
            print("You must either enter the path of the fits or the image array")
    def get_flux(self,location,size=[1,1]):
        return self._data[:,location[0]:location[0]+size[0], location[1]:location[1]+size[1] ]
    def bin(self):
        pass
    def get_size(self):
        #first dimension of the fit are filters wavelength
        return [ self._data.shape[1], self._data.shape[2] ]
    def get_num_of_filter(self):
        return self._data.shape[0]
    def read_fits(self,img_file):
        dataCube = fits.getdata(img_file)
        dataCube = np.flip(dataCube, axis=0)
        return dataCube
    def set_focus(self,xlow,xhigh,ylow,yhigh):
        self._data = self._data[:,ylow:yhigh,xlow:xhigh]

class Observation_Img(Image_Fits):
    def __init__(self,galactic_extinction_correction,fits_path=None,img_data=None):
        super(Observation_Img,self).__init__(fits_path, img_data)
        for i in range(self.get_size()[0]):
            for j in range(self.get_size()[1]):
                self._data[:,i,j] /= galactic_extinction_correction
    def bin(self,location,aperture_size):
        flux = self.get_flux(location, aperture_size)
        flux =  np.mean(flux, axis=(1,2))
        #flux /= (aperture_size[0] * aperture_size[1])
        return flux

class Noise_Img(Image_Fits):
    def __init__(self,error_bar, fits_path=None, img_data=None):
        super(Noise_Img,self).__init__(fits_path, img_data)
        self.error_bar = error_bar *4
    def bin(self, location, aperture):
        error = np.power( self.error_bar,2 )
        poisson = self.get_flux(location, aperture)
        poisson = np.mean(poisson, axis=(1,2))
        return np.sqrt( ( error+np.power(poisson,2) )/ aperture[0] / aperture[1] )
