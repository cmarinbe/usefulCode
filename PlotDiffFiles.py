#!/usr/bin/env python
# ===============================================================
# @file   PlotDiffFiles.py
# @author Carla Marin (carla.marin.benito@cern.ch)
# @date   24.05.2015
# ===============================================================
"""Script for ploting variables from diferents files (and trees)
in the same canvas"""

import os
from argparse import ArgumentParser

import ROOT
from functions_Dataset import read_trees

def fill_histos(labels, trees, variables, cuts="", bins=50):
    from ROOT import TH1F
    histos= {}
    for l,t in zip(labels, trees):
        num=0
        histos[l] = []
        for var, limits in variables.items():
            histos[l].append(TH1F("h%s_%s" %(num,l), "", bins, limits[0], limits[1]))
            t.Draw("%s>>h%s_%s" %(var,num,l), cuts, "same")
            num += 1
    print "####### Histos filled"
    return histos

def add_legend(labels, graphics, xi = 0.7, yi = 0.55, xf = 0.99, yf = 0.85):
    from ROOT import TLegend
    leg = TLegend(xi, yi, xf, yf)
    for l in labels:
        leg.AddEntry(graphics[l][0],l,"l")
    return leg

def scale_histo(histo, norm = 1.):
    """
    Scales an histogram to a given normalization using histo.Scale(norm/entries).
    If histo has no entries, scales it to 0 to avoid error.
    Returns new maximum value in histo
    histo: TH1, histo to be normalized
    norm: float, normalization value. Default in 1.
    """
    lEntries = histo.GetEntries()
    if lEntries==0: histo.Scale(0)
    else: histo.Scale(norm/lEntries)
    maxValue_l = histo.GetMaximum()
    return maxValue_l

def draw_histo(histo, maxValue, titleX, lineColor, titleOffset = 1.5):
    """
    Draw given histogram setting the max value of y axis, x and y axis titles
    and offsets and histo line color.
    histo: TH1, histo to be drawn
    maxValue: float, value to be used to set y axis maximum as 1.1*maxValue
    titleX: str, title to be set for the x axis
    lineColor: int, corresponding to the line color for the histo to be drawn
    titleOffset: float, mm of the title to be offset from the axis. Default is 1.5
    """
    histo.SetMaximum(1.1*maxValue)
    histo.GetXaxis().SetTitle(titleX)
    len_bin = (histo.GetXaxis().GetXmax() - histo.GetXaxis().GetXmin())/histo.GetNbinsX()
    histo.GetYaxis().SetTitle("Entries/%s" %len_bin)
    histo.GetYaxis().SetTitleOffset(titleOffset)
    histo.GetXaxis().SetTitleOffset(titleOffset)
    histo.SetLineColor(lineColor)
    histo.Draw("same")

def plot_vars(path_plots, variables, histos, optName="", leg=None, scale=True, canvas_x = 700, canvas_y = 700):
    """
    Plot all the variables given for all the labels, one plot per variable.
    Already filled histos (one per variable and per label) are used.
    variables: dict, keys are the variable names, entries are lists including
    x limits to be used when drawing and x axis title to be set.
    histos: dict, keys are the names in the legend, entries are lists with
    the histos for each variable.
    canvas_x: int, x size of the canvas to be ploted. Default is 700
    canvas_y: int, y size of the canvas to be ploted. Default is 700
    leg: TLegend, if exists it is drawn for each variable. Default is None
    """
    from ROOT import gStyle
    from ROOT import TCanvas
    print "####### Start drawing"
    gStyle.SetOptStat(0)
    canvas= []
    for i in xrange(len(variables.keys())):
        lineColor = 1
        varName = variables.keys()[i]
        canvas.append(TCanvas('c_%s' %varName, 'c_%s' %varName, canvas_x, canvas_y))
        #maxValue = 3000.
        maxValue = 0.
        for l in histos.keys():
            if scale: maxValue_l = scale_histo(histos[l][i])
            else: maxValue_l = histos[l][i].GetMaximum()
            if maxValue_l>maxValue: maxValue = maxValue_l
        for l in histos.keys():
            draw_histo(histos[l][i], maxValue, variables[varName][2], lineColor)
            lineColor=lineColor+1
        if leg: leg.Draw("same")
        canvas[i].SaveAs(path_plots+"/%s%s.root" % (varName,optName))
        canvas[i].SaveAs(path_plots+"/%s%s.png" % (varName,optName))
    print "####### Histos drawn and saved"


if __name__=="__main__":
    parser = ArgumentParser()
    parser.add_argument('tuplepath', action='store', type=str, help='Path for ntuples')
    parser.add_argument('fileslist', action='store', type=str, help='List with the files to be drawn')
    parser.add_argument('labellist', action='store', type=sts, help='List with the label of each file to be written int he plots')
    parser.add_argument('varslist' , action='store', type=str, help='List with the variables to be drawn')
    parser.add_argument('plotspath', action='store', type=str, help='Path for plots')
    parser.add_argument('--tNames', default = ''   , action='store', type=str, help='List with the names of the trees in the files')
    parser.add_argument('--scale' , default ='True', action='store', type=str, help='Normalize or not')
    parser.add_argument('--cuts'  , default = ''   , action='store', type=str, help='Cuts to be applied')
    args = parser.parse_args()
    # Build paths
    path_base  = os.path.abspath(args.tuplepath)
    file_names = (args.fileslist).split(",")
    labels     = (args.labellist).split(",")
    list_vars  = (args.varslist).split(",")
    path_plots = os.path.abspath(args.plotspath)
    tree_names = args.tNames if tNames!="" else ["DecayTree" for fN in file_names]
    scale = True if args.scale=='True' else False
    cuts  = args.cuts
    if not os.path.isdir(path_base):
        raise OSError("Cannot find tuple path -> %s" % path_base)
    if not os.path.isdir(path_plots):
        os.mkdir(path_plots)

    # Define files
    file_names = [os.path.join(path_base, fN) for fN in file_names]
    # open files
    files, trees = read_trees(file_names, tree_names)
    # fill histos
    histos = fill_histos(labels, trees, variables, cuts)
    # create legend
    leg = add_legend(labels, histos)
    # plot histos in the desired style
    plot_vars(path_plots, variables, histos, "", leg, scale)

    print "All variables have been plotted."

#EOF
