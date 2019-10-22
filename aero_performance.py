import numpy as np
import matplotlib.pyplot as plt
import re

with open('C:/Users/Thomas/Documents/S818_output3_extrap.txt', 'r') as f:
    data = f.readlines()

alpha, cl, cd, cm = [], [], [], []

# parsing through data lines and stopping at EOT if it exists. This is because I had trouble with string to float converting. 
# for some reason the string EOT could not be detected unless I used re.
for i in data[13:]:
    if re.match('EOT',i):
        break
    else:
        alpha.append(float(i.split()[0]))
        cl.append(float(i.split()[1]))
        cd.append(float(i.split()[2]))
        cm.append(float(i.split()[3]))

# Cl/Cd ratio
l_d_ratio = []
for i in range(0,len(cl)):
    l_d_ratio.append(cl[i]/cd[i])

print('Maximum lift coefficient is {} at AOA {}'.format(max(cl), alpha[cl.index(max(cl))]))
print('Maximum drag coefficient is {} at AOA {}'.format(max(cd), alpha[cd.index(max(cd))]))
print('Maximum lift/drag ratio is {} at AOA {}'.format(max(l_d_ratio), alpha[l_d_ratio.index(max(l_d_ratio))]))

fig, axes = plt.subplots(2,2)

# first plot
axes[0,0].plot(alpha,cl)
axes[0,0].set_xlim(-180,180)
axes[0,0].set_ylabel('Cl')

# second plot
axes[0,1].plot(alpha,cd)
axes[0,1].set_xlim(-180,180)
axes[0,1].set_ylabel('Cd')

# third plot
axes[1,0].plot(alpha,l_d_ratio)
axes[1,0].set_xlim(-180,180)
axes[1,0].set_xlabel('AOA')
axes[1,0].set_ylabel('Cl/Cd')

# fourth plot
# plotter tsr vs. Cp siden det passer bedre enn Cl cs. Cd
with open('C:/Users/Thomas/OneDrive/Tieto/Scripts/Output/Cp_res.txt', 'r') as f:
    res = [line.rstrip() for line in f]
    
res = res[1:24]

Cp = []
for i in res:
    Cp.append(float(i))

wind = np.linspace(3,25,len(Cp))

axes[1,1].plot(wind,Cp)
axes[1,1].set_xlim(2,26)
axes[1,1].set_xlabel('Wind Speed')
axes[1,1].set_ylabel('Cp')

plt.tight_layout()
plt.show()