import math
import numpy as np




def sphr_to_cart(r, theta, phi):

	if isinstance(theta, float) and isinstance(phi, float):
		x_point = r*math.sin(theta)*math.cos(phi) 
		y_point = r*math.sin(theta)*math.sin(phi)
		z_point = r*math.cos(theta)
		cartesian_point = (x_point, y_point, z_point)
	
		return cartesian_point

	elif isinstance(theta, np.ndarray) and isinstance(phi, np.ndarray):
		x_array = r*np.sin(theta)*np.cos(phi) 
		y_array = r*np.sin(theta)*np.sin(phi)
		z_array = r*np.cos(theta)

		return x_array, y_array, z_array




def golden_ratio_eq_sphr_pts(r=1, N=100):

	from numpy import pi, cos, sin, arccos, arange

	indices = arange(0, N, dtype=float) + 0.5

	phi = arccos(1 - 2*indices/N)
	theta = pi * (1 + 5**0.5) * indices

	x = r*cos(theta)*sin(phi)
	y = r*sin(theta)*sin(phi)
	z = r*cos(phi)

	return x,y,z







def equidst_sphr_pts(r=1, N=100):

	a = 4 * math.pi * r**2 / N
	d = math.sqrt(a)
	M_theta = round(math.pi / d)
	d_theta = math.pi / M_theta
	d_phi = a / d_theta

	phi_vals = []
	theta_vals = []

	for m in range(M_theta):
		theta = math.pi * (m + 0.5) / M_theta
		M_phi = round(2 * math.pi * math.sin(theta) / d_phi)

		for n in range(M_phi):
			phi = 2 * math.pi * n / M_phi
			
			phi_vals.append(phi)
			theta_vals.append(theta)
		
	phi_vals = np.array(phi_vals)
	theta_vals = np.array(theta_vals)

	x,y,z = sphr_to_cart(r, theta_vals, phi_vals)

	return x,y,z

