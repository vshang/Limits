import numpy as np
import json
import CMS_lumi
import os
import copy
import ROOT

def main():
    
    #work_dir = "."
    #plots_dir = "."
    
    ROOT.gROOT.SetBatch()
    ROOT.gStyle.SetOptStat(0000)
    ROOT.gStyle.SetPalette(ROOT.kVisibleSpectrum)
    
    file_obs = ROOT.TFile("higgsCombineTest.GoodnessOfFit.mH100.root","READ")
    file_toys = ROOT.TFile("higgsCombineTest.GoodnessOfFit.mH100.Toys.root","READ")
    
    
    limit_obs = np.zeros((1), dtype="float64")
    limit_toys = np.zeros((1), dtype="float64")
    m_h = np.zeros((1), dtype="float64")
    
    ########### Data #################
    tree_obs = file_obs.Get("limit")
    tree_obs.SetBranchAddress("limit",limit_obs)
    tree_obs.SetBranchAddress("mh",m_h)
    tree_obs.GetEntry(0)
    
    
    ########### Toys #################
    tree_toys = file_toys.Get("limit")
    tree_toys.SetBranchAddress("limit",limit_toys)

    #Histo =ROOT.TH1D("Histo","",40,(0.85)*tree_toys.GetMinimum("limit"),(0.95)*tree_toys.GetMaximum("limit"))
    Histo =ROOT.TH1D("Histo","",40,40,180)

    for iEvent in range(tree_toys.GetEntries()):
        tree_toys.GetEntry(iEvent)
        Histo.Fill(limit_toys,1.)
    Histo.Scale(1/Histo.Integral())

    bin_obs = Histo.GetXaxis().FindBin(limit_obs)
    p_value = Histo.Integral(bin_obs,Histo.GetNbinsX())
    print("p-value: " + str(p_value))
    
    canvas = ROOT.TCanvas("canvas","canvas",900,900)
    canvas.cd()
    canvas.SetTicks()
    canvas.SetLeftMargin(0.15)
    canvas.SetRightMargin(0.05)
    canvas.SetBottomMargin(0.13)
    
    Histo.GetYaxis().SetRangeUser(0.,1.6*Histo.GetMaximum())
    Histo.SetLineColor(ROOT.kSpring-8)
    Histo.SetLineWidth(1)
    Histo.SetLineStyle(1)
    Histo.SetFillColorAlpha(ROOT.kSpring-8,0.20)
    Histo.SetFillStyle(1001)
    Histo.GetYaxis().SetTitleOffset(1.5)
    Histo.GetYaxis().SetTitle("Normalized to unity")
    Histo.GetYaxis().SetTitleSize(0.038)
    Histo.GetYaxis().SetLabelSize(0.032)
    Histo.GetYaxis().SetTickLength(0.03)
    Histo.GetXaxis().SetLabelFont(42)
    Histo.GetXaxis().SetLabelSize(0.032)
    Histo.GetXaxis().SetTitleSize(0.038)
    Histo.GetXaxis().SetTitleOffset(1.3)
    Histo.GetXaxis().SetTitle("-2 ln #lambda (saturated)")
    Histo.GetXaxis().SetTickLength(0.03)
    
    Histo_PValue = Histo.Clone("Histo_PValue")
    Histo_PValue.SetLineColor(ROOT.kRed)
    Histo_PValue.SetLineWidth(0)
    Histo_PValue.SetFillColorAlpha(ROOT.kRed,0.40)
    
    arrow = ROOT.TArrow(Histo.GetBinLowEdge(bin_obs),0.002,Histo.GetBinLowEdge(bin_obs),0.4*Histo.GetBinContent(bin_obs),0.02,"<|")
    arrow.SetAngle(50)
    arrow.SetLineWidth(3)
    arrow.SetLineColor(ROOT.kRed)
    arrow.SetFillColorAlpha(ROOT.kRed,0.45)
    
    for iBin in range(Histo_PValue.GetXaxis().FindBin(limit_obs)):
        Histo_PValue.SetBinContent(iBin,0.)
    
    Histo.Draw("h")
    Histo_PValue.Draw("sameh")
    arrow.Draw()
    
    leg = ROOT.TLegend(0.55,0.55,0.9,0.75)
    leg.SetTextSize(0.035)
    leg.SetBorderSize(0)
    leg.AddEntry(arrow,"Observed","l")
    leg.AddEntry(Histo,"Expected (Toys)","lf")
    leg.Draw()
    
    Latex = ROOT.TLatex()
    Latex.SetNDC()
    Latex.SetTextColor(ROOT.kGray+2)
    Latex.SetTextSize(0.04)
    Latex.SetTextFont(12)
    Latex.DrawLatex(1-canvas.GetRightMargin()-0.75,1-canvas.GetTopMargin()-0.1,"Sig+Bkgd")
    Latex.DrawLatex(1-canvas.GetRightMargin()-0.75,1-canvas.GetTopMargin()-0.15,"p-value: " + str(round(p_value,3)))
    Latex.DrawLatex(canvas.GetLeftMargin()+0.01,1+0.02-canvas.GetTopMargin(),'#color[4]{SL}')
        
    CMS_lumi.CMS_lumi(canvas, 15, 3)
    
    canvas.Update()
    canvas.Print("GoF.pdf","Portrait pdf")
    
    
if __name__ == "__main__":
    main()
