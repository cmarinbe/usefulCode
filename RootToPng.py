#!/usr/bin/env python
#============================================================================
# @file   RootToPng.py
# @author Carla Marin (cmarin@ecm.ub.edu)
# @date   20.06.2014
#=============================================================================
"""Script to save the content off all .root files in a folder as .png"""

import os
import argparse
import ROOT


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder", default="", action="store", type=str)
    parser.add_argument("-s", "--files", default = "", action = "store", type = str)
    args   = parser.parse_args()
    folder = args.folder
    files  = args.files
    # read files
    if (files == ""):
        fileList = os.listdir(folder)
    elif (files.startswith("[")):
        if not (files.endswith("]")):
            parser.error("Invalid input string %s" % files)
        fileList = files[1:-1].split(",")
    elif (files.startswith("(")):
        if not files.endswith(")"):
            parser.error("Invalid input string %s" % files)
        fileList = files[1:-1].split(",")
    else:
        fileList = [files]
    # run
    savedFiles = 0
    for file in fileList:
        if (file[-5:]== ".root"):
            f = ROOT.TFile(folder+"/"+file)
            keys = f.GetListOfKeys()
            for k in keys:
                plot = k.ReadObj()
                name = k.GetName()+".png"
                plot.SaveAs(path+"/"+name)
                savedFiles += 1
    print "%s plots saved to .png" % savedFiles


# EOF
