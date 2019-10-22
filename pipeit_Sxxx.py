import os
import unittest
from math import pi
import math

import matplotlib.pyplot as plt
import numpy as np

from wisdem.ccblade import CCAirfoil, CCBlade


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
        self.Rtip = 63
        self.r = np.array([self.Rtip*0.045503175, self.Rtip*0.088888889, self.Rtip*0.132274603, self.Rtip*0.186507937, self.Rtip*0.251587302, self.Rtip*0.316666667,                         self.Rtip*0.381746032, self.Rtip*0.446825397, self.Rtip*0.511904762, self.Rtip*0.576984127, self.Rtip*0.642063492, self.Rtip*0.707142857,                         self.Rtip*0.772222222, self.Rtip*0.837301587, self.Rtip*0.891534921, self.Rtip*0.934920635, self.Rtip*0.978306349])

        afinit = CCAirfoil.initFromAerodynFile  # just for shorthand
        basepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "5MW_AFFiles/")

        # load all airfoils
        airfoil_types = [0]*8
        airfoil_types[0] = afinit(basepath + 'Cylinder1.dat')
        airfoil_types[1] = afinit(basepath + 'Cylinder2.dat')
        airfoil_types[2] = afinit(basepath + 'DU40_A17.dat')
        airfoil_types[3] = afinit(basepath + 'DU35_A17.dat')
        airfoil_types[4] = afinit(basepath + 'DU30_A17.dat')
        airfoil_types[5] = afinit(basepath + 'DU25_A17.dat')
        airfoil_types[6] = afinit(basepath + 'DU21_A17.dat')
        airfoil_types[7] = afinit(basepath + 'NACA64_A17.dat')

        # place at appropriate radial stations
        af_idx = [0, 0, 1, 2, 3, 3, 4, 5, 5, 6, 6, 7, 7, 7, 7, 7, 7]

        af = [0]*len(self.r)
        for i in range(len(self.r)):
            af[i] = airfoil_types[af_idx[i]]

        # chord = np.array([3.542, 3.854, 4.167, 4.557, 4.652, 4.458, 4.249, 4.007, 3.748,
        #                 3.502, 3.256, 3.010, 2.764, 2.518, 2.313, 2.086, 1.419])
        def chords(self, r, Cl):
            c = ((16*pi*self.Rtip)/(9*3*Cl))
        chord = np.array([self.Rtip*0.056222222, self.Rtip*0.061174603, self.Rtip*0.066142857])
        theta = np.array([13.308, 13.308, 13.308, 13.308, 11.480, 10.162, 9.011, 7.795,
                        6.544, 5.361, 4.188, 3.125, 2.319, 1.526, 0.863, 0.370, 0.106])

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


        Pref = np.array([42.9, 188.2, 427.9, 781.3, 1257.6, 1876.2, 2668.0, 3653.0,
                         4833.2, 5296.6, 5296.6, 5296.6, 5296.6, 5296.6, 5296.6,
                         5296.6, 5296.6, 5296.7, 5296.6, 5296.7, 5296.6, 5296.6, 5296.7])
        Tref = np.array([171.7, 215.9, 268.9, 330.3, 398.6, 478.0, 579.2, 691.5, 790.6,
                         690.0, 608.4, 557.9, 520.5, 491.2, 467.7, 448.4, 432.3, 418.8,
                         406.7, 395.3, 385.1, 376.7, 369.3])
        Qref = np.array([58.8, 250.2, 544.3, 939.5, 1418.1, 1956.9, 2474.5, 3051.1,
                         3881.3, 4180.1, 4180.1, 4180.1, 4180.1, 4180.1, 4180.1, 4180.1,
                         4180.1, 4180.1, 4180.1, 4180.1, 4180.1, 4180.1, 4180.1])
      

        P, T, Q, M, CP, CT, CQ, CM = self.aeroanalysis.evaluate(Uinf, Omega, pitch, coefficients=True)

        print('CP:' + str(CP))

        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Output\Cp_res.txt")

        with open(path, 'w') as f:
            f.write('Cp:\n')
            for i in CP:
                f.write("%s\n" % str(i))
            f.write('\n')
            f.write('Radius: \n')
            f.write(str(self.Rtip))
            f.close()

        '''
        fig, ax1 = plt.subplots()
        ax1.plot(Uinf, CP, 'k')
        ax1.set_xlabel('$\lambda$')
        ax1.set_ylabel('$c_p$')

        ax2 = ax1.twinx()

        ax2.plot(Uinf, P/1000, 'r')
        ax2.set_ylabel('$Power$')
        fig.tight_layout()
        plt.show()

        idx = (Uinf < 15)
        np.testing.assert_allclose(Q[idx]/1e6, Qref[idx]/1e3, atol=0.15)
        np.testing.assert_allclose(P[idx]/1e6, Pref[idx]/1e3, atol=0.2)  # within 0.2 of 1MW
        np.testing.assert_allclose(T[idx]/1e6, Tref[idx]/1e3, atol=0.15)
        '''


if __name__ == '__main__':
    Cp = Performance_coef()
    Cp.setup()
    # Cp.compute()
