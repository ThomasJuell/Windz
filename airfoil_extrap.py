import matplotlib.pyplot as plt
import numpy as np
import os

from wisdem.airfoilprep.airfoilprep import Airfoil, Polar

class Extrapolation:
    def __init__(self, file_in):
        # Takes polar data file which is cleaned/prepped
        path = 'C:/Users/Thomas/OneDrive/Tieto/Airfoils/xfoil/' + file_in
        with open(path, 'r') as f:
            self.data = f.readlines()
        self.file_in = file_in

    def set_up(self):
        '''
        parsing through the polar data given from xfoil and cutting out the 
        data points that are above and under cl max and min
        '''
        # Finding the Reynold's number used for the xfoil analysis. NB! need to be the same output as xfoil gives.
        # self.Re = []
        for i in self.data:
            temp=[]
            if 'Re =' in i:
                temp.append(i.split())
                self.Re = float(temp[0][5] + 'e6')

        # Since I have changed the xfoil session to analysis from 0 to -20 and then 0.25 to 20, 
        # the polar data needs to be rearanged from -20 to 20.
        alfa_first = []
        alfa_second = []
        data1 = []

        for i in self.data[12:]:
            data1.append(i.split())

        for i in data1:
            if float(i[0]) <= 0:
                alfa_first.append(i)
            elif float(i[0]) > 0:
                alfa_second.append(i)

        data1 = self.data[0:12] + alfa_first[::-1] + alfa_second
        
        # Splitting the data into correct arrays. Starting at line 13 since thats where the data starts.
        self.alpha, self.cl, self.cd, self.cm = [], [], [], []
        for i in data1[12:]:
            self.alpha.append(float(i[0]))
            self.cl.append(float(i[1]))
            self.cd.append(float(i[2]))
            self.cm.append(float(i[3]))

        # stripping all the data points over and under cl max and min
        cl_max_index = self.cl.index(max(self.cl))
        cl_min_index = self.cl.index(min(self.cl))
        self.alpha = self.alpha[cl_min_index:cl_max_index]
        self.cl = self.cl[cl_min_index:cl_max_index]
        self.cd = self.cd[cl_min_index:cl_max_index]
        self.cm = self.cm[cl_min_index:cl_max_index]

    def correction_3D(self, r_over_R, chord_over_r, tsr):



    def polar_extrap(self, file_out=None, plot=False):
        # Takes an output name for new extrapolated polar points.
        if file_out is None:
            name, ext = os.path.splitext(self.file_in)
            file_out = name + '_extrap' + ext
        # Defines section lift, drag, and pitching moment coefficients as a
        # function of angle of attack at a particular Reynolds number.
        polar1 = Polar(self.Re, self.alpha, self.cl, self.cd, self.cm)
        af = Airfoil([polar1])

        # Finding Cd max for extrapolation
        cd_max = max(self.cd)
        # Making alpha -180 to 180 deg so that ccblade can handle the data (Viterna Method)
        afext = af.extrapolate(cd_max)
        afext.writeToAerodynFile(file_out)

        if plot == True:
            afext.plot(single_figure=False)
            plt.show()

if __name__ == '__main__':
    main = Extrapolation('S830_output.txt')
    main.set_up()
    main.polar_extrap(plot=True)