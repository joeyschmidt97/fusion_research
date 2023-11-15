from equidistant_sphere_points import cart_to_disk

import matplotlib.pyplot as plt
import numpy as np


def plot_simulation_disk(point_dict: dict, plot_3D:bool = False):

    x = point_dict['x']['values']
    y = point_dict['y']['values']
    z = point_dict['z']['values']

    x_units = point_dict['x'].get('units', 'x')
    y_units = point_dict['y'].get('units', 'y')
    z_units = point_dict['z'].get('units', 'z')

    
    r = max(np.sqrt(x**2 + y**2 + z**2))
    ref_points = [(r,0,0, "+" + x_units), (-r,0,0, "-" + x_units), 
                  (0,r,0, "+" + y_units), (0,-r,0, "-" + y_units),
                  (0,0,r, "+" + z_units), (0,0,-r, "-" + z_units)]



    if plot_3D:
        fig = plt.figure(figsize=(12, 5))
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122, projection='3d')  # Set projection to 3D

        ax2.scatter(x,y,z)  # Add z_temp as the third dimension
        
        
        for (x_axis, y_axis, z_axis, axis_label) in ref_points:
            ax2.scatter(x_axis, y_axis, z_axis, alpha=1, marker='o', edgecolors='black', facecolors='none')  # Add z_temp as the third dimension
            ax2.text(x_axis, y_axis, z_axis, axis_label, color='black', fontsize=10, ha='right', va='bottom')

        ax2.set_title('3D Projection')
        ax2.set_xlabel(x_units)
        ax2.set_ylabel(y_units)
        ax2.set_zlabel(z_units)
    else:
        fig = plt.figure(figsize=(12, 5))
        ax1 = fig.add_subplot(121)


    x_disk, y_disk = cart_to_disk(x, y, z)
    ax1.scatter(x_disk, y_disk, alpha=0.2)


    for (x_axis, y_axis, z_axis, axis_label) in ref_points:
        xd_ref, yd_ref = cart_to_disk(x_axis, y_axis, z_axis)
        ax1.scatter(xd_ref, yd_ref, alpha=1, marker='o', edgecolors='black', facecolors='none')
        ax1.text(xd_ref, yd_ref, axis_label, color='black', fontsize=10, ha='left', va='bottom')


    theta_disk = np.linspace(0, 2*np.pi, 100)
    x_disk_circle = r*np.cos(theta_disk)*np.pi
    y_disk_circle = r*np.sin(theta_disk)*np.pi
    ax1.plot(x_disk_circle, y_disk_circle, color='black', linestyle='--')
    ax1.set_title('Subplot 1')


    plt.show()





def generate_axis_points(r):

    ref_points = [(r,0,0), (-r,0,0), 
                  (0,r,0), (0,-r,0),
                  (0,0,r), (0,0,-r)]

    x_ref_list = []
    y_ref_list = []
    z_ref_list = []

    for x_ref, y_ref, z_ref in ref_points:
        x_ref_list.append(x_ref)
        y_ref_list.append(y_ref)
        z_ref_list.append(z_ref)

    x_axis = np.array(x_ref_list)
    y_axis = np.array(y_ref_list)
    z_axis = np.array(z_ref_list)

    return x_axis, y_axis, z_axis

