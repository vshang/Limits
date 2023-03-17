#! /usr/bin/env python

import os, sys, getopt, multiprocessing
import copy
import math
from array import array
from ROOT import gROOT, TFile, TH1F

import optparse
usage = "usage: %prog [options]"
parser = optparse.OptionParser(usage)
parser.add_option("-f", "--fileName", action="store", type="string", dest="fileName", default="")
parser.add_option("-r", "--remove", action="store", type="string", default="", dest="catList")
parser.add_option("-c", "--cutcount", action="store_true", default=False, dest="isCutAndCount")
parser.add_option("-o", "--override", action="store_true", default=False, dest="override")
parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose")
parser.add_option("-N", "--name", action="store", type="string", dest="name", default="test")
parser.add_option("-Y", "--year", action="store", type="string", default="2016", dest="year")
(options, args) = parser.parse_args()

fileName = options.fileName
catList = options.catList
isShape = not options.isCutAndCount
isOverride = options.override
verbose = options.verbose
year = options.year

jobs = []

#latest one used
greenShape = ['CMS_res_j_'+year, 'CMS_WewkWeight', 'CMS_ZewkWeight', 'CMS_pdf', 'CMS_eff_b_corr', 'CMS_eff_b_light_corr', 'CMS_eff_b_'+year, 'CMS_eff_b_light_'+year, 'CMS_scale_pu', 'CMS_eff_met_trigger', 'QCDScale_ren_TT', 'QCDScale_fac_TT', 'QCDScale_ren_VV', 'QCDScale_fac_VV', 'preFire', 'CMS_eff_e', 'CMS_eff_m', 'CMS_trig_e', 'CMS_trig_m']

#greenShape = ['CMS_res_j_'+year, 'CMS_WqcdWeightRen', 'CMS_WqcdWeightFac', 'CMS_WewkWeight', 'CMS_ZqcdWeightRen', 'CMS_ZqcdWeightFac', 'CMS_ZewkWeight', 'CMS_pdf', 'CMS_eff_b_corr', 'CMS_eff_b_light_corr', 'CMS_eff_b_'+year, 'CMS_eff_b_light_'+year, 'CMS_scale_pu', 'CMS_eff_met_trigger', 'QCDScale_ren_TT', 'QCDScale_fac_TT', 'QCDScale_ren_VV', 'QCDScale_fac_VV', 'preFire', 'CMS_eff_e', 'CMS_eff_m', 'CMS_trig_e', 'CMS_trig_m']

#greenShape = ['CMS_res_j_'+year, 'CMS_WqcdWeightRen', 'CMS_WqcdWeightFac', 'CMS_WewkWeight', 'CMS_ZqcdWeightRen', 'CMS_ZqcdWeightFac', 'CMS_ZewkWeight', 'CMS_pdf', 'CMS_eff_b_corr', 'CMS_eff_b_light_corr', 'CMS_eff_b_'+year, 'CMS_eff_b_light_'+year, 'CMS_scale_pu', 'CMS_eff_met_trigger', 'QCDScale_ren_TT', 'QCDScale_fac_TT', 'QCDScale_ren_VV', 'QCDScale_fac_VV', 'preFire', 'CMS_eff_lep', 'CMS_eff_lep_trigger']

#greenShape = ['CMS_res_j_'+year, 'CMS_scale_j']

#greenShape = []

categories = []
back = []
sign = []

#CMS_scale_j, CMS_res_j, CMS_eff_b, CMS_scale_q2, CMS_scale_met, CMS_scale_pu, CMS_eff_l, lumi_8TeV, pdf_gg, pdf_qg, pdf_qq, CMS_norm_ZJets

#shape = ['CMS_eff_b', 'CMS_scale_pu' 'CMS_eff_trigger', 'CMS_eff_e', 'CMS_eff_m', 'QCDscale', 'EWKscale'] #, 'pdf', 'CMS_scale_met_jes', 'CMS_scale_met_jer', 'CMS_scale_met_m', 'CMS_scale_met_e', 'CMS_scale_met_t', 'CMS_scale_met_u', 'CMS_scale_met_g',



