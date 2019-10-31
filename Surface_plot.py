import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits import mplot3d

# grabbing the pipe-it results
basepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Results.xlsx')
data = pd.read_excel(basepath, sheet_name='S8xx_2019')
df = pd.DataFrame(data, columns=['Radius', 'Power', 'PValue'])

name = 'S8XX'
Radius = df['Radius']
Power = df['Power']
PValue = df['PValue']

# defining the 3D-trendline and plotting scatter points
x = np.linspace(min(Radius),max(Radius), len(Radius))
y = np.linspace(min(Power),max(Power), len(PValue))
z = np.linspace(min(PValue),max(PValue), len(PValue))
ax = plt.axes(projection='3d')
ax.plot3D(x, y, z, 'gray')
ax.scatter3D(Radius, Power, PValue, color='green', label=name)
# ax.scatter3D(Radius_S8xx, Power_S8xx, PValue_S8xx, color='red', label='S8xx')
ax.set_xlabel('Radius [m]')
ax.set_ylabel('Power [kW]')
ax.set_zlabel('Present Value [NOK]')
ax.legend(loc='best', title='Airfoil Set')
plt.tight_layout()

# plotting the 3D-surface plot
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_trisurf(Radius, Power, PValue, cmap='coolwarm', edgecolor='none')
ax.set_title('Surface Plot of {} Airfoil'.format(name))
ax.set_xlabel('Radius [m]')
ax.set_ylabel('Power [kW]')
ax.set_zlabel('Present Value [NOK]')
plt.tight_layout()
plt.show()
