# sed-project

In this project, our goal is to interpolate the SED plot of a galaxy using the appropriate methods to find the Star Formation Rate (SFR) of he galaxy in study. My supervisor on this, which is Mr. Leo W.H. Fung, has a plan to use this project to be used when JWST has finally launched and obtain crucial observations! 

* [class_def](https://github.com/alexinthewonderland/sed-project/tree/main/class_def) folder is a folder that contains all the class and function definitions that would be used in the [sed_evaluation.py](https://github.com/alexinthewonderland/sed-project/blob/main/sed_evaluation.ipynb) file 
* [throughput-file](https://github.com/alexinthewonderland/sed-project/tree/main/throughput-file) folder contains a few ```.csv``` file data to test out the SED fitting interpolation.
* [sed_evaluation.py](https://github.com/alexinthewonderland/sed-project/blob/main/sed_evaluation.ipynb) file is made by Mr. Leo W.H. Fung that consists of some functions relating to obtaining the wavefunction and generating the SED of a galaxy depending on how fast the Star Formation Rate (SFR) is.
* [sersic-profile.ipynb](https://github.com/alexinthewonderland/sed-project/blob/main/sersic-profile.ipynb) contains thhttps://github.com/alexinthewonderland/sed-project/blob/main/sersic-profile.ipynbe code to generate a simulation of a galaxy light distribution based on its Sersic profile.
* [redshifted-sed](https://github.com/alexinthewonderland/sed-project/blob/main/redshifted-sed.ipynb) adds a redshift effect to the observed galaxy SED and various types of noises to resemble more of a real a galaxy's SED observation.
* [emcee-attempt.ipynb](https://github.com/alexinthewonderland/sed-project/blob/main/emcee-attempt.ipynb) contains my attempt to learn and implement the [emcee](https://emcee.readthedocs.io/en/stable/) library in Python.
* [gradient-descent.ipynb](https://github.com/alexinthewonderland/sed-project/blob/main/gradient-descent.ipynb) file is a code about my first try ever trying to use gradient descent to predict the slope value of a line! This method would be used to try to find the SFR for future implementations.


This project is not fully finished and remains ongoing although I have stopped working on it due to moving to another research group to explore and try out new physics fields! But what I have learned here remains unforgettable and crucial to my preparations for other future projects. My biggest thanks go to Mr Leo W.H. Fung for supervising me on thsi project! For more detail regarding SED Fitting, one could check the following paper titled ["Fitting the integrated Spectral Energy Distributions of Galaxies"](http://www.sedfitting.org/Paper_vs1.0_online/walcher_ms.html) by Jakob Walcher, Brent Groves, Tamás Budavári, and Daniel Dale.

\*Note: when importing the library, make sure to run it twice to get rid of the weird graph that pops up when you run it the first time.
