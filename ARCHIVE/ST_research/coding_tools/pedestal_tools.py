import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter




def pedestal_points(x,y,plot=False, x_lim=0):
    from scipy.signal import savgol_filter
    
    y = savgol_filter(y, 51, 3)

    dy = np.gradient(y,x)
    dy = savgol_filter(dy, 51, 5)
    
    ddy = np.gradient(dy,x)  #Second order of pressure
    ddy = savgol_filter(ddy, 51, 5) # window size 51, polynomial order 5

    ped_mid = x[np.argmin(dy)]
    ped_top = x[np.argmin(ddy)]
    ped_bot = x[np.argmax(ddy)]
    y_med = y[x == ped_mid]
    y_top = y[x == ped_top]
    y_bot = y[x == ped_bot]

    if plot == True:
        y_cut = y[x > x_lim]
        dy_cut = dy[x > x_lim]
        ddy_cut = ddy[x > x_lim]
        x_cut = x[x > x_lim]

        plt.clf()
        fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize = (18,5))

        ax1.plot(x_cut,y_cut,label="p")
        ax1.scatter(ped_mid, y_med, c='red')
        ax1.scatter(ped_top, y_top, c='blue')
        ax1.scatter(ped_bot, y_bot, c='green')

        ax2.plot(x_cut,dy_cut,label="dp")
        ax2.axhline(y=0, label="Zero Axis", color="red")

        ax3.plot(x_cut,ddy_cut,label="ddp")
        ax3.axhline(y=0, label="Zero Axis", color="red")

        fig.suptitle('Regular')
        plt.show()


    return ped_top, ped_mid, ped_bot





def pedestal_points_scaled(x,y,plot=False, x_lim=0, scale=1):
    from scipy.signal import savgol_filter

    y = savgol_filter(y, 51, 3)
    
    dy = np.gradient(y,x)
    dy = savgol_filter(dy, 51, 3)
    
    ddy = np.gradient(dy,x)  #Second order of pressure
    ddy = savgol_filter(ddy, 51, 3) # window size 51, polynomial order 5

    dy_scaled = dy*x**scale
    ddy_scaled = ddy*x**scale

    ped_mid = x[np.argmin(dy_scaled)]
    ped_top = x[np.argmin(ddy_scaled)]
    ped_bot = x[np.argmax(ddy_scaled)]
    y_med = y[x == ped_mid]
    y_top = y[x == ped_top]
    y_bot = y[x == ped_bot]


    if plot == True:
        y_cut = y[x > x_lim]
        dy_cut = dy_scaled[x > x_lim]
        ddy_cut = ddy_scaled[x > x_lim]
        x_cut = x[x > x_lim]

        plt.clf()
        fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize = (18,5))

        ax1.plot(x_cut,y_cut,label="p")
        ax1.scatter(ped_mid, y_med, c='red')
        ax1.scatter(ped_top, y_top, c='blue')
        ax1.scatter(ped_bot, y_bot, c='green')

        ax2.plot(x_cut,dy_cut,label="dp")
        ax2.axhline(y=0, label="Zero Axis", color="red")

        ax3.plot(x_cut,ddy_cut,label="ddp")
        ax3.axhline(y=0, label="Zero Axis", color="red")

        fig.suptitle('Scaled')
        plt.show()

    return ped_top, ped_mid, ped_bot







def array_splice(y, x, x_bot, x_top):    
    x_bot_cut = x[x > x_bot]
    y_bot_cut = y[x > x_bot]
    
    x_array_cut = x_bot_cut[x_bot_cut < x_top]
    y_array_cut = y_bot_cut[x_bot_cut < x_top]
    
    return y_array_cut