shape = []
#jesUnc = ['AbsoluteMPFBias', 'AbsoluteScale', 'AbsoluteStat', 'FlavorQCD', 'Fragmentation', 'PileUpDataMC', 'PileUpPtBB', 'PileUpPtEC1', 'PileUpPtEC2', 'PileUpPtHF', 'PileUpPtRef', 'RelativeFSR', 'RelativeJEREC1', 'RelativeJEREC2', 'RelativeJERHF', 'RelativePtBB', 'RelativePtEC1', 'RelativePtEC2', 'RelativePtHF', 'RelativeBal', 'RelativeSample', 'RelativeStatEC', 'RelativeStatFSR', 'RelativeStatHF', 'SinglePionECAL', 'SinglePionHCAL', 'TimePtEta']
jesUnc = ['AbsoluteMPFBias', 'AbsoluteScale', 'AbsoluteStat', 'FlavorQCD', 'Fragmentation', 'PileUpDataMC', 'PileUpPtBB', 'PileUpPtEC1', 'PileUpPtEC2', 'PileUpPtHF', 'PileUpPtRef', 'RelativeFSR']
for unc in jesUnc:
    greenShape.append('CMS_scale'+unc+'_j')

norm = {
#    "QCDscale_Z_ACCEPT" : {"DYJets" : 1.03,},
#    "QCDscale_W_ACCEPT" : {"WJets": 1.03,},
#    "CMS_norm_VH" : {"VH" : 1.15,},
#    "CMS_norm_VV" : {"VV" : 1.15,},
#    "CMS_norm_ST" : {"ST" : 1.15,},
#    "Cms_norm_QCD" : {"QCD" : 1.50,},
#    'CMS_scale_j'  : {"VH" : 1.030, "VV" : 1.030, "ST" : 1.030, "QCD" : 1.030, "DM" : 1.030},
#    'CMS_res_j'  : {"VH" : 1.010, "VV" : 1.010, "ST" : 1.010, "QCD" : 1.010, "DM" : 1.010},
#    "CMS_eff_t" : {"VH" : 1.030, "VV" : 1.030, "ST" : 1.030, "QCD" : 1.030,},
#    "CMS_eff_met_trigger": {"VH" : 1.02, "VV" : 1.02, "ST" : 1.02, "QCD" : 1.02, "DM" : 1.02},
    #"pdf_accept_2l_Z" :{DYJetsToLL_HT                 DYJetsToNuNu_HT  }

    # #paper
    # "preFire_2b" :{"DM":1.03},
    # "preFire_1f" :{"DM":1.10},
    # "pdf_accept_Z" :{"DYJetsToLL_HT":1.06},
    # "pdf_accept_1l_T" :{"TTbarSL": 1.03},
    # "pdf_accept_2l_T" :{"TTbarSL": 1.06},
    # "pdf_accept_W" :{"WJetsToLNu_HT": 1.03},
    # "forwJet_SL_T":{"TTbarSL": 1.067},
    # "forwJet_SL_W":{"WJetsToLNu_HT": 1.043},
    # "forwJet_AH_T":{"TTbarSL": 1.045},
    # "forwJet_AH_W":{"WJetsToLNu_HT": 1.024},
    # "forwJet_AH_Z":{"DYJetsToNuNu_HT": 1.066},
    # "QCD_xsec"   : {"QCD" : 2.000},
    # "ST_xsec"    : {"ST" : 1.200},
    # "lumi_13TeV" : {"VH" : 1.025, "VV" : 1.025, "ST" : 1.025, "QCD" : 1.025, "DM" : 1.025},

    #Run2 tests
    #"preFire_2b" :{"DM":1.03},
    #"preFire_1f" :{"DM":1.10},
    #"pdf_accept_Z" :{"DYJetsToLL":1.06},
    #"pdf_accept_1l_T" :{"TTbarSL": 1.03},
    #"pdf_accept_2l_T" :{"TTbarSL": 1.06},
    #"pdf_accept_W" :{"WJetsToLNu": 1.03},
    #"forwJet_SL_T":{"TTbarSL": 1.067},
    #"forwJet_SL_W":{"WJetsToLNu": 1.043},
    #"forwJet_AH_T":{"TTbarSL": 1.045},
    #"forwJet_AH_W":{"WJetsToLNu": 1.024},
    #"forwJet_AH_Z":{"DYJetsToNuNu": 1.066},
    #"QCD_xsec"   : {"QCD" : 2.000},
    #"QCD_xsec"   : {"QCD" : 1.500},
    "ST_xsec"     : {"ST" : 1.200},
    "QCDScale_tDM" : {"tDM_" : 1.3},
    "QCDScale_ttDM" : {"ttDM_" : 1.3},
    "QCDScale_tttDM" : {"tttDM_" : 1.3},
    "ttH_HToInv_xsec" : {"ttDM_" : [1.068, 0.901]},
    "CMS_PSisr"   : {"VV" : 1.05, "ST" : 1.05, "DM" : 1.05},
    "CMS_PSfsr"   : {"VV" : 1.05, "ST" : 1.05, "DM" : 1.05},
    #"CMS_pdf"   : {"VV" : 1.05, "ST" : 1.05},
    #"lumi16_13TeV" : {"VV" : 1.012, "ST" : 1.012, "DM" : 1.012},
    #"lumi17_13TeV" : {"VV" : 1.023, "ST" : 1.023, "DM" : 1.023},
    #"lumi18_13TeV" : {"VV" : 1.025,  "ST" : 1.025, "DM" : 1.025},
}

