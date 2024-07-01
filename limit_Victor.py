#! /usr/bin/env python

import os, sys, getopt
import copy
import time
import math
from array import array
from ROOT import gROOT, gRandom
from ROOT import TFile, TTree, TCut, TH1F, TH2F, TGraph, TGraph2D, TGraphErrors, TGraphAsymmErrors
from ROOT import TStyle, TCanvas, TPad
from ROOT import TLegend, TLatex, TText, TColor

from utils import *

# Combine output
# 0 - Observed Limit
# 1 - Expected  2.5%
# 2 - Expected 16.0%
# 3 - Expected 50.0%
# 4 - Expected 84.0%
# 5 - Expected 97.5%
# 6 - Significance
# 7 - p-value
# 8 - Best fit r
# 9 - Best fit r down
#10 - Best fit r up

import optparse
usage = "usage: %prog [options]"
parser = optparse.OptionParser(usage)
parser.add_option("-c", "--category", action="store", type="string", dest="category", default="")
parser.add_option("-s", "--signal", action="store", type="string", dest="signal", default="")
parser.add_option("-m", "--mediator", action="store", type="string", dest="mediator", default="SC")
parser.add_option("-j", "--bjets", action="store", type="string", dest="bjets", default="1b")
parser.add_option("-a", "--all", action="store_true", default=False, dest="all")
parser.add_option("-b", "--bash", action="store_true", default=False, dest="bash")
parser.add_option("-B", "--blind", action="store_true", default=False, dest="blind")
parser.add_option("-N", "--name", action="store", type="string", default="", dest="name")
parser.add_option("-Y", "--year", action="store", type="string", default="2016", dest="year")
parser.add_option("-R", "--ratio", action="store_false", default=True, dest="ratio")
(options, args) = parser.parse_args()
if options.bash: gROOT.SetBatch(True)
gStyle.SetOptStat(0)

if options.year == "2016":
    LUMI = 36330
elif options.year == "2017":
    LUMI = 41530
elif options.year == "2018":
    LUMI = 59740
elif options.year == "RunII":
    LUMI = 137600

if options.category=="":
    print "Specify category: AH, SL, ALL"
    sys.exit(2)

if options.signal=="":
    print "Specify signal: ttDM, tDM"
    sys.exit(2)


signals = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
#signals = [10, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
if options.mediator == "SC":
    if options.signal == "tDM":
        signalXsecs = [883.8, 339.74, 171.12, 98.81, 62.33, 41.82, 28.906, 17.516, 10.967, 7.29]
    elif options.signal == "ttDM":
        signalXsecs = [3065.5, 722.67, 240.65, 104.25, 54.20, 32.22, 21.39, 12.99, 8.125, 5.585]
    else:
        signalXsecs = [3949.3, 1062.41, 411.77, 203.06, 116.53, 74.04, 50.296, 30.506, 19.092, 12.875]
else:
    if options.signal == "tDM":
        signalXsecs = [162.95, 108.85, 74.19, 52.09, 37.63, 27.62, 16.338, 8.713, 5.967, 4.348]
    elif options.signal == "ttDM":
        signalXsecs = [309.70, 194.83, 127.30, 87.99, 60.80, 43.29, 24.69, 12.69, 8.375, 5.958]
    else:
        signalXsecs = [472.65, 303.68, 201.49, 140.08, 98.43, 70.91, 41.028, 21.403, 14.342, 10.306]

signalXsecs.insert(0, 1) #Only uncomment when including 1,10 GeV mass point
        
try: os.stat('plotsLimit_'+options.name)
except: os.mkdir('plotsLimit_'+options.name)

def fillValues(filename):
    val = {}
    mass = []
    for i, s in enumerate(signals):
        try:
            file = open(filename % s, 'r')
            if file==None:
                print "Signal", filename % s, "does not exist"
                continue
            val[s] = file.read().splitlines()
            if len(val[s]) <= 1:
                signals.remove(s)
                print "Signal", filename % s, "has no values"
                continue
            for j, f in enumerate(val[s]): 
                if options.ratio:
                    val[s][j] = float(val[s][j])
                else:
                    val[s][j] = float(val[s][j])*signalXsecs[i]
            if 'fullCls' in filename: val[1:5]=sorted(val[1:5])
            if not s in mass: mass.append(s)
        except:
            print "File", filename % s, "does not exist"
    #print val
    return mass, val





