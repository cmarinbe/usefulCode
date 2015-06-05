vars
import os
import argparse

import ROOT
from ROOT import TCanvas, TH1F, TFile, TTree, TLegend
from ROOT import gBenchmark, gStyle, gROOT

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--files" , default = "", action = "store", type = str, help = "ROOT files to be read")
parser.add_argument("-t", "--trees" , default = "", action = "store", type = str, help = "Tree names")
parser.add_argument("-l", "--labels", default = "", action = "store", type = str, help = "Labels for the files")
parser.add_argument("-c", "--cuts"  , default = "", action = "store", type = str, help = "Cuts to apply before drawing")
parser.add_argument("-p", "--path"  , default = "", action = "store", type = str, help = "Folder where the histos will be saved")

args = parser.parse_args()
fileNames = args.files
treeNames = args.trees
labels = args.labels
cuts  = args.cuts
path  = args.path

# Connect ROOT histogram/ntuple.
if fileNames.startswith("["):
    if not fileNames.endswith("]"):
        parser.error("Invalid input string %s" % fileNames)
    fileNames = fileNames[1:-1].split(",")
elif fileNames.startswith("("):
    if not fileNames.endswith(")"):
        parser.error("Invalid input string %s" % fileNames)
    fileNames = fileNames[1:-1].split(",")
else:
    fileNames = [fileNames]

if treeNames=="": treeNames=["DecayTree" for i in range(len(fileNames))]
elif treeNames.startswith("["):
    if not treeNames.endswith("]"):
        parser.error("Invalid input string %s" % treeNames)
    treeNames = treeNames[1:-1].split(",")
elif treeNames.startswith("("):
    if not treeNames.endswith(")"):
        parser.error("Invalid input string %s" % treeNames)
    treeNames = treeNames[1:-1].split(",")
else:
    treeNames = [treeNames]

if labels.startswith("["):
    if not labels.endswith("]"):
        parser.error("Invalid input string %s" % labels)
    labels = labels[1:-1].split(",")
elif labels.startswith("("):
    if not labels.endswith(")"):
        parser.error("Invalid input string %s" % labels)
    labels = labels[1:-1].split(",")
else:
    labels = [labels]

files = []
trees = []
histos= {}
i=0
for fN, tN in zip(fileNames, treeNames):
    files.append(TFile(fN))
    trees.append(files[i].Get(tN))
    i=i+1

