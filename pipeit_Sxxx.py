import os
import unittest
from math import pi
import math

import matplotlib.pyplot as plt
import numpy as np

from wisdem.ccblade import CCAirfoil, CCBlade
from blade_geometry import blade_geometry

class Performance_coef(unittest.TestCase):
    def setup(self):
        """
        Parameters
        ----------
        r : array_like (m)
            locations defining the blade along z-axis of :ref:`blade coordinate system <azimuth_blade_coord>`
            (values should be increasing).
        chord : array_like (m)
            corresponding chord length at each section
        theta : array_like (deg)
            corresponding :ref:`twist angle <blade_airfoil_coord>` at each section---
            positive twist decreases angle of attack.
        Rhub : float (m)
            location of hub
        Rtip : float (m)
            location of tip
        B : int, optional
            number of blades
        rho : float, optional (kg/m^3)
            freestream fluid density
        mu : float, optional (kg/m/s)
            dynamic viscosity of fluid
        precone : float, optional (deg)
            :ref:`hub precone angle <azimuth_blade_coord>`
        tilt : float, optional (deg)
            nacelle :ref:`tilt angle <yaw_hub_coord>`
        yaw : float, optional (deg)
            nacelle :ref:`yaw angle<wind_yaw_coord>`
        shearExp : float, optional
            shear exponent for a power-law wind profile across hub
        hubHt : float, optional
            hub height used for power-law wind profile.
            U = Uref*(z/hubHt)**shearExp
        nSector : int, optional
            number of azimuthal sectors to descretize aerodynamic calculation.  automatically set to
            ``1`` if tilt, yaw, and shearExp are all 0.0.  Otherwise set to a minimum of 4.
        """
        self.Rhub = 1.5
        self.Rtip = 55.60721094924956
        B = 3  # number of blades
        # atmosphere
        rho = 1.225
        mu = 1.81206e-5
        
        tilt = 5.0
        precone = 2.5
        yaw = 0.0
        shearExp = 0.2
        hubHt = (self.Rtip*2)*0.92
        nSector = 8

        tsr = 7.55
        # max chord length
        c_max = 5
        # lift coefficients for the given airfoils
        Cl = [1.3871, 1.3871, 1.3871, 1.3871, 1.464, 1.464, 1.464, 1.464, 1.4509, 1.4509, 1.4509, 1.4509, 1.4509, 1.4509]

        self.r = np.array([self.Rtip*0.045503175, self.Rtip*0.088888889, self.Rtip*0.132274603, self.Rtip*0.186507937, self.Rtip*0.251587302,       self.Rtip*0.316666667, self.Rtip*0.381746032, self.Rtip*0.446825397, self.Rtip*0.511904762, self.Rtip*0.576984127, self.Rtip*0.642063492, self.Rtip*0.707142857, self.Rtip*0.772222222, self.Rtip*0.837301587, self.Rtip*0.891534921, self.Rtip*0.934920635, self.Rtip*0.978306349])

        afinit = CCAirfoil.initFromAerodynFile  # just for shorthand
        basepath = 'C:/Users/Thomas/OneDrive/Tieto/Airfoils/'

        # load all airfoils
        airfoil_types = [0]*5
        airfoil_types[0] = afinit(basepath + 'Cylinder1.dat')
        airfoil_types[1] = afinit(basepath + 'Cylinder2.dat')
        airfoil_types[2] = afinit(basepath + 'S818_output3_extrap.txt')
        airfoil_types[3] = afinit(basepath + 'S830_output_extrap.txt')
        airfoil_types[4] = afinit(basepath + 'S831_output_extrap.txt')

        # place at appropriate radial sections
        af_idx = [0, 0, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4]

        af = [0]*len(self.r)
        for i in range(len(self.r)):
            af[i] = airfoil_types[af_idx[i]]

        # chord = np.array([3.542, 3.854, 4.167, 4.557, 4.652, 4.458, 4.249, 4.007, 3.748,
        #                 3.502, 3.256, 3.010, 2.764, 2.518, 2.313, 2.086, 1.419])

        chord = np.array(blade_geometry(self.Rtip, self.r, B, Cl, tsr, c_max, plot=False))

        theta = np.array([13.308, 13.308, 13.308, 13.308, 11.480, 10.162, 9.011, 7.795,
                        6.544, 5.361, 4.188, 3.125, 2.319, 1.526, 0.863, 0.370, 0.106])

        # create CCBlade object
        self.aeroanalysis = CCBlade(self.r, chord, theta, af, self.Rhub, self.Rtip, B, rho, mu,
                            precone, tilt, yaw, shearExp, hubHt, nSector)

    def compute(self):
        ''' 
        Uinf : array_like (m/s)
            hub height wind speed
        Omega : array_like (RPM)
            rotor rotation speed
        pitch : array_like (deg)
            blade pitch setting
        '''
        # set conditions
        Uinf = np.array([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                         20, 21, 22, 23, 24, 25])
        Omega = np.array([6.972, 7.183, 7.506, 7.942, 8.469, 9.156, 10.296, 11.431,
                          11.890, 12.100, 12.100, 12.100, 12.100, 12.100, 12.100,
                          12.100, 12.100, 12.100, 12.100, 12.100, 12.100, 12.100, 12.100])
        pitch = np.array([0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000,
                          3.823, 6.602, 8.668, 10.450, 12.055, 13.536, 14.920, 16.226,
                          17.473, 18.699, 19.941, 21.177, 22.347, 23.469])

        P, T, Q, M, CP, CT, CQ, CM = self.aeroanalysis.evaluate(Uinf, Omega, pitch, coefficients=True)

        print('CP:' + str(CP))

        path = "C:/Users/Thomas/OneDrive/Tieto/Scripts/Output/Cp_res.txt"

        with open(path, 'w') as f:
            f.write('Cp:\n')
            for i in CP:
                f.write("%s\n" % str(i))
            f.write('\n')
            f.write('Radius: \n')
            f.write(str(self.Rtip))
            f.close()

        
        # fig, ax1 = plt.subplots()
        # ax1.plot(Uinf, CP, 'k')
        # ax1.set_xlabel('$\lambda$')
        # ax1.set_ylabel('$c_p$')

        # ax2 = ax1.twinx()

        # ax2.plot(Uinf, P/1000, 'r')
        # ax2.set_ylabel('$Power$')
        # fig.tight_layout()
        # plt.show()

        # idx = (Uinf < 15)
        # np.testing.assert_allclose(Q[idx]/1e6, Qref[idx]/1e3, atol=0.15)
        # np.testing.assert_allclose(P[idx]/1e6, Pref[idx]/1e3, atol=0.2)  # within 0.2 of 1MW
        # np.testing.assert_allclose(T[idx]/1e6, Tref[idx]/1e3, atol=0.15)
        


if __name__ == '__main__':
    Cp = Performance_coef()
    Cp.setup()
    Cp.compute()
