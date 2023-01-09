import numpy as np
from class_def.Abstract_Model import Abstract_Model

class SED_Model(Abstract_Model):
    def __init__(self, spectra, interpolation=True):
        self.model = spectra
        self.isLogNorm = False
        if interpolation:
            self._init_sed_interpolator()
    def _init_sed_interpolator():
        pass    
    def set_logNorm(self, isLogNorm):
        self.isLogNorm = isLogNorm
    def evaluate(self, param):
        '''
        input: list of param in format of [normalization, extinction, age_idx, metallicity_idx, covering_idx]
        '''
        normalization = param[0]
        extinction_strength = param[1]
        if self.checkParamRange(param):
            # hostExt = np.power(10, (extinction_strength * mySED.blambda/-2.5))
            hostExt = 1
            base_sed = self._getBaseModel(param)
            if self.isLogNorm:
                return np.exp(normalization) * base_sed * hostExt
            else:
                return normalization * base_sed * hostExt

    def checkParamRange(self,param):
        ageIdxLow = 0
        ageIdxHigh = self.get_num_of_age()
        extIdxHigh = 1.2
        metalIdxLow = 0
        metalIdxHigh = self.get_num_of_metal()
        covering_idx_low = 0
        covering_idx_high = self.get_num_of_covering()
        outRange = (
            ( not (ageIdxLow <= param[2] <= ageIdxHigh) )
            or (param[0]<= 0)
            or (not (0 <= param[1] <= extIdxHigh) )
            or (not( metalIdxLow <= param[3]<= metalIdxHigh))
            or (not( covering_idx_low <= param[4]<= covering_idx_high ))
        )
        if outRange:
            raise IndexError("Parameters out of range")
        else:
            return True

    def _getBaseModel(self,param):
        age_idx = int(param[2])
        metallicity_idx = int(param[3])
        covering_idx = int(param[4])  #covering factor

        return self.model[covering_idx, metallicity_idx, age_idx, :]

    def get_color_overview(self):
        colors = np.zeros((self.get_num_of_covering(), self.get_num_of_metal(), self.get_num_of_age() , self.get_num_of_filters()))
        for i in range(colors.shape[0]):
            for j in range(colors.shape[1]):
                for k in range(colors.shape[2]):
                    colors[i,j,k,:] = self.model[i,j,k,:]
        return colors

    def save_color_overview(self, fname , metal_list, covering_list):
        ages = np.array([ [modelNumAgeMap[i]*1e6] for i in range(1,len(modelNumAgeMap)) ])
        color_arr = self.get_color_overview()
        for i in range(self.get_num_of_metal()):
            for j in range(self.get_num_of_covering()):
                color_stack_age = np.hstack( (ages, color_arr[j,i,:,:]) )
                file_full_name = metal_list[i] + "_" + fname + "_" + covering_list[j] + ".tab"
                np.savetxt( file_full_name, color_stack_age, delimiter='\t')
        print("Color array saved as file, with name: metal_" , fname , "_fcov.tab")

    def get_num_of_filters(self):
        return self.model.shape[3]

    # implements the MCMC_Sampler_Interface

    def get_num_of_parameters(self):
        return 5

    def get_num_of_age(self):
        return self.model.shape[2]

    def get_num_of_metal(self):
        return self.model.shape[1]

    def get_num_of_covering(self):
        return self.model.shape[0]