def limit(channel, signal):
    multF = 1. # in fb
    filename = "./limitOutput_"+options.name + "/" + signal + "_MChi1_MPhi%d_scalar"+options.bjets+"_"+ channel + "_AsymptoticLimits_grepOutput.txt"
    if(options.mediator=='SC'):
        filename = "./limitOutput_"+options.name + "/" + signal + "_MChi1_MPhi%d_scalar"+options.bjets+"_"+ channel + "_AsymptoticLimits_grepOutput.txt"
    elif(options.mediator=='PS'):
        filename = "./limitOutput_"+options.name + "/" + signal + "_MChi1_MPhi%d_pseudo"+options.bjets+"_"+ channel + "_AsymptoticLimits_grepOutput.txt"
    else:
        print 'WRONG mediator type'
    mass, val = fillValues(filename)
    
    Obs0s = TGraph()
    Exp0s = TGraph()
    Exp1s = TGraphAsymmErrors()
    Exp2s = TGraphAsymmErrors()
    Sign = TGraph()
    pVal = TGraph()
    Best = TGraphAsymmErrors()
    Theory0s = TGraph()
    
    for i, m in enumerate(mass):
        if not m in val:
            print "Key Error:", m, "not in value map"
            continue
        
        n = Exp0s.GetN()
        Obs0s.SetPoint(n, m, val[m][0]*multF)
        Exp0s.SetPoint(n, m, val[m][3]*multF)
        Exp1s.SetPoint(n, m, val[m][3]*multF)
        Exp1s.SetPointError(n, 0., 0., val[m][3]*multF-val[m][2]*multF, val[m][4]*multF-val[m][3]*multF)
        Exp2s.SetPoint(n, m, val[m][3]*multF)
        Exp2s.SetPointError(n, 0., 0., val[m][3]*multF-val[m][1]*multF, val[m][5]*multF-val[m][3]*multF)
        #Sign.SetPoint(n, m, val[m][6])
        #pVal.SetPoint(n, m, val[m][7])
        #Best.SetPoint(n, m, val[m][8])
        #Best.SetPointError(m, 0., 0., abs(val[m][9]), abs(val[m][10]))
        Theory0s.SetPoint(n, m, signalXsecs[i]*multF)
   
    Exp2s.SetLineWidth(2)
    Exp2s.SetLineStyle(1)
    Obs0s.SetLineWidth(3)
    Obs0s.SetMarkerStyle(0)
    Obs0s.SetLineColor(1)
    Exp0s.SetLineStyle(2)
    Exp0s.SetLineWidth(3)
    Exp1s.SetFillColor(417) #kGreen+1
    Exp1s.SetLineColor(417) #kGreen+1
    Exp2s.SetFillColor(800) #kOrange
    Exp2s.SetLineColor(800) #kOrange
    Theory0s.SetLineStyle(2)
    Theory0s.SetLineWidth(3)
    Theory0s.SetLineColor(632) #kRed
    if options.mediator=='SC':
        Exp2s.GetXaxis().SetTitle("m_{#phi} (GeV)")
    else:
        Exp2s.GetXaxis().SetTitle("m_{a} (GeV)")
    #Exp2s.GetXaxis().SetTitleSize(Exp2s.GetXaxis().GetTitleSize()*1.25)
    Exp2s.GetXaxis().SetTitleSize(Exp2s.GetXaxis().GetTitleSize()*1.25)
    Exp2s.GetXaxis().SetNoExponent(True)
    Exp2s.GetXaxis().SetMoreLogLabels(True)
    Exp2s.GetYaxis().SetTitleSize(Exp2s.GetYaxis().GetTitleSize()*1.5)
    if options.ratio:
        Exp2s.GetYaxis().SetTitle("#sigma/#sigma_{th}")
    else:
        Exp2s.GetYaxis().SetTitle("#sigma")
    Exp2s.GetYaxis().SetTitleOffset(1.5)
    Exp2s.GetYaxis().SetNoExponent(True)
    #Exp2s.GetYaxis().SetMoreLogLabels()##to uncomment

    Sign.SetLineWidth(2)
    Sign.SetLineColor(629)
    Sign.GetXaxis().SetTitle("m_{#phi} (GeV)")
    Sign.GetXaxis().SetTitleSize(Sign.GetXaxis().GetTitleSize()*1.1)
    Sign.GetYaxis().SetTitle("Significance")
    
    pVal.SetLineWidth(2)
    pVal.SetLineColor(629)
    pVal.GetXaxis().SetTitle("m_{#phi} (GeV)")
    pVal.GetXaxis().SetTitleSize(pVal.GetXaxis().GetTitleSize()*1.1)
    pVal.GetYaxis().SetTitle("local p-Value")
    
    Best.SetLineWidth(2)
    Best.SetLineColor(629)
    Best.SetFillColor(629)
    Best.SetFillStyle(3003)
    Best.GetXaxis().SetTitle("m_{#phi} (GeV)")
    Best.GetXaxis().SetTitleSize(Best.GetXaxis().GetTitleSize()*1.1)
    Best.GetYaxis().SetTitle("Best Fit (pb)")
    
    
    c1 = TCanvas("c1", "Exclusion Limits", 800, 600)
    c1.cd()
    #SetPad(c1.GetPad(0))
    c1.GetPad(0).SetTopMargin(0.06)
    c1.GetPad(0).SetRightMargin(0.05)
    c1.GetPad(0).SetTicks(1, 1)
    #c1.GetPad(0).SetGridx()
    #c1.GetPad(0).SetGridy()
    #c1.GetPad(0).SetLogx()
    c1.GetPad(0).SetLogy()

    Exp2s.Draw("A3")
    Exp1s.Draw("SAME, 3")

    #Theory Line
    c1.GetPad(0).Update()
    if options.ratio:
        line = TLine(50.,1.0,500,1.0)
        print "min",c1.GetPad(0).GetUxmin()
        print "max",c1.GetPad(0).GetUxmax()
        print "min",Exp2s.GetXaxis().GetXmin()
        print "max",Exp2s.GetXaxis().GetXmax()
        line.SetLineColor(921)
        line.SetLineWidth(2)
        line.SetLineStyle(1)
        line.Draw()
    else:
        Theory0s.Draw("SAME, L")

    Exp0s.Draw("SAME, L")
    if not options.blind: Obs0s.Draw("SAME, L")
    #Theory[0].Draw("SAME, L")
    #Theory[1].Draw("SAME, L")
    #setHistStyle(Exp2s)
    Exp2s.GetXaxis().SetTitleSize(0.045)
    Exp2s.GetXaxis().SetMoreLogLabels(True)
    Exp2s.GetXaxis().SetNoExponent(True)
    Exp2s.GetXaxis().SetLabelSize(0.04)
    Exp2s.GetXaxis().SetTitleOffset(1)

    #Exp2s.GetYaxis().SetTitleSize(0.04)
    Exp2s.GetYaxis().SetTitleSize(0.05)
    Exp2s.GetYaxis().SetLabelSize(0.04)
    #Exp2s.GetYaxis().SetTitleOffset(1.25)
    Exp2s.GetYaxis().SetTitleOffset(0.9)
    Exp2s.GetYaxis().SetMoreLogLabels(False)##to make True
    Exp2s.GetYaxis().SetNoExponent(False)## to make True

    #Exp2s.GetYaxis().SetRangeUser(0.1, 1000.)
    maximum = Exp2s.GetHistogram().GetMaximum()
    #Exp2s.GetYaxis().SetRangeUser(0.0001, maximum*1.4)
    if options.category=='ALL':
        Exp2s.GetYaxis().SetRangeUser(0.0001, 10)
    else:
        Exp2s.GetYaxis().SetRangeUser(0.0001, 14)
    #else: Exp2s.GetYaxis().SetRangeUser(0.1, 1.e2)
    if options.ratio:
        Exp2s.GetYaxis().SetRangeUser(0.05, 500.)##to remove
    else:
        Exp2s.GetYaxis().SetRangeUser(5., 1.e4)
    Exp2s.GetXaxis().SetRangeUser(mass[0], mass[-1])
    drawAnalysis("tDM")
    drawRegion(channel, True)

    latex = TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.042)
    latex.SetTextColor(1)
    latex.SetTextFont(42)
    #latex.SetTextAlign(33)
    text = ""
    if options.mediator=='SC':
        text = "#bf{Scalar, Dirac #chi, g_{#chi} = g_{q} = 1, m_{#chi} = 1 GeV}"
    else:
        text = "#bf{Pseudoscalar, Dirac #chi, g_{#chi} = g_{q} = 1, m_{#chi} = 1 GeV}"
    #latex.DrawLatex(0.15, 0.83, text)
    if options.ratio:
        latex.DrawLatex(0.15, 0.8, text)
    else:
        latex.DrawLatex(0.36, 0.8, text)
    #drawCMS(LUMI, "Preliminary")
    drawCMS(LUMI, "")
    
    if False:
        if(options.mediator=='SC'):
            massT, valT = fillValues("./limitOutput_"+options.name + "/" + signal.replace('tttDM', 'tDM') + "_MChi1_MPhi%d_scalar"+options.bjets+"_"+ channel + "_AsymptoticLimits_grepOutput.txt")
        elif(options.mediator=='PS'):
            massT, valT = fillValues("./limitOutput_"+options.name + "/" + signal.replace('tttDM', 'tDM') + "_MChi1_MPhi%d_pseudo"+options.bjets+"_"+ channel + "_AsymptoticLimits_grepOutput.txt")
        ExpT, ObsT = TGraphAsymmErrors(), TGraphAsymmErrors()
        for i, m in enumerate(massT):
            if not m in val: continue
            ExpT.SetPoint(ExpT.GetN(), m, valT[m][3]*multF)
            ObsT.SetPoint(ObsT.GetN(), m, valT[m][0]*multF)
        ExpT.SetLineWidth(3)
        ExpT.SetLineColor(602) #602
        ExpT.SetLineStyle(5)
        ObsT.SetLineWidth(3)
        ObsT.SetLineColor(602)
        ExpT.SetMarkerStyle(21)
        ObsT.SetMarkerStyle(22)
        ExpT.SetMarkerColor(602)
        ObsT.SetMarkerColor(602)
        #ExpT.Draw("SAME, PC")
        #ExpT.Draw("SAME, PL")
        #if not options.blind: ObsT.Draw("SAME, P")
        
        if(options.mediator=='SC'):
            massTTT, valTTT = fillValues("./limitOutput_"+options.name + "/" + signal.replace('tttDM', 'ttDM') + "_MChi1_MPhi%d_scalar"+options.bjets+"_"+ channel + "_AsymptoticLimits_grepOutput.txt")
        elif(options.mediator=='PS'):
            massTTT, valTTT = fillValues("./limitOutput_"+options.name + "/" + signal.replace('tttDM', 'ttDM') + "_MChi1_MPhi%d_pseudo"+options.bjets+"_" + channel + "_AsymptoticLimits_grepOutput.txt")

        ExpTTT, ObsTTT = TGraphAsymmErrors(), TGraphAsymmErrors()
        for i, m in enumerate(massTTT):
            if not m in val: continue
            ExpTTT.SetPoint(ExpTTT.GetN(), m, valTTT[m][3]*multF)
            ObsTTT.SetPoint(ObsTTT.GetN(), m, valTTT[m][0]*multF)
        ExpTTT.SetLineWidth(3)
        ExpTTT.SetLineColor(634) #602
        ExpTTT.SetLineStyle(5)
        ObsTTT.SetLineWidth(3)
        ObsTTT.SetLineColor(634)
        ExpTTT.SetMarkerStyle(22)
        ExpTTT.SetMarkerSize(1.3)
        ObsTTT.SetMarkerStyle(22)
        ExpTTT.SetMarkerColor(634)
        ObsTTT.SetMarkerColor(634)
        #ExpTTT.Draw("SAME, PC")
        #ExpTTT.Draw("SAME, PL")
        #if not options.blind: ObsTTT.Draw("SAME, P")
    

    # legend
    #top = 0.9
    top = 0.8
    nitems = 4+2
    
    #leg = TLegend(0.55, top-nitems*0.3/5., 0.95, top)
    #leg = TLegend(0.15, 0.40, 0.55, 0.76)
    if options.ratio:
        leg = TLegend(0.14, 0.52, 0.49, 0.76)
    else:
        leg = TLegend(0.35, 0.52, 0.70, 0.76)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0) #1001
    leg.SetFillColor(0)
    leg.SetTextSize(0.04)
    leg.SetTextSize(0.037)
    #leg.SetHeader("95% CL limits")
    # if options.mediator=='SC':
    #     leg.SetHeader("Scalar, Dirac #chi, g_{#chi} = g_{q} = 1, m_{#chi} = 1 GeV")
    # else:
    #     leg.SetHeader("Pseudoscalar, Dirac #chi, g_{#chi} = g_{q} = 1, m_{#chi} = 1 GeV")
    if not options.ratio: leg.AddEntry(Theory0s, "LO #sigma_{th}", "l")
    if not options.blind: leg.AddEntry(Obs0s,  "Observed 95% CL", "l")
    if options.signal == "tDM":
        leg.AddEntry(Exp0s,  "Median expected 95% CL (t+DM)", "l")
    elif options.signal == "ttDM":
        leg.AddEntry(Exp0s,  "Median expected 95% CL (tt+DM)", "l")
    elif options.signal == "tttDM":
        leg.AddEntry(Exp0s,  "Median expected 95% CL (t/tt+DM)", "l")
    leg.AddEntry(Exp1s, "68% CL expected", "f")
    leg.AddEntry(Exp2s, "95% CL expected", "f")

    # leg.AddEntry(Exp1s, "#pm 1 s. d.", "f")
    # leg.AddEntry(Exp2s, "#pm 2 s. d.", "f")
    if False:## put to True
        leg.AddEntry(ExpT,  "Median expected 95% CL (t+DM)", "pl")
        leg.AddEntry(ExpTTT,  "Median expected 95% CL (tt+DM)", "pl")
        #leg.AddEntry(line, "#sigma/#sigma_{th}=1", "l")        
    leg.Draw()
    c1.GetPad(0).RedrawAxis()
    c1.GetPad(0).Update()
    if gROOT.IsBatch():
        suffix = ""
        if not options.ratio:
            suffix += "_noRatio"
        if options.blind:
            suffix += "_blind"
        c1.Print("plotsLimit_"+options.name+"/Exclusion_"+channel+"_"+options.mediator+"_"+options.bjets+suffix+".root")
        c1.Print("plotsLimit_"+options.name+"/Exclusion_"+channel+"_"+options.mediator+"_"+options.bjets+suffix+".png")
        c1.Print("plotsLimit_"+options.name+"/Exclusion_"+channel+"_"+options.mediator+"_"+options.bjets+suffix+".pdf")

    if not gROOT.IsBatch(): raw_input("Press Enter to continue...")
    
