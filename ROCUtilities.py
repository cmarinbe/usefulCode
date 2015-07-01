#!/usr/bin/env python
#============================================================================
# @file   RootUtilities.py
# @author Carla Marin (cmarin@ecm.ub.edu)
# @date   19.06.2014
#=============================================================================
"""Define some nice functions to complement ROOT built-ins"""

import ROOT

def findPointY(roocurve, yvalue, tolerance = 1e-10):
    x, y = ROOT.Double(0), ROOT.Double(0)
    delta = tolerance
    n = roocurve.GetN()
    ibest = -1
    for i in range(1, n-1):
        roocurve.GetPoint(i,x,y)
        if (abs(yvalue-y)<delta):
            delta = abs(yvalue-y)
            ibest = i
    roocurve.GetPoint(ibest, x, y)
    return ibest, x, y
