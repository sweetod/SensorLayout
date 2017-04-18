#-*- coding:utf-8 -*-

from pykrige.ok import OrdinaryKriging
from pykrige.ok3d import OrdinaryKriging3D
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import pykrige.kriging_tools as kt
import matplotlib.pyplot as plt
import matplotlib as mpl
import platform
import csv
import sys
sys.path.append("..")
from draw.draw_layout import drawLayout
from file_input_output.read_data import ReadData

class DrawHeatMap:
    def __init__(self):
        self.bottom = ['10728412', '10728506', '10728435', '10728391', '10728399', '10728527', '10728419', '10728404', '10728422', '10728387']
        self.mid = []
        self.up = []
        self.sensor_num = ['10728412','10728515','10728382','10728506','10728402','10728400','10728435','10728517','10728383',
        '10728534','10728432','10728401','10728391','10728437','10728525','10728399','10728518','10728442','10728527','10728390',
        '10728405','10728419','10728425','10728439','10728404','10728408','10728522','10728396','10728422','10728507','10728513',
        '10728387','10728385','10728519']

    def draw(self, filtered_file_path, pos_file_path, temp_hum, low_mid_high, title, file_saved,data_num):
        read_data = ReadData(filtered_file_path, pos_file_path)
        temp_hum_data = read_data.get_temperature_humidity_data(14355)
        pos_data = read_data.get_pos_data()
        #print temp_hum_data
        data = []
        for item in self.sensor_num:
            tmp = []
            tmp.append(float(pos_data[item][0]))
            tmp.append(float(pos_data[item][1]))
            tmp.append(float(pos_data[item][2]))
            tmp.append(float(temp_hum_data[item][data_num][0]))
            tmp.append(float(temp_hum_data[item][data_num][1]))
            #print tmp
            #print pos_data[item][0], pos_data[item][1], temp_hum_data[item][0][0]
            #data.append( [int(pos_data[item][0])/10, int(pos_data[item][1])/10, float(temp_hum_data[item][0][0])] )
            data.append(tmp)

        data = np.array(data)

        gridx = np.arange(0.0, 1901.0, 50.0)
        gridy = np.arange(0.0, 901.0, 50.0)
        gridz = np.array([0.0, 180.0, 360.0])


        OK3d = OrdinaryKriging3D(data[:, 0], data[:, 1], data[:, 2], data[:, temp_hum],variogram_model='linear',
                     verbose=False, enable_plotting=False)

        z, ss = OK3d.execute('grid', gridx, gridy, gridz)

        #print z[0]
        fig = plt.figure()
        ax = fig.add_subplot(111)

        #plt.style.use('ggplot')

        sys_str = platform.system()
        if sys_str == 'Darwin':
            zhfont = mpl.font_manager.FontProperties(fname='/System/Library/Fonts/PingFang.ttc')
        elif sys_str == 'Windows':
            zhfont = mpl.font_manager.FontProperties(fname='C:/Windows/Fonts/simhei.ttf')        
        plt.xlabel(u'长度(cm)', fontproperties = zhfont, fontsize = 15)
        plt.ylabel(u'宽度(cm)', fontproperties = zhfont, fontsize = 15)
        # ax.xaxis.set_label_coords(-10, -0.025)
        plt.title(title, fontproperties = zhfont, fontsize = 15)

        plt.plot([10,10],[20,850],'k-',linewidth=2)
        plt.plot([10,930],[20,20],'k-',linewidth=2)
        plt.plot([10,930],[850,850],'k-',linewidth=2)
        plt.plot([930,930],[10,300],'k-',linewidth=2)
        plt.plot([930,930],[550,850],'k-',linewidth=2)
        plt.plot([930,1110],[550,550],'k-',linewidth=2)
        plt.plot([930,1110],[300,300],'k-',linewidth=2)
        plt.plot([1110,1110],[300,100],'k-',linewidth=2)
        plt.plot([1110,1110],[550,700],'k-',linewidth=2)
        plt.plot([1110,1810],[700,700],'k-',linewidth=2)
        plt.plot([1110,1810],[100,100],'k-',linewidth=2)

        
        
        if temp_hum == 3:
            im = ax.imshow(z[low_mid_high], interpolation='bicubic', extent=[0, 1901, 0, 901], vmin=8.5, vmax=15.5)
            #ax.grid(True)
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.5)
            cbar = plt.colorbar(im, cax = cax)
            cbar.set_label('$^oC$')
        else:
            im = ax.imshow(z[low_mid_high], interpolation='bicubic', extent=[0, 1901, 0, 901], vmin=19, vmax=27)
            #ax.grid(True)
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.5)
            cbar = plt.colorbar(im, cax = cax)
            cbar.set_label('RH%')

        # plt.colorbar(im)

        # plt.figure(3)
        # plt.imshow(z[low_mid_high], interpolation='bicubic', extent=[0, 1800, 0, 840])
        # plt.grid(True)

        #plt.show()
        plt.savefig(file_saved)
        plt.close(fig)


if __name__ == '__main__':
    dh = DrawHeatMap()
    for i in range(1197):
        # dh.draw("../data/filter_data","../data/pos/pos.csv", 3, 0 ,u"高度为0cm时的洞窟温度热力图", u"../data/result/heat_0/"+str(i)+u".png",i)
        dh.draw("../data/filter_data","../data/pos/pos.csv", 3, 1 ,u"高度为180cm时的洞窟温度热力图", u"../data/result/heat_180/"+str(i)+u".png",i)
        dh.draw("../data/filter_data","../data/pos/pos.csv", 3, 2 ,u"高度为360cm时的洞窟温度热力图", u"../data/result/heat_360/"+str(i)+u".png",i)
        dh.draw("../data/filter_data","../data/pos/pos.csv", 4, 0 ,u"高度为0cm时的洞窟湿度热力图", u"../data/result/hum_0/"+str(i)+u".png",i)
        dh.draw("../data/filter_data","../data/pos/pos.csv", 4, 1 ,u"高度为180cm时的洞窟湿度热力图", u"../data/result/hum_180/"+str(i)+u".png",i)
        dh.draw("../data/filter_data","../data/pos/pos.csv", 4, 2 ,u"高度为360cm时的洞窟湿度热力图", u"../data/result/hum_360/"+str(i)+u".png",i)
    #3 代表温度， 4 代表湿度

    # print read_data.get_temperature_humidity_data(1)
    # print read_data.get_pos_data()