#Add lumi norm uncertainties based on year
if year == "2016":
    norm["lumi16_13TeV"] = {"VV" : 1.012, "ST" : 1.012, "DM" : 1.012}
    greenShape.append('CMS_UncMET_2016')
    greenShape.append('CMS_WqcdWeightRen')
    greenShape.append('CMS_WqcdWeightFac')
    greenShape.append('CMS_ZqcdWeightRen')
    greenShape.append('CMS_WqcdWeightFac')
elif year == "2017":
    norm["lumi17_13TeV"] = {"VV" : 1.023, "ST" : 1.023, "DM" : 1.023}
    greenShape.append('CMS_UncMET_2017')
elif year == "2018":
    norm["lumi18_13TeV"] = {"VV" : 1.025,  "ST" : 1.025, "DM" : 1.025}
    greenShape.append('CMS_UncMET_2018')

freenorm = {
#    "CMS_norm_DYJetsToNuNu_HT" : 4,
#    "CMS_norm_DYJetsToLL_HT" : 4,
#    "CMS_norm_WJetsToLNu_HT" : 4,
#    "CMS_norm_TTbarSL" : 4,
}


rateparam = {
    # #paper
    # 'rateTopAH' : 'ST',
    # 'rateTopAH' : 'TTbarSL',
    # 'rateZjetsAH' : 'DYJetsToNuNu_HT',
    # 'rateZjetsAH_ZR' : 'DYJetsToLL_HT', #will effectively be called rateZjetsAH
    # 'rateWjetsAH' : 'WJetsToLNu_HT',
    # 'rateTopSL' : 'TTbarSL',
    # 'rateWjetsSL' : 'WJetsToLNu_HT',

    #Run2 tests
    #'rateTopAH' : 'ST',
    # #paper
    'rateQCDAH'+year : 'QCD',
    # 'rateTopAH' : 'TTbarSL',
    # 'rateTopSL' : 'TTbarSL',
    'rateTopSL'+year : 'TTTo2L2Nu', 
    'rateTopAH'+year : 'TTToSemiLepton',
    #'rateTop2lepAH' : 'TTTo2L2Nu',
    # 'ratetopsl' : 'TTTo2L2Nu',

    'rateZjetsAH'+year : 'DYJetsToNuNu',
    'rateZjetsAH_ZR'+year : 'DYJetsToLL', #will effectively be called rateZjetsAH

    'rateWjetsAH'+year : 'WJetsToLNu',
    'rateWjetsSL'+year : 'WJetsToLNu',



}


def datacard(cat, sign):
    
    if verbose: print "  Starting datacard for category", cat, "and mass", sign, "..."
    
