class Naive_Spectra:
    def __init__(self, metal,fcov,age,spectra):
        self.__spectra = dict()
        self.__spectra['metal'] = metal
        self.__spectra['fcov'] = fcov
        self.__spectra['age'] = age
        self.__spectra['spectra'] = spectra

    def get_spectra(self):
        return self.__spectra['spectra']

    def get_param(self):
        return (self.__spectra['metal'], self.__spectra['fcov'], self.__spectra['age'])

    def redshift_correction(self,redshift):
        spectra = self.__spectra['spectra'].copy()
        spectra[:,0] *= (1+redshift)
        return spectra

    def convolve_with_filters(self, filter):
        pass