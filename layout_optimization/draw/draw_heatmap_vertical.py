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

    def draw(self, filtered_file_path, pos_file_path, temp_hum, title, file_saved):
        read_data = ReadData(filtered_file_path, pos_file_path)
        temp_hum_data = read_data.get_temperature_humidity_data(5)
        pos_data = read_data.get_pos_data()
        #print temp_hum_data
        data = []
        for item in self.sensor_num:
            tmp = []
            tmp.append(float(pos_data[item][0]))
            tmp.append(float(pos_data[item][1]))
            tmp.append(float(pos_data[item][2]))
            tmp.append(float(temp_hum_data[item][4][0]))
            tmp.append(float(temp_hum_data[item][4][1]))
            #print tmp
            #print pos_data[item][0], pos_data[item][1], temp_hum_data[item][0][0]
            #data.append( [int(pos_data[item][0])/10, int(pos_data[item][1])/10, float(temp_hum_data[item][0][0])] )
            data.append(tmp)

        data = np.array(data)

        gridx = np.arange(0.0, 1801.0, 50)
        gridy = np.array([420.0])
        gridz = np.arange(0.0, 560.0, 10.0)

        OK3d = OrdinaryKriging3D(data[:, 0], data[:, 1], data[:, 2], data[:, temp_hum],variogram_model='linear',
                     verbose=False, enable_plotting=False)

        z, ss = OK3d.execute('grid', gridx, gridy, gridz)

        # print z

        res = []
        for itemz in z:
            for itemy in itemz:
                res.append(itemy)
        res = res[::-1]
        res = np.array(res)
        # print res


        #res = [[1,2,3,4,5],[2,2,2,2,2],[3,3,3,3,3],[4,4,4,4,4],[5,5,5,5,5]]

        fig = plt.figure()
        ax = fig.add_subplot(111)

        sys_str = platform.system()
        if sys_str == 'Darwin':
            zhfont = mpl.font_manager.FontProperties(fname='/System/Library/Fonts/PingFang.ttc')
        elif sys_str == 'Windows':
            zhfont = mpl.font_manager.FontProperties(fname='C:/Windows/Fonts/simhei.ttf')        
        plt.xlabel(u'长度(cm)', fontproperties = zhfont, fontsize = 15)
        plt.ylabel(u'高度(cm)', fontproperties = zhfont, fontsize = 15)
        # ax.xaxis.set_label_coords(-10, -0.025)
        plt.title(title, fontproperties = zhfont, fontsize = 15)

        plt.plot([10,10],[10,350],'k-',linewidth=2)
        plt.plot([10,380],[350,550],'k-',linewidth=2)
        plt.plot([380,540],[550,550],'k-',linewidth=2)
        plt.plot([540,920],[550,380],'k-',linewidth=2)
        plt.plot([920,920],[380,320],'k-',linewidth=2)
        plt.plot([920,1100],[320,320],'k-',linewidth=2)
        plt.plot([1100,1100],[320,380],'k-',linewidth=2)
        plt.plot([1100,1400],[380,550],'k-',linewidth=2)
        plt.plot([1400,1500],[550,550],'k-',linewidth=2)
        plt.plot([1500,1800],[550,380],'k-',linewidth=2)

        
        im = ax.imshow(res, interpolation='bicubic', extent=[0, 1801.0, 0, 560.0])


        #im = ax.imshow(res, interpolation='bicubic')
        ax.grid(True)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.5)
        cbar = plt.colorbar(im, cax = cax)
        if temp_hum == 3:
            cbar.set_label('$^oC$')
        else:
            cbar.set_label('RH%')
        #plt.show()
        plt.savefig(file_saved)


if __name__ == '__main__':
    dh = DrawHeatMap()
    dh.draw("../data/filter_data","../data/pos/pos.csv", 3 ,u"洞窟洞窟中心轴线垂直面温度热力图", u"../data/result/洞窟洞窟中心轴线垂直面温度热力图.png")
    dh.draw("../data/filter_data","../data/pos/pos.csv", 4 ,u"洞窟洞窟中心轴线垂直面湿度热力图", u"../data/result/洞窟洞窟中心轴线垂直面湿度热力图.png")
    #3 代表温度， 4 代表湿度

    # print read_data.get_temperature_humidity_data(1)
    # print read_data.get_pos_data()