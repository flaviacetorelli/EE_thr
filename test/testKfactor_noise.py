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
parser = argparse.ArgumentParser()
parser.add_argument('--debug',           action='store_true',           default=False,      help='debugging mode')
parser.add_argument("-r", "--rms",     action="store",      type=float,       default=2   ,          help="rms of noise")
parser.add_argument("-i", "--inputfile", action="store",      type=str,                     help="input file")



args = parser.parse_args()
if (args.debug):
  print ">>> Entering Debugging Mode ... "
DEBUG = args.debug
filename = args.inputfile
rms = args.rms

thrs = [6, 10, 14] #select the thrs u want to apply. Upper cut is set to 80, see below.
Ecut = 40 #80 before
#rms = 6. #of the noise RMS
#filename = "PROVONA_notagli_old.root" #args.inputfile
#outfolder = "/eos/user/f/fcetorel/www/PhiSym/thr_kfactor/FitRange14-60expo_Ecut40_10kEv_1ktoys/"
outfolder = "/eos/user/f/fcetorel/www/PhiSym/thr_kfactor/FitRange14-60expo_Ecut40_10kEv_1ktoys_wnoise/RMS_"+str(int(rms))+"/"
#DEBUG = False



if not os.path.exists(filename): 
  print '>>> This File does not exist -->  '+filename+'... check path ... '
else:
  print '>>> Opening File :' , filename
  inFile = R.TFile.Open ( filename," READ ")
  tree = inFile.Get("PulseTreeProducer/tree")


if not os.path.exists(outfolder):
  os.mkdir(outfolder)

c = R.TCanvas()

############# Find the signal expr by fitting with expo
h=R.TH1F("h","h", 100 ,0, 100)
tree.Draw("amplitude_EE>>h","amplitude_EE>14 && amplitude_EE < 100","goff")
#fun=R.TF1("fun","pol3",4,100)
#fun=R.TF1("fun","[0]*x*expo",4,60)
fun=R.TF1("fun","expo",4,100)
h.Fit("fun", "Q","",14,60) #FIT range
h.SetLineColor(6)
h.GetYaxis().SetRangeUser(0,5000)
h.Draw()
fun.Draw("same")
#print (fun.GetParameter(0), fun.GetParameter(1))
fun.SetParameter(0,fun.GetParameter(0))
fun.SetParameter(1,fun.GetParameter(1))
c.Update()
c.SaveAs(outfolder+"Energy_histos_expo_14-60.png")
hk6 = R.TH1F("hk6","6", 100 ,0, 1.5)
hk10 = R.TH1F("hk10","10", 100 ,0.5, 2)
hk14 = R.TH1F("hk14","14", 100 ,1, 2.5)


gnoise = R.TF1 ("gnoise","gaus", 0,200) #gaussian smearing


#generating toys wrt to expo function above
for t in range(0,1000):
  
  hrand = R.TH1F("hrand_"+str(t),"hrand", 100 ,0, 100)
  hrand_p2 = R.TH1F("hrand_p2_"+str(t),"hrand_p2", 100 ,0, 100)
  hrand_p1 = R.TH1F("hrand_p1_"+str(t),"hrand_p1", 100 ,0, 100)
  hrand_m1 = R.TH1F("hrand_m1_"+str(t),"hrand_m1", 100 ,0, 100)
  hrand_m2 = R.TH1F("hrand_m2_"+str(t),"hrand_m2", 100 ,0, 100)
  allhisto = [hrand_m2, hrand_m1 ,hrand,hrand_p1,hrand_p2]
  
  #generate nominal and miscalibrated histos
  for i in range(0,10000):
    etoy = fun.GetRandom() #toy energy from expo
    
    gnoise.SetParameters(1, etoy, rms )
    
    etoy_smear = gnoise.GetRandom() 

    hrand.Fill(etoy_smear)
    hrand_p2.Fill(etoy_smear*1.05)
    hrand_p1.Fill(etoy_smear*1.02)
    hrand_m1.Fill(etoy_smear*0.98)
    hrand_m2.Fill(etoy_smear*0.95)


  c.cd()

  color = 1
  for hist in allhisto:
    hist.SetLineColor(color) 
    hist.Scale(fun.Integral(4,100)/hist.Integral())
    hist.Draw("histo same")
    color = color + 1

  cmy = R.TCanvas()
  cmy.cd()
  hrand.SetLineColor(1)
  hrand.Draw("histo")

  hrand_p2.SetLineColor(3)
  hrand_p2.Draw("histo same")


  hrand_m2.SetLineColor(4)
  hrand_m2.Draw("histo same")
  fun.Draw("same")  
  #print (fun.Integral(0,100))
  #print (hrand.Integral())
    
  if t == 1 :    
    c.SaveAs(outfolder+"Energy_histos_"+str(t)+".png")
    cmy.SaveAs(outfolder+"Energy_histos_bello_"+str(t)+".png")
  
  Et = []

  for thr in thrs:
    et = []
    mesmis = []
    for hist in allhisto:
      et.append(hist.Integral(thr,Ecut))
    Et.append(et)
    for mis in et:
      #print (mis)
      mesmis.append(mis/et[2]-1)
    mesmis.sort()
    #print (mesmis)
    truemis = [-0.05, -0.02, 0, 0.02, 0.05]
    graph = R.TGraph(5, array('f',truemis),  array('f',mesmis))
    c1 = R.TCanvas()
    graph.SetMarkerStyle(22)
    kfit = R.TF1("kfit", "pol1")
    graph.Fit("kfit", "Q")
    #kfit.GetParameter(0)
    if DEBUG: print("THR is ", thr)
    if thr is 6: 
      if DEBUG: print ("so i'm here in 6")
      hk6.Fill(kfit.GetParameter(1))
    elif thr is 10: 
      if DEBUG: print ("so i'm here in 10")
      hk10.Fill(kfit.GetParameter(1))
    else: 
      if DEBUG: print ("so i'm here in 14")
      hk14.Fill(kfit.GetParameter(1))
    
  
    if t == 1: 
      R.gStyle.SetOptFit(1)
      graph.Draw("AP")
      c1.SaveAs(outfolder+"kfactorFit_"+str(thr)+"_"+str(t)+".png")


#finally plot the k factor histo
khisto = [hk6, hk10, hk14]

with open("output_rms_"+str(int(rms))+".txt","w") as of:
  print ("THR   ,  Mean   ,  err mean")
  of.write("THR   ,  Mean   ,  err mean\n")
  for kh in khisto:
    c2 =R.TCanvas()
    c2.cd()
    kh.Draw("histo")
    kh.SetStats(1) 
    print (kh.GetTitle(), kh.GetMean(), kh.GetMeanError()) 
    of.write("{},{:.2f},{:.2f}\n".format(int(kh.GetTitle()), kh.GetMean(), kh.GetMeanError()))
    c2.SaveAs(outfolder+"histo_"+kh.GetName()+".png")
#print Et



########################## testing the goodness of trowing gauss
    #hsmear = R.TH1F("","",100,0,100)

    #for n in range (0,10000):  
      #print gnoise.GetRandom()
      #hsmear.Fill( gnoise.GetRandom())
    #cp = R.TCanvas()
    #cp.cd()

    #hsmear.Draw("histo")
    #cp.SaveAs(outfolder+"noiseGauss_"+str(int(m))+".png")
 