variables = {
    'nbody_pt':                                 [0,20000,       "n body PT [MeV/c^{2}]"                 ],
    'nbody_p':                                  [0,200000,      "n body P [MeV/c^{2}]"                  ],
    'nbody_vertex_chi2':                        [0,6,           "n body vtx #chi^{2}"                   ],
    'nbody_fd':                                 [0,100,         "n body FD [mm]"                        ],
    'nbody_fdchi2':                             [0,1000,        "n body FD #chi^{2}"                    ],
    'nbody_fd_rho':                             [0,5,           "n body FD rho"                         ], #what is this??
    'nbody_fd_over_p':                          [0,0.0005,      "n body FD/p [mm/(MeV/c^{2})]"          ],
    'nbody_children_pt_sum':                    [0,30000,       "n body children sum PT [MeV/c^{2}]"    ],
    'nbody_children_pt_max':                    [0,20000,       "n body children max PT [MeV/c^{2}]"    ],
    'nbody_children_pt_min':                    [0,10000,       "n body children min PT [MeV/c^{2}]"    ],
    'nbody_children_chi2ndof_max':              [0,3,           "n body children max #chi^{2}/ndf"      ],
    'nbody_children_chi2ndof_min':              [0,3,           "n body children min #chi^{2}/ndf"      ],
    'nbody_children_ipchi2_sum':                [0,10000,       "n body children sum IP #chi^{2}"       ],
    'nbody_children_ipchi2_max':                [0,10000,       "n body children max IP #chi^{2}"       ],
    'nbody_children_ipchi2_min':                [0,2500,        "n body children sum IP #chi^{2}"       ],
    'nbody_doca_max':                           [0,0.2,         "n body max doca [mm]"                  ],
    'nbody_doca_min':                           [0,0.2,         "n body min doca [mm]"                  ],
#'nbody_children_charge_sum':                [-1,1,          "n body children sum charge"            ],
    'nbody_m':                                  [0,5000,        "n body mass [MeV/c^{2}]"               ],
    'nbody_am':                                 [0,5000,        "n body a mass [MeV/c^{2}]"             ], # diferencia amb m?
    'nbody_m_corrected':                        [0,10000,       "n body corr mass [MeV/c^{2}]"          ], # que corregeix?
    'nbody_children_num_ipchi2_under_sixteen':  [0, 3,          "n children with IP chi2 < 16"          ],
    'gamma_pt':                                 [0,15000,       "#gamma PT"                             ],
    'gamma_p':                                  [0,300000,      "#gamma P"                              ],
    'sv_children_pt_sum':                       [0,30000,       "SV children sum PT [MeV/c^{2}]"        ],
    'sv_children_pt_max':                       [0,20000,       "SV children max PT [MeV/c^{2}]"        ],
    'sv_children_pt_min':                       [0,8000,        "SV children min PT [MeV/c^{2}]"        ],
    'sv_pt':                                    [0,30000,       "SV PT [MeV/c^{2}]"                     ],
    'sv_p':                                     [20000,400000,  "SV P [MeV/c^{2}]"                      ],
    'sv_fd_over_p':                             [0,0.0001,      "SV FD/p [mm/(MeV/c^{2})]"              ],
    'sv_eta':                                   [-5,7,          "SV eta"                                ],
    'sv_m':                                     [2000,7000,     "SV mass [MeV/c^{2}]"                   ],
    'sv_am':                                    [0,8000,        "SV a mass [MeV/c^{2}]"                 ],
    'sv_m_corrected':                           [2000,11000,    "SV corr mass [MeV/c^{2}]"              ],
    'trigger_l0_electron_tos':                  [0,2,           "L0_Electron_TOS"                       ],
    'trigger_l0_photon_tos':                    [0,2,           "L0_Photon_TOS"                         ],
    'trigger_1track_tos':                       [0,2,           "Hlt1_1track_TOS"                       ],
    'trigger_1track_dec':                       [0,2,           "Hlt1_1track_dec"                       ],
    'trigger_2track_tos':                       [0,2,           "Hlt1_2track_TOS"                       ],
    'trigger_2track_dec':                       [0,2,           "Hlt1_2track_dec"                       ],
    'track1_chi2ndof':                          [0,3,           "tr 1 #chi^{2}/ndf"                     ],
    'track1_pt':                                [0,10000,       "tr 1 PT [MeV/c^{2}]"                   ],
    'track1_p':                                 [0,200000,      "tr 1 P [MeV/c^{2}]"                    ],
    'track1_ip':                                [0,3,           "tr 1 IP"                               ],
    'track1_ipchi2':                            [0,3000,        "tr 1 IP #chi^{2}"                      ],
    'track1_eta':                               [1.5,5.5,       "tr 1 eta"                              ],
#'track1_charge':                            [-1,1,          "tr 1 charge"                           ],
    'track2_chi2ndof':                          [0,3,           "tr 2 #chi^{2}/ndf"                     ],
    'track2_pt':                                [0,10000,       "tr 2 PT [MeV/c^{2}]"                   ],
    'track2_p':                                 [0,200000,      "tr 2 P [MeV/c^{2}]"                    ],
    'track2_ip':                                [0,3,           "tr 2 IP"                               ],
    'track2_ipchi2':                            [0,3000,        "tr 2 IP #chi^{2}"                      ],
    'track2_eta':                               [1.5,5.5,       "tr 2 eta"                              ],
#'track2_charge':                            [-1,1,          "tr 2 charge"                           ]
}

for l,t in zip(labels,trees):
    num=0
    histos[l] = []
    for var, limits in variables.items():
        histos[l].append(TH1F("h%s_%s" %(num,l), "h%s_%s" %(num,l), 50, limits[0], limits[1]))
        t.Draw("%s>>h%s_%s" %(var,num,l), cuts, "same")
        num=num+1

print "####### Histos filled"
print "####### Start drawing"

leg = TLegend(0.7,0.55,0.9,0.75)
leg.SetHeader("Legend")
for l in labels:
    leg.AddEntry(histos[l][0],l,"l")

# check path where to save histos exists or create it
if not os.path.isdir(path):
    os.mkdir(path)

canvas= []
for i in xrange(len(variables.keys())):
    lineColor = 1
    canvas.append(TCanvas('c_%s' %variables.keys()[i], 'c_%s' %variables.keys()[i], 700, 700))
    maxValue = 0
    for l in labels:
        lEntries = histos[l][i].GetEntries()
        if lEntries==0: histos[l][i].Scale(0)
        else: histos[l][i].Scale(1./lEntries)
        maxValue_l = histos[l][i].GetMaximum()
        if maxValue_l>maxValue: maxValue = maxValue_l
    for l in labels:
        histos[l][i].SetMaximum(maxValue+0.1*maxValue)
        histos[l][i].GetXaxis().SetTitle(variables[variables.keys()[i]][2])
        histos[l][i].GetYaxis().SetTitle("Entries/%s" %((histos[l][i].GetXaxis().GetXmax() - histos[l][i].GetXaxis().GetXmin())/histos[l][i].GetNbinsX()) )
        histos[l][i].GetYaxis().SetTitleOffset(1.5)
        histos[l][i].SetLineColor(lineColor)
        histos[l][i].Draw("same")
        lineColor=lineColor+1
    leg.Draw()
    if variables.keys()[i]=="B_FDCHI2_OWNPV_smeared_shifted": canvas[i].SetLogy()
    canvas[i].SaveAs(path+"/%s.root" % variables.keys()[i])
    canvas[i].SaveAs(path+"/%s.png" % variables.keys()[i])

print "####### Histos drawn and saved"

#EOF

