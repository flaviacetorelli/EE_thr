#!/usr/bin/env python3
import sys
import os
import csv
from array import array

import argparse 

import ROOT as R
R.gROOT.SetBatch(True) 



##Code to test effect of different thresholds on K
##with NOISE
#parser = argparse.ArgumentParser()
#parser.add_argument('--debug',           action='store_true',           default=False,      help='debugging mode')
#parser.add_argument("-r", "--rms",     action="store",      type=float,       default=2   ,          help="rms of noise")
#parser.add_argument("-i", "--inputfile", action="store",      type=str,                     help="input file")
#
#
#
#args = parser.parse_args()
#if (args.debug):
#  print ">>> Entering Debugging Mode ... "
#DEBUG = args.debug
#filename = args.inputfile
#rms = args.rms
noise = [0,1,2,3, 4,5,6]
thrs = [6, 10, 14] #select the thrs u want to apply. Upper cut is set to 80, see below.
Ecut = 40 #80 before
rms = 2. #of the noise RMS
#filename = "PROVONA_notagli_old.root" #args.inputfile
#outfolder = "/eos/user/f/fcetorel/www/PhiSym/thr_kfactor/FitRange14-60expo_Ecut40_10kEv_1ktoys/"
outfolder = "/eos/user/f/fcetorel/www/PhiSym/thr_kfactor/FitRange14-60expo_Ecut40_10kEv_1ktoys_wnoise/"
#DEBUG = False
ip = 0
tgraph6 = R.TGraphErrors()
tgraph6.SetName("gr6")
tgraph10 = R.TGraphErrors()
tgraph6.SetName("gr10")
tgraph14 = R.TGraphErrors()
tgraph6.SetName("gr14")


for rms in noise:
  #print (rms)
  with open("output_rms_"+str(rms)+".txt","r") as If:
    reader = csv.reader(If)
    for row in reader:
      #print(row)
      if "6" in row[0] : 
        tgraph6.SetPoint(ip,rms,float(row[1]))
        tgraph6.SetPointError(ip,0,float(row[2]))
        #print "ECCOLO 6"
      elif "10" in row[0] : 
        tgraph10.SetPoint(ip,rms,float(row[1]))
        tgraph10.SetPointError(ip,0,float(row[2]))
        #print "ECCOLO 10"
      elif "14" in row[0] : 
        tgraph14.SetPoint(ip,rms,float(row[1]))
        tgraph14.SetPointError(ip,0,float(row[2]))
        print ip, rms, float(row[1])
        #print "ECCOLO 14"
    #print ip
    ip = ip +1 

c = R.TCanvas()
c.cd()

tgraph6.SetMarkerStyle(20)
tgraph10.SetMarkerStyle(20)
tgraph14.SetMarkerStyle(20)


tgraph6.SetMarkerColor(1)
tgraph10.SetMarkerColor(2)
tgraph14.SetMarkerColor(4)


tgraph14.Draw("AP ")
tgraph14.GetYaxis().SetRangeUser(0, 2.2)
tgraph14.GetXaxis().SetTitle("rms noise (ADC)")
tgraph14.GetYaxis().SetTitle("k ")


tgraph6.Draw("P same")
tgraph10.Draw("P same")



leg = R.TLegend(0.2,0.8,0.6,0.9);
leg.SetNColumns(3)
leg.AddEntry(tgraph6,"thr 6","ep")
leg.AddEntry(tgraph10,"thr 10","ep")
leg.AddEntry(tgraph14,"thr 14","ep")
leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.Draw("same")

c.SaveAs(outfolder+"kfactorVSrms.png")

graphs = [tgraph6, tgraph10, tgraph14]
#graphs = [tgraph14]
for g in graphs:
  #print "here"
  pointzero = g.GetPointY(0)
  for i in range(len(noise)):
    #print len (noise)
    
    print (g.GetPointX(i),g.GetPointY(i), pointzero,  g.GetPointY(i)/pointzero)
    g.SetPoint(i, g.GetPointX(i), g.GetPointY(i)/pointzero)

c.Clear()


tgraph14.Draw("AP ")
tgraph14.GetYaxis().SetRangeUser(0, 1.1)
tgraph14.GetXaxis().SetTitle("rms noise (ADC)")
tgraph14.GetYaxis().SetTitle("k / k_{wo noise}")

tgraph6.Draw("P same")
tgraph10.Draw("P same")



#leg1 = R.TLegend(0.2,0.8,0.6,0.9);
#leg1.SetNColumns(3)

leg1 = R.TLegend(0.15,0.2,0.25,0.4);
leg1.AddEntry(tgraph6,"thr 6","ep")
leg1.AddEntry(tgraph10,"thr 10","ep")
leg1.AddEntry(tgraph14,"thr 14","ep")
leg1.SetFillStyle(0)
leg1.SetBorderSize(0)
leg1.Draw("same")

c.SaveAs(outfolder+"kfactorVSrms_rel.png")






#tgraph6.Fit("pol1")
#tgraph10.Fit("pol1")
#tgraph14.Fit("pol1")
#
#
#c.SaveAs(outfolder+"kfactorVSrms_fit.png")
