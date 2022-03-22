import sys
import os
import csv


import argparse 

import ROOT as R
R.gROOT.SetBatch(True) 

def Average(lst):
    return sum(lst) / len(lst)

def doGraph(listX, listY, fileout):
  c = R.TCanvas()
  gr = R.TGraph ()
  for i in range(0,len(listX)):
    gr.SetPoint(i,listX[i], listY[i])  

  gr.SetMarkerStyle(22)
  gr.Draw("")
  c.SaveAs(fileout+".png")


 

#Code to scan different thresholds for EE

#args = parser.parse_args()
nEvTot = []
meanXstal = []
meanHit = []
#thrAmp = [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12]
#thrAmp = [0,2,4,6,8,10,12]
thrAmp = [12,15]
#if (args.debug):
#  print ">>> Entering Debugging Mode ... "
#DEBUG = args.debug
#savePlot = args.savePlot
#outdir=args.outdir
filename = "PROVONA_notagli.root" #args.inputfile
DEBUG = False

if not os.path.exists(filename): 
  print '>>> This File does not exist -->  '+filename+'... check path ... '
else:
  print '>>> Opening File :' , filename
  inFile = R.TFile.Open ( filename," READ ")
  tree = inFile.Get("PulseTreeProducer/tree")


#Number of hits total over thr vs thr
#print (">>>>>>>>>> Doing hits total over thr")
#for thr in thrAmp:
#  #print(thr)
#  
#  h=R.TH1F("","", 100 ,0, 40)
#  n = tree.Draw("amplitude_EE>>h","amplitude_EE>"+str(thr)+" && amplitude_EE < 40","goff")
#  #print(thr,int( n) )
#  nEvTot.append( int(n)  )
#  #print (thr,nEvTot[0] )
#
#doGraph(thrAmp, nEvTot, "EvTotvsThr")
#
#print (">>>>>>>>>> Ended hits total over thr")

EExstals =  14648
EBxstals = 62100

#Number of xstal per event vs thr

print (">>>>>>>>>> Doing mean xstal over thr")
for thr in thrAmp:
  print (">>>>>>>>>>>>> NOW thr: ", thr)
  app=[]
  for ev in tree:
    nXstal = 0
#    for xstal in range(0,EExstals):
#      if DEBUG: print ("That's xstal: ", xstal, " with amplitude ", ev.amplitude_EE[xstal])
#      if (ev.amplitude_EE[xstal] > thr):
#        if DEBUG: print ("PASSED")
#        nXstal= nXstal+1   
#        if DEBUG: print ("So N xstals = ", nXstal)
#    app.append(nXstal)
#  meanXstal.append(Average(app))

    for xstal in range(0,EBxstals):
      if DEBUG: print ("That's xstal: ", xstal, " with amplitude ", ev.amplitude_EB[xstal])
      if (ev.amplitude_EB[xstal] > thr):
        if DEBUG: print ("PASSED")
        nXstal= nXstal+1   
        if DEBUG: print ("So N xstals = ", nXstal)
    app.append(nXstal)
  meanXstal.append(Average(app))


print (meanXstal)
#doGraph(thrAmp, meanXstal, "meanXstalvsThr")      

print (">>>>>>>>>> Ended mean xstal over thr")



#print (">>>>>>>>>> Doing mean hits over thr")
#for thr in thrAmp:
#  app=[]
#  nHit = 0
#  
#  print (">>>>>>>>>>>>> NOW thr: ", thr)
#  for xstal in range(0,EExstals):
#    for ev in tree:
#      if (ev.amplitude_EE[xstal] > thr):
#        if DEBUG: print ("PASSED")
#        nHit= nHit+1   
#        if DEBUG: print ("So N xstals = ", nXstal)
#    app.append(nHit)
#  print (app)
#  meanHit.append(Average(app))
#
#doGraph(thrAmp, meanHit, "meanHitsvsThr")      
#
#
#print (">>>>>>>>>> Ended mean hits over thr")