#    hist = {}
#    syst = {}
#    nbin = {}
#    name = {}
#    inFile = TFile("rootfiles/"+cat+".root", "READ")
#    inFile.cd()
#    for c in categories:
#        hist[c] = {}
#        syst[c] = {}
#        nbin[c] = inFile.Get(c+"/data_obs").GetNbinsX() if isShape else 1
#        hist[c]["data_obs"] = inFile.Get(c+"/data_obs")
#        #print "  category", c, "has", nbin[c], "bins"
#        for i, s in enumerate(back + sign):
#            hist[c][s] = inFile.Get(c+"/"+s)
#            #print c, s, hist[c][s].Integral()
#            #if 'CR' in c: continue
#            syst[c][s] = {}
#            for i, h in enumerate(shape):
#                base = c+"/Sys_"+s+"/"+h
#                #print c, s, h, base, inFile.Get(base).Integral(), inFile.Get(base+"Up").Integral(), inFile.Get(base+"Down").Integral()
#                syst[c][s][h] = [inFile.Get(base), inFile.Get(base+"Up"), inFile.Get(base+"Down")]
#                #print c, s, h, syst[c][s][h][0].Integral(), syst[c][s][h][1].Integral(), syst[c][s][h][-1].Integral()
#    
#    if verbose: print "  Histagrams read, producing header..."
    #exit()
    
    ### Header, Categories and Processes ###
    space = " "*50
    hline = "-"*100 + "\n"
    
    card =  "imax *   number of channels\n"
    card += "jmax *   number of backgrounds\n"
    card += "kmax *   number of nuisance parameters\n"
    card += hline
    card += "bin        " + space + ("%-25s" % cat) + "\n"
    card += "observation" + space + ("%-25.0f" % -1.) + "\n"
    card += hline
    card += "shapes * * " + space + "rootfiles_"+options.name+"/$CHANNEL.root          $PROCESS          $SYSTEMATIC/$PROCESS\n"
    card += hline
    card += "bin        " + space
    for i, s in enumerate([sign] + back):
        card += "%-30s" % cat
    card += "\n"
    card += "process    " + space
    for i, s in enumerate([sign] + back):
        card += "%-30s" % s
    card += "\n"
    card += "process    " + space
    for i, s in enumerate([sign] + back):
        card += "%-30d" % i
    card += "\n"
    card += "rate       " + space
    for i, s in enumerate([sign] + back):
        card += "%-25.6f" % getNumber(cat, s) #-1.
    card += "\n"
    card += hline
    
    if verbose: print "  Header done, now shape uncertainties..."
    
    ### Systematic Uncertainties ###
    if verbose: print "  MC statistics..."
    # MC statistics
    #card += "* autoMCStats 0.1\n"
    
    # Shape
    if isShape:
        for i, h in enumerate(shape):
            card += "%-50s shape     " % h
            for i, s in enumerate([sign] + back):