#    print "p1s[",
#    for i in range(Exp0s.GetN()):
#        print Exp0s.GetY()[i]+Exp1s.GetErrorYhigh(i), ",",
#    print "],"
#    print "m1s[",
#    for i in range(Exp0s.GetN()):
#        print Exp0s.GetY()[i]-Exp1s.GetErrorYlow(i), ",",
#    print "],"
#    print "[",
#    for i in range(Exp0s.GetN()):
#        print Exp0s.GetY()[i], ",",
#    print "]"
    
    return
    
    # ---------- Significance ----------
    c2 = TCanvas("c2", "Significance", 800, 600)
    c2.cd()
    c2.GetPad(0).SetTopMargin(0.06)
    c2.GetPad(0).SetRightMargin(0.05)
    c2.GetPad(0).SetTicks(1, 1)
    c2.GetPad(0).SetGridx()
    c2.GetPad(0).SetGridy()
    Sign.GetYaxis().SetRangeUser(0., 5.)
    Sign.Draw("AL3")
    drawCMS(LUMI, "Preliminary")
    drawAnalysis(channel[1:3])
    if gROOT.IsBatch():
        c2.Print("plotsLimit_"+options.name+"/Significance/"+channel+"_"+options.mediator+"_"+options.bjets+".png")
        c2.Print("plotsLimit_"+options.name+"/Significance/"+channel+"_"+options.mediator+"_"+options.bjets+".pdf")
