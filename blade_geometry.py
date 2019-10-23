import numpy as np
from math import pi, sin

def blade_geometry(Rtip, r, B, Cl, tsp):
    chord = [] 
    circ_af_coef = [0.056222222, 0.061174603, 0.066142857]
    for i in range(len(r)):
        # if i == 0 or 1 or 2:
        #     np.append(chord, r[i]*circ_af_coef[i])
        # elif i > 2:
        c = (1/B) * ((16*pi*r[i])/Cl[i]) * sin((1/3) * sin(Rtip/(tsp*r[i]))**(-1))**2
        # np.append(chord, c)
        chord.append(c)
    return chord
    
if __name__ == '__main__':
    Rtip = 63
    r = np.array([Rtip*0.045503175, Rtip*0.088888889, Rtip*0.132274603, Rtip*0.186507937, Rtip*0.251587302, Rtip*0.316666667, Rtip*0.381746032, Rtip*0.446825397, Rtip*0.511904762, Rtip*0.576984127, Rtip*0.642063492, Rtip*0.707142857, Rtip*0.772222222, Rtip*0.837301587, Rtip*0.891534921, Rtip*0.934920635, Rtip*0.978306349])
    B = 3
    tsp = 7.55
    Cl = [0.01, 0.01, 0.01, 1.3871, 1.3871, 1.3871, 1.3871, 1.464, 1.464, 1.464, 1.464, 1.4509, 1.4509, 1.4509, 1.4509, 1.4509, 1.4509]
    chord = blade_geometry(Rtip, r, B, Cl, tsp)
    print(chord)
    print(len(chord))