#                    if i>0: card += ("%-20.1f" % 1)
#                    else: card += "%-25s" % "-"
                if not checkShape(cat, s, h): card += ("%-25.0f" % 1)
                else: card += "%-25s" % "-"
            card += "\n"
    
    # Cut&count++
    else:
        for i, h in enumerate(shape):
            card += "%-50s lnN       " % h
            for c in categories:
                for b in range(nbin[c] if not isShape else 1):
                    for i, s in enumerate([sign] + back): #
                        #print c, s, h, syst[c][s][h][1].GetBinContent(b+1)
                        if syst[c][s][h][0].GetBinContent(b+1) != 0:
                            up = max(min(syst[c][s][h][1].GetBinContent(b+1)/syst[c][s][h][0].GetBinContent(b+1), 2), 0.5)
                            down = max(min(syst[c][s][h][-1].GetBinContent(b+1)/syst[c][s][h][0].GetBinContent(b+1), 2), 0.5)
                            string = "%.3f/%.3f" % (up, down)
                        else:
                            string = "-"
                        card += "%-25s" % string
            card += "\n"
    
    if verbose: print "  Shapes done, now normalization..."
    
    # Normalization
    for k in sorted(norm.keys()):
        card += "%-50s lnN       " % k
        for i, s in enumerate([sign] + back):
            issyst = False
            for n, nn in norm[k].iteritems():
                if n in s and norm[k][n]>0:
                    #print "--test ", n, s, cat
                    #if k=='CMS_eff_met_trigger' and not cat.startswith('AH0l'): continue
                    if 'preFire_1f' in k and not('1f' in cat): continue
                    if 'preFire_2b' in k and not('2b' in cat): continue
                    if 'forwJet_SL' in k and not('SL' in cat and '1f' in cat): continue
                    if 'forwJet_AH' in k and not('AH' in cat and '1f' in cat): continue
                    if k=='pdf_accept_Z' and not('2m' in cat or '2e' in cat): continue
                    if k=='pdf_accept_2l_T' and not('1e1m' in cat or '2m' in cat or '2e' in cat): continue
                    if k=='pdf_accept_1l_T' and (not('1m' in cat or '1e' in cat) or ('1e1m' in cat)): continue
                    if k=='pdf_accept_W' and (not('1m' in cat or '1e' in cat) or ('1e1m' in cat)): continue
                    if k=='QCDScale_tDM' and ('ttDM' in s or 'tttDM' in s): continue
                    if k=='QCDScale_ttDM' and ('tttDM' in s or 'DM_MChi1_MPhi125_scalar' in s): continue
                    if k=='ttH_HToInv_xsec':
                        if 'DM_MChi1_MPhi125_scalar' in s:
                            card += ("%.3f/%-19.3f" % (norm[k][n][0], norm[k][n][1]))
                            continue
                        else:
                            continue
                    card += ("%-25.3f" % norm[k][n])
                    issyst = True
            if not issyst: card += "%-25s" % "-"
        card += "\n"
    
    if verbose: print "  Normalization done, now minor backgrounds..."
    
    # Free backgrounds
    for k in sorted(freenorm.keys()):
        if any([True for x in back if x in k]):
            card += "%-50s lnU       " % k
            for i, s in enumerate([sign] + back):
                if s in k: card += ("%-25.3f" % freenorm[k])
                else: card += "%-25s" % "-"
            card += "\n"
    

    if verbose: print "  Rate params..."
    for p, m in rateparam.iteritems():
        if (('AH' in cat and 'AH' in p) or ('SL' in cat and 'SL' in p)):
            if ("ZR" in cat and "ZR" in p):
                p= p.replace("_ZR","")
            elif ("ZR" in cat and "NuNu" in m): continue
            elif ("ZR" in p): continue

            if "bin" in cat:
                p = p + cat[cat.find("bin")+3:]

            #paper
            #print '--> p',p,'cat',cat,'m',m
            #card += "%-25s%-20s%-20s\t%-20s          1.   [0.1,2]\n" % (p, 'rateParam', cat, m, )
            card += "%-25s%-20s%-20s\t%-20s          1.   \n" % (p, 'rateParam', cat, m, )
            #print '--> rate ',"%-25s%-20s%-20s\t%-20s          1.   [0.1,2]\n" % (p, 'rateParam', cat, m, )
            #card += "%25s%20s          1.   0.9\n" % (p, 'aparam')
            #print '--> param',"%25s%20s          1.   0.9\n" % (p, 'param')
            #card += "%-25s%-20s%-20s\t%-20s          1.   [0.01,1.2]\n" % (p, 'rateParam', cat, m, )
            #card += "%-25s%-20s%-20s\t%-20s          1.  \n" % (p, 'rateParam', cat, m, )


    
    if verbose: print "  MC statistics..."
    # MC statistics
    ##paper
    card += "* autoMCStats 0.1\n"
    
    if verbose: print "  Done. Writing to file..."
    # Close rootfile
    #inFile.Close()
    
    # Write to file
    try: os.stat("datacards_"+options.name) 
    except: os.mkdir("datacards_"+options.name)
    #try: os.stat("/hdfs/store/user/vshang/datacards_"+options.name) 
    #except: os.mkdir("/hdfs/store/user/vshang/datacards_"+options.name)
    
    outname = "datacards_"+options.name+"/" + sign + '_' + cat + ".txt"
    #outname = "/hdfs/store/user/vshang/datacards_"+options.name+"/" + sign + '_' + cat + ".txt"
    cardfile = open(outname, 'w')
    cardfile.write(card)
    cardfile.close()
    print "Datacard for ", sign, "saved in", outname
    
    # Avoid closing the file, directly remove the TFile from internal list
    # https://root.cern.ch/phpBB3/viewtopic.php?t=14450
    #gROOT.GetListOfFiles().Remove(inFile)


def getNumber(cat, s, syst=''):
    f = TFile("rootfiles_"+options.name+"/"+cat+".root", "READ")
    h = f.Get((syst+'/' if len(syst)>0 else '')+s)
    if h==None: return -1
    n = h.Integral()
    f.Close()
    #print "In category", cat, "background", s, "has", n, "events"
    return n