#    c2.Print("plotsLimit/Significance/"+channel+suffix+".root")
#    c2.Print("plotsLimit/Significance/"+channel+suffix+".C")

    # ---------- p-Value ----------
    c3 = TCanvas("c3", "p-Value", 800, 600)
    c3.cd()
    c3.GetPad(0).SetTopMargin(0.06)
    c3.GetPad(0).SetRightMargin(0.05)
    c3.GetPad(0).SetTicks(1, 1)
    c3.GetPad(0).SetGridx()
    c3.GetPad(0).SetGridy()
    c3.GetPad(0).SetLogy()
    pVal.Draw("AL3")
    pVal.GetYaxis().SetRangeUser(2.e-7, 0.5)
    
    ci = [1., 0.317310508, 0.045500264, 0.002699796, 0.00006334, 0.000000573303, 0.000000001973]
    line = TLine()
    line.SetLineColor(922)
    line.SetLineStyle(7)
    text = TLatex()
    text.SetTextColor(922)
    text.SetTextSize(0.025)
    text.SetTextAlign(12)
    for i in range(1, len(ci)-1):
        line.DrawLine(pVal.GetXaxis().GetXmin(), ci[i]/2, pVal.GetXaxis().GetXmax(), ci[i]/2);
        text.DrawLatex(pVal.GetXaxis().GetXmax()*1.01, ci[i]/2, "%d #sigma" % i);
    
    drawCMS(LUMI, "Preliminary")
    drawAnalysis(channel[1:3])
    if gROOT.IsBatch():
        c3.Print("plotsLimit_"+options.name+"/pValue/"+channel+suffix+"_"+options.mediator+"_"+options.bjets+".png")
        c3.Print("plotsLimit_"+options.name+"/pValue/"+channel+suffix+"_"+options.mediator+"_"+options.bjets+".pdf")
