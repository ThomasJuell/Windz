import numpy as np
from math import pi, sin, atan
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d

def blade_geometry(Rtip, r, B, Cl, tsr, c_max, plot=False):
    chord = [] 
    # scaling value derived from previous blade design from NREL 
    circ_af_coef = [0.056222222, 0.061174603, 0.066142857]
    for i in range(3):
        chord.append(Rtip*circ_af_coef[i])
    # The three first points are the circular profiles and has 0 lift, therefor bypassing with i+3
    for i in range(len(r)-3):
        c = (1/B) * ((16*pi*r[i+3])/Cl[i]) * sin((1/3) * atan(Rtip/(tsr*r[i+3])))**2
        if c > c_max:
            chord.append(c_max)
        else:
            chord.append(c)

    if plot == True:
        chord_smooth = gaussian_filter1d(chord, sigma=0.5)
        plt.plot(r,chord_smooth)
        plt.ylim(0,6)
        plt.xlabel('Radius of blade')
        plt.ylabel('Chord length')
        plt.show()

    return chord
    
if __name__ == '__main__':
    Rtip = 63
    r = np.array([Rtip*0.045503175, Rtip*0.088888889, Rtip*0.132274603, Rtip*0.186507937, Rtip*0.251587302, Rtip*0.316666667, Rtip*0.381746032, Rtip*0.446825397, Rtip*0.511904762, Rtip*0.576984127, Rtip*0.642063492, Rtip*0.707142857, Rtip*0.772222222, Rtip*0.837301587, Rtip*0.891534921, Rtip*0.934920635, Rtip*0.978306349])
    B = 3
    tsr = 7.55
    c_max = 5
    Cl = [1.3871, 1.3871, 1.3871, 1.3871, 1.464, 1.464, 1.464, 1.464, 1.4509, 1.4509, 1.4509, 1.4509, 1.4509, 1.4509]
    chord = np.array(blade_geometry(Rtip, r, B, Cl, tsr, c_max, plot=True))
    print(chord)

