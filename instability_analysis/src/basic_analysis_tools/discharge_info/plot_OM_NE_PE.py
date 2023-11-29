import sys
# sys.path.insert(1, '/global/u1/j/joeschm/jojo_github/ST_research/coding_tools')
from instability_analysis.src.basic_analysis_tools.discharge_info.PRE_profiles_from_iterdb import auto_create_profiles

sys.path.insert(1, '/global/u1/j/joeschm/ifs_scripts')
from mtmDopplerFreqs_JOEY import omega_star_data

import matplotlib.pyplot as plt
import numpy as np


def round_points(x_point, i, j, plot_dict, titles):
        x = plot_dict[titles[i]]['x']
        y = plot_dict[titles[i]]['y']

        x_point = plot_dict[titles[j]]['x_input']
        x_point = x[abs(x_point - x).argmin(axis=0)]
        x_ind = np.where(x == x_point)[0][0]

        x_curve = round(x_point, 7)
        y_curve = y[x_ind]

        return x_curve, y_curve


def multiplot_PE_NE_OM(filepath, point_list, display_all_points = True):
        omega_star_dict = omega_star_data(filepath)
        uni_rhot = omega_star_dict['uni_rhot']
        mtmFreq = omega_star_dict['mtmFreq']
        n0_global = omega_star_dict['n0_global']

        profile_dict, g_plot_dict = auto_create_profiles(filepath)
        rhot = profile_dict['PE']['rhot']
        pe = profile_dict['PE']['arr']
        pe_units = profile_dict['PE']['units']
        ne = profile_dict['NE']['arr']
        ne_units = profile_dict['NE']['units']

        plot_dict = {'Electron Pressure': 
                {'x': rhot, 'y': pe,'units': pe_units, 'x_input': point_list[0]}, 
                'Electron Density': 
                {'x': rhot, 'y': ne,'units': ne_units, 'x_input': point_list[1]}, 
                'Electron Diamagnetic (MTM in plasma frame)': 
                {'x': uni_rhot, 'y': mtmFreq,'units': 'kHz, n=' + str(n0_global), 'x_input': point_list[2]}
                }

        titles = list(plot_dict.keys())

        fig, axs = plt.subplots(1,3, figsize = (18,5))
        axs = axs.ravel()

        for i in range(0, len(titles)):
                x = plot_dict[titles[i]]['x']
                y = plot_dict[titles[i]]['y']
                units = plot_dict[titles[i]]['units']

                x_point_PE = plot_dict[titles[0]]['x_input']
                x_point_NE = plot_dict[titles[1]]['x_input']
                x_point_OM = plot_dict[titles[2]]['x_input']

                x_curve_PE, y_curve_PE = round_points(x_point_PE, i, 0, plot_dict, titles)
                x_curve_NE, y_curve_NE = round_points(x_point_NE, i, 1, plot_dict, titles)
                x_curve_OM, y_curve_OM = round_points(x_point_OM, i, 2, plot_dict, titles)

                axs[i].plot(x,y, label= '('+units+')')
                axs[i].title.set_text(titles[i])
                axs[i].legend(loc='lower left')

                if display_all_points:

                        axs[i].scatter(x_curve_PE, y_curve_PE, c='blue')
                        axs[i].text(x_curve_PE*1.02, y_curve_PE*1.02, 'PE')

                        axs[i].scatter(x_curve_NE, y_curve_NE, c='red')
                        axs[i].text(x_curve_NE*1.02, y_curve_NE*1.02, 'NE')
                        
                        axs[i].scatter(x_curve_OM, y_curve_OM, c='green')
                        axs[i].text(x_curve_OM*1.02, y_curve_OM*1.02, 'OM')
                
                else:
                        if i == 0:
                                axs[i].scatter(x_curve_PE, y_curve_PE, c='blue')
                                axs[i].text(x_curve_PE*1.02, y_curve_PE*1.02, 'PE')
                        elif i == 1:
                                axs[i].scatter(x_curve_NE, y_curve_NE, c='red')
                                axs[i].text(x_curve_NE*1.02, y_curve_NE*1.02, 'NE')
                        elif i == 2:
                                axs[i].scatter(x_curve_OM, y_curve_OM, c='green')
                                axs[i].text(x_curve_OM*1.02, y_curve_OM*1.02, 'OM')

                # offset = 300
                # if offset > x_ind: offset = 0 

                # axs[i+3].plot(x[x_ind - offset:],y[x_ind - offset:], label= '('+units+')')
                # axs[i+3].title.set_text(str(titles[i]) + ' (Zoomed)')
                # axs[i+3].legend(loc='lower left')
                # axs[i+3].scatter(x_point, y_point, c='red')
                # axs[i+3].text(x_point*1.02, y_point*1.02, 'x: ' + str(x_point))
                
                # print('Pedestal top (x-location) for ' + str(titles[i]) + ': ' + str(x_point))

        fig.show()