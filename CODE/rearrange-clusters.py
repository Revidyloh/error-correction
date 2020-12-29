#!/usr/bin/env python3

import pandas as pd
import numpy as np


def pyth(x, y):
    return (x**2 + y**2)**(1/2)

def shortest(x, y, row):
    x = float(x)
    y = float(y)
    dx_min = 1000
    dy_min = 1000
    nx = 0
    ny = 0
    print("ARHG",row["0 (x,y)"].split(' ')[0])
    for column in row[1:]:
        if str(column) != 'nan':
            xc = float(str(column).split(' ')[0])
            yc = float(str(column).split(' ')[1])
            if abs(x-xc) < dx_min:
                dx_min = abs(x-xc)
                nx  = xc
            if abs(y-yc) < dy_min:
                dy_min = abs(y-yc)
                ny = yc


    print("Shortest x:", nx)
    print("Shortest y:", ny)

    return [nx, ny]

def shortest2(x, y, row):
    x = float(x)
    y = float(y)
    dx_min = 1000
    dy_min = 1000
    nx = 0
    ny = 0
    print("ARHG",row["0 (x,y)"].split(' ')[0])
    for column in row[1:]:
        if str(column) != 'nan':
            xc = float(str(column).split(' ')[0])
            yc = float(str(column).split(' ')[1])
            if abs(x-xc) < dx_min:
                dx_min = abs(x-xc)
                nx  = xc
                ny = yc


    print("Shortest x:", nx)
    print("Shortest y:", ny)

    return [nx, ny]

def shortest3(x, y, row):
    x = float(x)
    y = float(y)
    dx_min = 1000
    dy_min = 1000
    nx = 0
    ny = 0
    print("ARHG",row["0 (x,y)"].split(' ')[0])
    for column in row[1:]:
        if str(column) != 'nan':
            xc = float(str(column).split(' ')[0])
            yc = float(str(column).split(' ')[1])
            if abs(y-yc) < dx_min:
                dy_min = abs(y-yc)
                nx  = xc
                ny = yc


    print("Shortest x:", nx)
    print("Shortest y:", ny)

    return [nx, ny]

def shortest5(x, y, row):
    x = float(x)
    y = float(y)
    dmin = 1000
    d = pyth(x, y)
    nx = 0
    ny = 0
    print("ARHG",row["0 (x,y)"].split(' ')[0])
    for column in row[1:]:
        if str(column) != 'nan':
            xc = float(str(column).split(' ')[0])
            yc = float(str(column).split(' ')[1])
            dc = pyth(xc, yc)
            if d-dc < dmin:
                dmin = d-dc
                nx = xc
                ny = yc


    print("Shortest x:", nx)
    print("Shortest y:", ny)

    return [nx, ny]

def main():
    legs = pd.read_csv("legs.csv")

    clusters_distance=[]
    # first index is cluster col, second is value
    # ex: clusters_distance[0][0] is the distance from the robot for the first
    # (x, y) of the first cluster
    for i in range(7):
        temp = []
        for cluster in legs["{} (x,y)".format(i)]:
            if pd.isna(cluster):
                temp.append(np.nan)
            else:
                xy = cluster.split(' '); x = xy[0]; y = xy[1]
                d = pyth(float(x), float(y))
                temp.append(d)
        clusters_distance.append(temp)

    ##########################################################################
    # naive reorganization
    prev_r = []
    curr_r = []
    for i, row in legs.iterrows():
        if i==0:
            prev_r = row
            x0p = prev_r["0 (x,y)"].split(' ')[0]
            y0p = prev_r["0 (x,y)"].split(' ')[1]
        if i>0 and i<5:
            # x0p = prev_r["0 (x,y)"].split(' ')[0]
            # y0p = prev_r["0 (x,y)"].split(' ')[1]
            # print(row)
            new_coord = shortest5(x0p, y0p, row)
            new_input = str(new_coord[0]) + ' ' + str(new_coord[1])
            legs.iloc[i, 1] = new_input
            x0p = new_coord[0]
            y0p = new_coord[1]

            # prev_r = row
            # prev_r = pd.read_csv("legs.csv", skiprows=i-1, nrows=1)
    legs.to_csv("legs5.csv")











if __name__=="__main__":
    main()
