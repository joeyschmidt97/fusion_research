from typing import Tuple
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

import numpy as np


def sphere_to_disk(cartesian_points:Tuple[np.ndarray, np.ndarray, np.ndarray], 
                   color_values:np.array=None,
                   units:Tuple[str,str,str]=('x','y','z'), origin:Tuple[float,float,float]=(0,0,0), 
                   dist_opacity_origin:bool = True, plot_3D:bool = False):

    x = cartesian_points[0]
    y = cartesian_points[1]
    z = cartesian_points[2]

    x0 = origin[0]
    y0 = origin[1]
    z0 = origin[2]

    del_x = x - x0
    del_y = y - y0
    del_z = z - z0

    r = np.sqrt(del_x**2 + del_y**2 + del_z**2)

    if dist_opacity_origin:    

        # Define the desired range for scaled r
        opac_min = 0.4
        opac_max = 0.8
        min_r = np.min(r)
        max_r = np.max(r)

        # Scale the values of r to the desired range
        opac_r = ((r - min_r) / (max_r - min_r)) * (opac_max - opac_min) + opac_min

    else:
        max_r = np.max(r)
        opac_r = 0.5


    x_units = units[0]
    y_units = units[1]
    z_units = units[2]

    ref_points = [(max_r,0,0, "+" + x_units), (-max_r,0,0, "-" + x_units), 
                  (0,max_r,0, "+" + y_units), (0,-max_r,0, "-" + y_units),
                  (0,0,max_r, "+" + z_units), (0,0,-max_r, "-" + z_units)]



    if color_values is None:        
        point_colors = np.ones_like(del_x)
        norm = Normalize(vmin=0, vmax=1)
    else:
        point_colors = (color_values - color_values.min()) / (color_values.max() - color_values.min())
        norm = Normalize(vmin=color_values.min(), vmax=color_values.max()) 

    if plot_3D:
        fig = plt.figure(figsize=(12, 5))
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122, projection='3d')  # Set projection to 3D

        sc2 = ax2.scatter(x,y,z, c=point_colors, cmap='plasma', edgecolor='black', norm=norm)
        ax2.scatter(x0,y0,z0, c='red', s=100, marker='*')
        ax2.set_title('3D Projection')
        ax2.set_xlabel(x_units)
        ax2.set_ylabel(y_units)
        ax2.set_zlabel(z_units)

    else:
        fig = plt.figure(figsize=(12, 5))
        ax1 = fig.add_subplot(121)


    x_disk, y_disk = cartesian_to_disk(del_x, del_y, del_z)
    ax1.scatter(x_disk, y_disk, alpha=opac_r, c=point_colors, cmap='plasma', edgecolor='black', norm=norm)


    for (x_axis, y_axis, z_axis, axis_label) in ref_points:
        xd_ref, yd_ref = cartesian_to_disk(x_axis, y_axis, z_axis)
        ax1.scatter(xd_ref, yd_ref, alpha=1, marker='o', edgecolors='black', facecolors='none')
        ax1.text(xd_ref, yd_ref, axis_label, color='black', fontsize=10, ha='left', va='bottom')


    outer_theta_disk = np.linspace(0, 2*np.pi, 100)
    x_disk_circle = np.cos(outer_theta_disk)*np.pi
    y_disk_circle = np.sin(outer_theta_disk)*np.pi
    ax1.plot(x_disk_circle, y_disk_circle, color='black', linestyle='-', alpha=0.5)
    ax1.plot(x_disk_circle/2, y_disk_circle/2, color='black', linestyle=':')
    ax1.set_title('Sphere-Disk Projection')

    
    cbar_ax = fig.add_axes([0.93, 0.15, 0.02, 0.6])  # positioning the colorbar
    cbar = fig.colorbar(sc2, cax=cbar_ax)
    cbar.set_label(r'$Q_{EM}/(Q_{ES} - Q_{EM})$', fontsize=14)
    

    plt.show()







def cartesian_to_disk(x_array, y_array, z_array, disk_rad_match_real_rad:bool = False):

	x_array = x_array + 1e-16
	y_array = y_array + 1e-16
	z_array = z_array + 1e-16

	r = np.sqrt(x_array**2 + y_array**2 + z_array**2)
	theta = np.arccos(z_array/r)

	arg = x_array/np.sqrt(x_array**2 + y_array**2)
	phi = np.where(y_array < 0, -np.arccos(arg), np.arccos(arg))

	if disk_rad_match_real_rad:
		disk_r = r
	else:
		disk_r = 1

	x_disk = disk_r*theta*np.cos(phi)
	y_disk = disk_r*theta*np.sin(phi)

	return x_disk, y_disk