#    c3.Print("plotsLimit/pValue/"+channel+suffix+".root")
#    c3.Print("plotsLimit/pValue/"+channel+suffix+".C")

    # --------- Best Fit ----------
    c4 = TCanvas("c4", "Best Fit", 800, 600)
    c4.cd()
    c4.GetPad(0).SetTopMargin(0.06)
    c4.GetPad(0).SetRightMargin(0.05)
    c4.GetPad(0).SetTicks(1, 1)
    c4.GetPad(0).SetGridx()
    c4.GetPad(0).SetGridy()
    Best.Draw("AL3")
    drawCMS(LUMI, "Preliminary")
    drawAnalysis(channel[1:3])
    if gROOT.IsBatch():
        c4.Print("plotsLimit_"+options.name+"/BestFit/"+channel+suffix+"_"+options.mediator+"_"+options.bjets+".png")
        c4.Print("plotsLimit_"+options.name+"/BestFit/"+channel+suffix+"_"+options.mediator+"_"+options.bjets+".pdf")
#    c4.Print("plotsLimit/BestFit/"+channel+suffix+".root")
#    c4.Print("plotsLimit/BestFit/"+channel+suffix+".C")
    
    if not gROOT.IsBatch(): raw_input("Press Enter to continue...")



if options.all:
    limit("tttDM")
else:
    limit(options.category, options.signal)
