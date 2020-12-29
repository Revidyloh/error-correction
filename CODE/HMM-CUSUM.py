#!/usr/bin/env python3

# Gwenaël Gatto
# CUSUM and CUSUM-like module

# This module contains a basic CUSUM implementation
# A CUSUM object can be created that takes in:
# a mean, change to be detected, threshold to raise alarm, and
# optionally a CUSUM value (default to 0 otherwise)

# CUSUM2 allows for an update of the mean after an alarm is raised

# CUSUM3 allows for spike detection using HMM

# d0 = e0 = 0
# d1, d2, ... and e1, e2, ... are calculated recursively
# dl = max[0, dl-1 + (xbar - (mu0 + k))]    upper limit
# el = max[0, el-1 - (xbar - (mu0 - k))]    lower limit
# k = delta/2, where delta is the change to be detected
# alarm is raised if at time r, dr > h or er > h
# dr > h means process has shifted to greater value
# er > h means process has shifted to lower value

import pandas as pd
import numpy as np
import CUSUM_suplib as csl
from math import log
import sys

class CUSUM(object):

    def __init__(self, mean, delta, h, dlcusum=0, elcusum=0):
        # from arguments
        self.mean = mean
        self.delta = delta
        self.h = h
        self.dlcusum = dlcusum
        self.elcusum = elcusum

        # derived
        self.k = delta/2
        self.dlvariance = self.mean + self.k
        self.elvariance = self.mean - self.k

        self.dlalarm = False
        self.elalarm = False

    # Core methods
    def Update(self, xbar):
        # CUSUM values
        self.dlcusum = max(0, self.dlcusum + (xbar - self.dlvariance))
        self.elcusum = max(0, self.elcusum - (xbar - self.elvariance))

        # Alarm state
        if self.h < self.dlcusum:
            self.dlalarm = True
        else:
            self.dlalarm = False
        if self.h < self.elcusum:
            self.elalarm = True
        else:
            self.elalarm = False


    def WhichAlarm(self):
        if self.dlalarm:
            return 1
        else:
            return 0

    def Alarm(self):
        return self.dlalarm or self.elalarm


    # Utility methods
    def Print(self, todo=None):
        if todo!=None:
            print("CUSUM+: ", self.dlcusum)
            print("CUSUM-: ", self.elcusum)
            print("Mean: ", self.mean)
            print("Delta: ", self.delta)
            print("Threshold: ", self.h)
        else:
            print("CUSUM +/-: ", self.dlcusum, "/", self.elcusum)

    def __str__(self):
        return ("+CUSUM: " + str(self.dlcusum) + \
                "\n-CUSUM: " + str(self.elcusum))

    # Accessors/Mutators
    def GetUpperCusum(self):
        return self.dlcusum

    def GetLowerCusum(self):
        return self.elcusum

###############################################################################
# CUSUM class that resets its mean on alarm
# New mean is m0+k or m0-k depending which alarm has been raised
###############################################################################
class CUSUM2(CUSUM):
    def __init__(self, mean, delta, h, dlcusum=0, elcusum=0):
        CUSUM.__init__(self, mean, delta, h, dlcusum, elcusum)


    def Update2(self, xbar):
        CUSUM.Update(self, xbar)
        if CUSUM.Alarm(self):
            print("Alarm Raised")
            self.Reinitialize(CUSUM.WhichAlarm(self))
            print("New mean: ", self.mean)



    def Reinitialize(self, alarm):
        if alarm:
            self.mean = self.dlvariance
        else:
            self.mean = self.elvariance

        self.dlcusum = 0
        self.elcusum = 0

        # derived
        self.dlvariance = self.mean + self.k
        self.elvariance = self.mean - self.k

        self.dlalarm = False
        self.elalarm = False

###############################################################################
# CUSUM-like using HMM
###############################################################################
class CUSUM3(CUSUM2):
    def __init__(self, mean, delta, h, dlcusum=0, elcusum=0):
        CUSUM2.__init__(self, mean, delta, h, dlcusum, elcusum)

        # Initial probability distribution
        self.ps = [1, 0, 0.5, 0.5]

        # Transition matrix under Hk
        self.tmatrix = [1, 0, 0.5, 0.5]

        self.high_var = False
        self.passed_h = False
        self.passed_0 = False
        self.low_h = h


    def InitializeForwardVars(self, xt, mean, sigma_low, sigma_high):
        self.apH0 = self.ps[0] * csl.GaussianSimple(xt, mean, sigma_low)
        self.apH1 = self.ps[1] * csl.GaussianSimple(xt, mean, sigma_high)
        self.apK0 = self.ps[2] * csl.GaussianSimple(xt, mean, sigma_low)
        self.apK1 = self.ps[3] * csl.GaussianSimple(xt, mean, sigma_high)

    def Print3(self):
        print("apH0:", self.apH0)
        print("apH1:", self.apH1)
        print("apK0:", self.apK0)
        print("apK1:", self.apK1)

    def UpdateForwardVars(self, xt, mean, sigma_low, sigma_high):
        denomH = self.apH0 + self.apH1
        denomK = self.apK0 + self.apK1
        self.apH0 = csl.GaussianSimple(xt, mean, sigma_low)
        if self.apH0 == 0:
            self.apH0 = sys.float_info.min
        if denomH == 0:
            denomH = sys.float_info.min
        if denomK == 0:
            denomK = sys.float_info.min

        self.apH1 *= csl.GaussianSimple(xt, mean, sigma_high) / denomH
        self.apK0 = (self.apK0*self.tmatrix[0] + self.apK1*self.tmatrix[1])*csl.GaussianSimple(xt, mean, sigma_low) / denomK
        self.apK1 = (self.apK0*self.tmatrix[2] + self.apK1*self.tmatrix[3])*csl.GaussianSimple(xt, mean, sigma_high) / denomK


    def InitializeLLR(self):
        self.llr = 0.0
        self.llrr = 0.0

    def UpdateLLR(self):
        self.llr += log( (self.apK0 + self.apK1) / (self.apH0 + self.apH1) )
        self.llrr +=log( (self.apH0 + self.apH1) / (self.apK0 + self.apK1) )

    def GetAps(self):
        ap = [self.apH0, self.apH1, self.apK0, self.apK1]
        return ap

    def GetLLR(self):
        return self.llr

    def GetLLRR(self):
        return self.llrr

    def Update3(self, xt, mean, sigma_low, sigma_high):
        if self.passed_h == False:
            self.UpdateForwardVars(xt, mean, sigma_low, sigma_high)
            self.UpdateLLR()

        if self.passed_0:
            self.InitializeForwardVars(xt, mean, sigma_low, sigma_high)
            self.passed_0 = False

        if self.passed_h:
            self.InitializeForwardVars(xt, mean, sigma_low, sigma_high)
            self.InitializeLLR()
            self.passed_h = False

        if self.llr > self.h:
            print("PASSED THRESHOLD")
            self.passed_h = True
            return True

        elif self.llr < 0:
            self.passed_0 = True
            self.llr = 0
        #########################################
        if self.llrr < 0:
            self.llrr = 0




def main():
    pass

if __name__ == "__main__":
    main()





###############################################################################
