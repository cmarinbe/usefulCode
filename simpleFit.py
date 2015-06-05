##########################################
#
# author: C. Marin Benito
# date  : 22.12.2014
# docu  : This script fits a simple pdf to
# a given dataset using RooFit.
#
##########################################

import os
import ROOT
import PyLHCb.Root.RooFitDecorators
from PyLHCb.Root.RooFitUtils import ResidualPlot

#from PyLHCb.Root.RootUtils import load_library
#from PyLHCb.Root.RootUtils import get_RooDataSet

#load_library("BifurcatedCB")

RooFit         = ROOT.RooFit
RooRealVar     = ROOT.RooRealVar
RooArgList     = ROOT.RooArgList
RooArgSet      = ROOT.RooArgSet
RooDataSet     = ROOT.RooDataSet
RooGaussian    = ROOT.RooGaussian
RooExponential = ROOT.RooExponential
RooAddPdf      = ROOT.RooAddPdf

def simpleFit(tree, cuts, mean, xmin = 4000, xmax = 7000):
    # define pdf
    B_MM = RooRealVar("B_MM","B_MM", xmin, xmax)
    
    mean  = RooRealVar("mean", "mean",  mean, mean-50, mean+50)
    sigma = RooRealVar("sigma", "sigma", 80, 10, 150)
    gauss = RooGaussian("gauss", "gauss", B_MM, mean, sigma)
    
    tau = RooRealVar("tau", "tau", -0.005, -0.01, 0.)
    exp = RooExponential("exp", "exp", B_MM, tau)
    
    nsig = RooRealVar("nsig", "nsig", 1000, 0, 20000)
    nbkg = RooRealVar("nbkg", "nbkg", 1000, 0, 20000)
    
    suma = RooArgList()
    coeff = RooArgList()
    
    suma.add(gauss)
    suma.add(exp)
    
    coeff.add(nsig)
    coeff.add(nbkg)
    
    model = ROOT.RooAddPdf("model", "model", suma, coeff)
    
    # define dataset
    if (cuts!=""): tree = tree.CopyTree(cuts)
    nentries = tree.GetEntries()
    
    ds = RooDataSet("data", "dataset with x", tree, RooArgSet(B_MM))
    
    # plot dataset and fit
    massFrame = B_MM.frame()
    ds.plotOn(massFrame, Name="histo_data")
    
    fitResults = model.fitTo(ds)
    model.plotOn(massFrame, RooFit.VisualizeError(fitResults, 1), RooFit.Name("curve_model"))
    model.plotOn(massFrame, RooFit.Components("gauss"), RooFit.LineColor(2), RooFit.VisualizeError(fitResults, 1))
    model.plotOn(massFrame, RooFit.Components("exp")  , RooFit.LineColor(3), RooFit.VisualizeError(fitResults, 1))
    model.paramOn(massFrame, Layout = (.55,.95,.93), Parameters = RooArgSet(nsig, nbkg, mean, sigma, tau))
    Plot = ResidualPlot("chi2plot", massFrame)
    chi2 = Plot.addResidual("histo_data", "curve_model")
    Plot.plot(bigLabels=True, residualBand=True)
    
    print "%s has been fit to %s with a chi2 = %s." % (model.GetName(), tree.GetName(), chi2)
    print "Total number of entries is: %s" % nentries
    print "Number of sig entries is: %s +- %s" % (nsig.getValV(), nsig.getError())
    print "Number of bkg entries is: %s +- %s" % (nbkg.getValV(), nbkg.getError())
    print "S/B is: %s +- %s" % (nsig.getValV()/nbkg.getValV(), ( (nsig.getError()/nbkg.getValV())**2 + (nsig.getValV()*nbkg.getError()/nbkg.getValV()**2)**2 )**0.5 )
    
    return model, Plot, chi2


if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default = ""         , action = "store", type = str)
    parser.add_argument("-m", "--mean", default = ""         , action = "store", type = str)
    parser.add_argument("-c", "--cuts", default = ""         , action = "store", type = str)
    parser.add_argument("-n", "--xmin", default = "4000"     , action = "store", type = str)
    parser.add_argument("-x", "--xmax", default = "7000"     , action = "store", type = str)
    parser.add_argument("-t", "--tree", default = "DecayTree", action = "store", type = str)

    args = parser.parse_args()
    fileName = args.file
    mean     = float(args.mean)
    cuts     = args.cuts
    xmin     = float(args.xmin)
    xmax     = float(args.xmax)
    treeName = args.tree

    # read data
    file = ROOT.TFile(fileName)
    tree = file.Get(treeName)

    model, Plot, chi2 = simpleFit(tree, cuts, mean, xmin, xmax)


#EOF
