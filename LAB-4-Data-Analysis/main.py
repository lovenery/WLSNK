from os import path, listdir
from pprint import pprint
from math import sin, cos, sqrt, atan2, radians
from json import load
from sys import exit
import numpy as np
import matplotlib.pyplot as plt

from locations import *

"""
PLEASE EXTRACT testData.zip FIRST!

Example Data:
'testData/1/106522097_008000000000e332_1_1_7_1.txt'
'testData/(1~412)/106522097_008000000000e332_(1)_(1~20)_(7~10)_(1~5).txt'
'testData/(location)/(student ID)_(device EUI)_(location)_(power)_(sf)_(count).txt'

gateway EUI:
工程五館|GATEWAY1|00800000a00006d4|(24.96715, 121.18766)|西
總圖書館|GATEWAY2|00800000a0000a1c|(24.96822, 121.19437)|東
科學五館|GATEWAY3|00800000a0000ed1|(24.97154, 121.19268)|北

References:
https://stackoverflow.com/questions/2835559/parsing-values-from-a-json-file
https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
https://stackoverflow.com/questions/543309/programmatically-stop-execution-of-python-script
https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
https://stackoverflow.com/questions/2282727/draw-points-using-matplotlib-pyplot-x1-y1-x2-y2
https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.linalg.lstsq.html
"""

base_dir = path.abspath(path.dirname(__file__))
result_dict = {}
for i in range(1, 21):
    for j in range(7, 11):
        result_dict['{}_{}'.format(i, j)] = [] # init

def get_distance(tuple1, tuple2):
    R = 6373.0 # approximate radius of earth in km
    
    lon1 = radians(tuple1[0])
    lon2 = radians(tuple2[0])
    lat1 = radians(tuple1[1])
    lat2 = radians(tuple2[1])

    d_lon = lon2 - lon1
    d_lat = lat2 - lat1

    a = sin(d_lat / 2)**2 + cos(lat1) * cos(lat2) * sin(d_lon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c # km

    return round(distance * 1000, 2) # meter

def get_which_gateway(EUI):
    if EUI == '00800000a00006d4': # GATEWAY1_EUI
        return 0
    elif EUI == '00800000a0000a1c': # GATEWAY2_EUI
        return 1
    elif EUI == '00800000a0000ed1': # GATEWAY3_EUI
        return 2
    else:
        exit('Error: gateway EUI not found.')

def single_location_data(relative_path, student_id, device_EUI, testpoint_location_index):
    for i in range(1, 21):
        for j in range(7, 11):
            gateway_rssi = [0, 0, 0] # gateway1's rssi, gateway2's rssi, gateway3's rssi
            gateway_count = [0, 0, 0] # gateway1's count, gateway2's count, gateway3's count

            for k in range(1, 6):
                file_name = '{}_{}_{}_{}_{}_{}.txt'.format(student_id, device_EUI, testpoint_location_index + 1, i, j, k)
                full_path = path.join(base_dir, relative_path, file_name)
                print(full_path)
                with open(full_path) as fd:
                    data = load(fd)

                gateway_index = get_which_gateway(data['gateway'])
                gateway_count[gateway_index] += 1
                gateway_rssi[gateway_index] += int(data['rx_rssi'])
            for idx, item in enumerate(gateway_count):
                if item != 0:
                    gateway_tuple = gateway_locations[idx]
                    testpoint_tuple = testpoint_locations[testpoint_location_index]
                    d = get_distance(gateway_tuple, testpoint_tuple)
                    rssi = round(gateway_rssi[idx] / item, 2)

                    print('power_sf={:2}_{:2}, x={:6.2f}, y={:6.2f}'.format(i, j, d, rssi))
                    result_dict['{}_{}'.format(i, j)].append([d, rssi])
            print('---')
            # exit(0) # breakpoint

def draw_line_chart():
    for i in range(1, 21):
        for j in range(7, 11):
            dict_index = '{}_{}'.format(i, j)
            coordinates = result_dict[dict_index]
            x_axis_list, y_axis_list = zip(*coordinates)
            
            plt.plot(x_axis_list, y_axis_list, label=dict_index)

    plt.title('testData.zip, 共20(power)*4(sf)條線.\n折線圖.')
    plt.xlabel('距離')
    plt.ylabel('RSSI')
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False
    plt.show()

def draw_lstsq():
    for i in range(1, 21):
        for j in range(7, 11):
            dict_index = '{}_{}'.format(i, j)
            coordinates = result_dict[dict_index]
            x_axis_list, y_axis_list = zip(*coordinates)

            # Least squares
            x = np.array(x_axis_list)
            y = np.array(y_axis_list)
            A = np.vstack([x, np.ones(len(x))]).T
            m, c = np.linalg.lstsq(A, y, rcond=None)[0]
            plt.plot(x, m*x + c, label=dict_index)
            # plt.plot(x, y, 'o', markersize=2) # scatter

    plt.title('testData.zip, 共20(power)*4(sf)條線.\n使用least-squares(最小平方法)在每個power_sf的一堆點對中, 繪出最適直線.')
    plt.xlabel('距離')
    plt.ylabel('RSSI')
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False
    plt.show()

def main():
    for testpoint_location_index in range(len(testpoint_locations)): # start from 0
        if testpoint_locations[testpoint_location_index] is None:
            print('Bypass location {} because of incompleteness.'.format(testpoint_location_index + 1))
            continue

        relative_path = 'testData/{}/'.format(testpoint_location_index + 1)
        random_file_name = listdir(path.join(base_dir, relative_path))[0]

        student_id = random_file_name.split('_')[0]
        device_EUI = random_file_name.split('_')[1]

        single_location_data(relative_path, student_id, device_EUI, testpoint_location_index)

if __name__ == '__main__':
    main()
    draw_line_chart()
    draw_lstsq()

"""
TEST
"""
# print('Testing get_distance():', get_distance((21.0122287, 52.2296756), (16.9251681, 52.406374)), ', it should be 278546m.')
# print('Testing get_which_gateway():', get_which_gateway('00800000a00006d4'), ', it should be 0.')

# single_location_data('testData/1/', '106522097', '008000000000e332', 0)
# draw_line_chart()
# draw_lstsq()