def checkShape(cat, s, syst=''):
    f = TFile("rootfiles_"+options.name+"/"+cat+".root", "READ")
    h = f.Get(s)
    hUp = f.Get(syst+'Up'+'/'+s)
    hDown = f.Get(syst+'Down'+'/'+s)
    
    if h==None or hUp==None or hDown==None: 
        print "***** WARNING: sys hists do not exists!!"
        return False
    isSame = True
    
    if 'eff_e' in syst and 'm' in cat and '1e1m' not in cat: 
        return True
    if 'eff_m' in syst and 'e' in cat and '1e1m' not in cat: 
        return True
    if 'trig_e' in syst and 'm' in cat and '1e1m' not in cat: 
        return True
    if 'trig_m' in syst and 'e' in cat and '1e1m' not in cat: 
        return True
    if 'CMS_W' in syst and 'TTbar' in s:
        return True
    if 'CMS_Z' in syst and 'TTbar' in s:
        return True
    if 'CMS_pdf' in syst and 'DM' in s:
        return True
    if 'pdf_accept' in syst and 'DM' in s:
        return True
    if 'CMS_HF_Z' in syst and not(s.startswith('ZJ') or s.startswith('DYJets')):
        return True
    if 'CMS_HF_W' in syst and not(s.startswith('WJ')):
        return True
    if h.Integral()<1.e-20 or hUp.Integral()<1.e-20 or hDown.Integral()<1.e-20: 
        return True
    for i in range(h.GetNbinsX()):
        if not h.GetBinContent(i+1) > 0.: 
            continue
        if abs(hUp.GetBinContent(i+1)-h.GetBinContent(i+1))/h.GetBinContent(i+1) > 1.e-20 or abs(h.GetBinContent(i+1)-hDown.GetBinContent(i+1))/h.GetBinContent(i+1) > 1.e-20:
            isSame = False
            break
    f.Close()
    #if not isSame: print "systematic", syst,"for sample", s, "in cat", cat, "has been degraded"
    # if 'res' in syst or 'QCDscale' in syst:
    #     isSame = False
    return isSame

def fillLists():
    # List files and fill categories
    for c in os.listdir('rootfiles_'+options.name+'/'):
        if c.endswith('root'):
            categories.append(c.replace('.root', ''))
    
    # Read file and histograms
    inFile = TFile("rootfiles_"+options.name+"/"+categories[0]+".root", "READ")
    inFile.cd()
    for key in inFile.GetListOfKeys():
        obj = key.ReadObj()
        if obj.IsA().InheritsFrom("TH1"):
            name = obj.GetName()
            #if 'DM' in name:
            #if ('ttDM_' in name) and  ('tttDM' not in name) and ('scalar' in name):
            if ('tttDM_MChi1_MPhi100_scalar' in name):
            #if ('DM_MChi1_MPhi125_scalar' in name) or ('DM_MChi1_MPhi100_scalar' in name):
            #if ('DM_MChi1_MPhi125_scalar') in name or ('DM_MChi1_MPhi100_scalar' in name) or ('DM_MChi1_MPhi150_scalar' in name):
                sign.append( name )                
            ##paper
            #elif not "data_obs" in name and not "BkgSum" in name: back.append(name)
            #elif not "data_obs" in name and not "BkgSum" in name and not "TTTo2L2Nu" in name  and not "TTToSemiLepton" in name and not "TTV" in name and not "DM" in name: back.append(name)
            elif not "data_obs" in name and not "BkgSum" in name and not "TTbarSL" in name and not "DM" in name: back.append(name)
        # Categories (directories)
        if obj.IsFolder():
            subdir = obj.GetName()
            subdir = subdir.replace('Up', '').replace('Down', '')
            if not subdir in greenShape: continue
            if not subdir in shape: 
                shape.append(subdir)
    print 'filled shape ', shape
    inFile.Close()
        

fillLists()

print "Categories  :", categories
print "Signal      :", sign
print "Backgrounds :", back
print "Shape unc   :", shape


for cat in categories:
#    for s in sign[:1]: #for testing to just run one signal
    for s in sign:
        #if 'tttDM_MChi1_MPhi10_scalar' in s or 'tttDM_MChi1_MPhi100_scalar' in s:
        datacard(cat, s)

