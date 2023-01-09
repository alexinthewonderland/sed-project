from astropy.cosmology import FlatLambdaCDM
import astropy.units as u

class Observation_Specification:
    def __init__(self, z,radec,arcsec_per_pixel,cosmology = None):
        if cosmology is None :
            print("No cosmology model input. Assumes Lambda-CDM cosmology.")
            self.cosmology = FlatLambdaCDM(H0=70 * u.km / u.s / u.Mpc, Tcmb0=2.725 * u.K, Om0=0.3)
        else:
            self.cosmology = cosmology
        self.redshift = z
        self.pxiel2arcsec = arcsec_per_pixel
        # rms_err = np.flip(err,0)
        # blambda = ext_ccm(wave)
        self.raDec_extinction = radec

    def get_luminosity_distance(self):
        return (self.cosmology.luminosity_distance(z).to(u.cm)).value

    def get_angular_diameter_distance(self):
        return (cosmo.angular_diameter_distance(z).to(u.Mpc)).value

    def get_length_per_pixel(self):
        return self.get_angular_diameter_distance() * self.pixel2arcsec
