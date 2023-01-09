import numpy as np
from class_def.SED_Model import SED_Model

class SED_Fixed_Model( SED_Model, object ):
    def __init__(self, m, fix):
        super(SED_Fixed_Model,self).__init__(m)
        self.fix = fix
    def _getBaseModel(self, param):
        if not self.fix: # if fix is an empty dict
            super(SED_Fixed_Model, self)._getBaseModel(param)
        else:
            age_idx = int(param[2])
            metallicity_idx = int(param[3])
            covering_idx = int(param[4])  #covering factor
            if 'age' in self.fix:
                age_idx = self.fix['age']
            if 'metal' in self.fix:
                metallicity_idx = self.fix['metal']
            if 'covering' in self.fix:
                covering_idx = self.fix['covering']
        return self.model[covering_idx, metallicity_idx, age_idx, :]
    def evaluate(self, param):
        if 'extinction' in self.fix:
            extinction_av = self.fix['extinction']
        else:
            extinction_av = param[1]
        try:
            self.checkParamRange(param)
            # hostExt = np.power(10, (extinction_av * mySED.blambda/-2.5))
            hostExt = 1
            base_sed = self._getBaseModel(param)
            if self.isLogNorm:
                return np.exp(param[0]) * 1e-3 * base_sed * hostExt
            else:
                return param[0] * base_sed * hostExt
        except IndexError:
            print("[WARNING]: Parameters out of range. Automatically assigned an unrealistically large value")
            VERY_SMALL_NUMBER = -1e9
            return np.ones(self.model.shape[-1]) * VERY_SMALL_NUMBER

    def determine_mass(self, param):
        if self.isLogNorm:
            return np.exp(param[0]) * 1e-3 * 1e6 * mySED.age_mass_scaling[param[3].astype(np.int),param[2].astype(np.int)]
        else:
            return param[0] * 1e6 # in unit of solar mass

    def transform_to_physical_param(self, param):
        # the mass and age stored in param is not in physical units,
        # Use this function to transform to physical units
        # age/mass in log scale
        param = self.transform_fixed_param(param)
        mass = self.determine_mass(param.T)
        age = mySED.modelNumAgeMap[ param[:,2].astype(np.int) ]
        param_phys = np.copy(param)
        param_phys[:,0] = mass
        param_phys[:,2] = age
        return param_phys

    def transform_fixed_param(self, param):
        param = param.T
        if 'age' in self.fix:
            param[2] = self.fix['age']
        if 'metal' in self.fix:
            param[3] = self.fix['metal']
        if 'covering' in self.fix:
            param[4] = self.fix['covering']
        if 'extinction' in self.fix:
            param[1] = self.fix['extinction']
        return param.T
    def get_axis_labels(self):
        # go through the fix_dict to determine the axis labels
        labels = { 0: '$\log$ Mass [$M_\odot$]' }
        if not( 'extinction' in self.fix ):
            labels[1] = '$A_v$'
        if not( 'age' in self.fix ):
            labels[2] = '$\log$ Age [Myr]'
        if not( 'metal' in self.fix ):
            labels[3] = 'Metallicity [$Z_\odot$]'
        if not( 'covering' in self.fix ):
            labels[4] = '$f_{cov}$'
        return labels
