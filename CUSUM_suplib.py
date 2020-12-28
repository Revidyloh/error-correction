#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, pi, exp

# Means
###############################################################################
def FirstNMean(data, n):
    # Error checking
    if n<0:
        n=0
    if n>len(data):
        n=len(data)
    if n==0 or len(data)==0:
        return 0

    sum = 0.0
    for x in data[:n]:
        sum += x
    return sum/n

def FirstNPercent(data, n):
    # Error checking
    if n>100:
        n=100
    if n<0:
        n=0
    n = int(len(data) * n/100)
    if n==0 or len(data)==0:
        return 0
    return FirstNMean(data, n)

def TopNPercent(data, n):
    if n>100:
        n=100
    if n<0:
        n=0
    if n==0 or len(data)==0:
        return 0
    p = int(len(data) * n/100)
    if p==0:
        p=1
    sum = 0.0
    for x in sorted(data)[-p:]:
        sum += x
    return sum/p

def BotNPercent(data, n):
    if n>100:
        n=100
    if n<0:
        n=0
    if n==0 or len(data)==0:
        return 0
    p = int(len(data) * n/100)
    if p==0:
        p=1
    sum = 0.0
    for x in sorted(data)[:p]:
        sum += x
    return sum/p

def GaussianSimple(xt, mu, sigma):
    sigma_sqrd = sigma * sigma
    gaussian = np.longdouble((1.0/(sigma * sqrt(2.0*pi))) * exp(-(xt - mu)*(xt - mu) / (2.0*sigma_sqrd)))
    return gaussian

# The mean is the same for the null and alt hypothesis
# sigma_alt is sigma_base + something
def LogLikelihoodRatio(xt, mu, sigma_base, sigma_alt):
    L = GaussianSimple(xt, mu, sigma_alt) / GaussianSimple(xt, mu, sigma_base)
    return log(L)
###############################################################################
# /Means

# Data manip
###############################################################################
def RemoveSpikes(data, spike_threshold):
    data_wo_spikes = data.copy()
    iteration = 0
    for spike in data_wo_spikes:
        if spike < spike_threshold:
            data_wo_spikes.remove(spike)
            print("Data point:", iteration)
        iteration += 1
    mean = np.mean(data_wo_spikes)

    data_wo_spikes = data.copy()
    for i in range(len(data_wo_spikes)):
        if data_wo_spikes[i] < spike_threshold:
            data_wo_spikes[i] = mean
    return data_wo_spikes

def NormalizeMeanTo0(data):
    normalized = data.copy()
    mean = np.mean(normalized)
    for i in range(len(normalized)):
        normalized[i] = normalized[i] - mean
    return normalized

def MultiplyData(data, n):
    new_data = []
    for each in data:
        new_data.append(each*n)
    return new_data
###############################################################################
# /Data manip


# Debugging functions - TO BE REMOVED -
def test():
    myl0 = [9,8,7,6,5,4,3,2,1,0]
    myl1 = [1,3,5,7,9,2,4,6,8,0]
    #
    # norm = NormalizeMeanTo0(myl0)
    #
    # print(norm, np.mean(norm))

    myl2 = MultiplyData(myl0, 2)
    print (myl2)
    print (myl0)


def main():
    test()

if __name__ == "__main__":
    main()
