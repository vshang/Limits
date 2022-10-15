#!/bin/bash  

dir='combinedCards_ModuleCommonSkim_06102022_RunIIFull'
name='ttDM_MChi1_MPhi125_scalar1b2b_ALL'
mass='125'

ulimit -s unlimited

# text2workspace.py  $dir/$name.txt $dir/$name.root channel-masks

### Fitting ###
combine -M FitDiagnostics --datacard $dir/$name.root --expectSignal=0 --saveNormalizations --saveShapes --saveWithUncertainties --saveNLL  -n _$name -m $mass --robustFit=1 --setParameters mask_run16_SL1l0fT1SRbin_250_290=1,mask_run16_SL1l0fT1SRbin_290_330=1,mask_run16_SL1l0fT1SRbin_330_370=1,mask_run16_SL1l0fT1SRbin_370_410=1,mask_run16_SL1l0fT1SRbin_410_450=1,mask_run16_SL1l0fT1SRbin_450_490=1,mask_run16_SL1l0fT1SRbin_490_530=1,mask_run16_SL1l0fT2SRbin_250_290=1,mask_run16_SL1l0fT2SRbin_290_330=1,mask_run16_SL1l0fT2SRbin_330_370=1,mask_run16_SL1l0fT2SRbin_370_410=1,mask_run16_SL1l0fT2SRbin_410_450=1,mask_run16_SL1l0fT2SRbin_450_490=1,mask_run16_SL1l0fT2SRbin_490_530=1,mask_run16_SL1l0fT3SRbin_250_290=1,mask_run16_SL1l0fT3SRbin_290_330=1,mask_run16_SL1l0fT3SRbin_330_370=1,mask_run16_SL1l0fT3SRbin_370_410=1,mask_run16_SL1l0fT3SRbin_410_450=1,mask_run16_SL1l0fT3SRbin_450_490=1,mask_run16_SL1l0fT3SRbin_490_530=1,mask_run16_SL1l1fT1SRbin_250_290=1,mask_run16_SL1l1fT1SRbin_290_330=1,mask_run16_SL1l1fT1SRbin_330_370=1,mask_run16_SL1l1fT1SRbin_370_410=1,mask_run16_SL1l1fT1SRbin_410_450=1,mask_run16_SL1l1fT1SRbin_450_490=1,mask_run16_SL1l1fT1SRbin_490_530=1,mask_run16_SL1l1fT2SRbin_250_290=1,mask_run16_SL1l1fT2SRbin_290_330=1,mask_run16_SL1l1fT2SRbin_330_370=1,mask_run16_SL1l1fT2SRbin_370_410=1,mask_run16_SL1l1fT2SRbin_410_450=1,mask_run16_SL1l1fT2SRbin_450_490=1,mask_run16_SL1l1fT2SRbin_490_530=1,mask_run16_SL1l1fT3SRbin_250_290=1,mask_run16_SL1l1fT3SRbin_290_330=1,mask_run16_SL1l1fT3SRbin_330_370=1,mask_run16_SL1l1fT3SRbin_370_410=1,mask_run16_SL1l1fT3SRbin_410_450=1,mask_run16_SL1l1fT3SRbin_450_490=1,mask_run16_SL1l1fT3SRbin_490_530=1,mask_run16_SL1l2bT1SRbin_250_290=1,mask_run16_SL1l2bT1SRbin_290_330=1,mask_run16_SL1l2bT1SRbin_330_370=1,mask_run16_SL1l2bT1SRbin_370_410=1,mask_run16_SL1l2bT1SRbin_410_450=1,mask_run16_SL1l2bT1SRbin_450_490=1,mask_run16_SL1l2bT1SRbin_490_530=1,mask_run16_SL1l2bT2SRbin_250_290=1,mask_run16_SL1l2bT2SRbin_290_330=1,mask_run16_SL1l2bT2SRbin_330_370=1,mask_run16_SL1l2bT2SRbin_370_410=1,mask_run16_SL1l2bT2SRbin_410_450=1,mask_run16_SL1l2bT2SRbin_450_490=1,mask_run16_SL1l2bT2SRbin_490_530=1,mask_run16_SL1l2bT3SRbin_250_290=1,mask_run16_SL1l2bT3SRbin_290_330=1,mask_run16_SL1l2bT3SRbin_330_370=1,mask_run16_SL1l2bT3SRbin_370_410=1,mask_run16_SL1l2bT3SRbin_410_450=1,mask_run16_SL1l2bT3SRbin_450_490=1,mask_run16_SL1l2bT3SRbin_490_530=1,mask_run17_SL1l0fT1SRbin_250_290=1,mask_run17_SL1l0fT1SRbin_290_330=1,mask_run17_SL1l0fT1SRbin_330_370=1,mask_run17_SL1l0fT1SRbin_370_410=1,mask_run17_SL1l0fT1SRbin_410_450=1,mask_run17_SL1l0fT1SRbin_450_490=1,mask_run17_SL1l0fT1SRbin_490_530=1,mask_run17_SL1l0fT2SRbin_250_290=1,mask_run17_SL1l0fT2SRbin_290_330=1,mask_run17_SL1l0fT2SRbin_330_370=1,mask_run17_SL1l0fT2SRbin_370_410=1,mask_run17_SL1l0fT2SRbin_410_450=1,mask_run17_SL1l0fT2SRbin_450_490=1,mask_run17_SL1l0fT2SRbin_490_530=1,mask_run17_SL1l0fT3SRbin_250_290=1,mask_run17_SL1l0fT3SRbin_290_330=1,mask_run17_SL1l0fT3SRbin_330_370=1,mask_run17_SL1l0fT3SRbin_370_410=1,mask_run17_SL1l0fT3SRbin_410_450=1,mask_run17_SL1l0fT3SRbin_450_490=1,mask_run17_SL1l0fT3SRbin_490_530=1,mask_run17_SL1l1fT1SRbin_250_290=1,mask_run17_SL1l1fT1SRbin_290_330=1,mask_run17_SL1l1fT1SRbin_330_370=1,mask_run17_SL1l1fT1SRbin_370_410=1,mask_run17_SL1l1fT1SRbin_410_450=1,mask_run17_SL1l1fT1SRbin_450_490=1,mask_run17_SL1l1fT1SRbin_490_530=1,mask_run17_SL1l1fT2SRbin_250_290=1,mask_run17_SL1l1fT2SRbin_290_330=1,mask_run17_SL1l1fT2SRbin_330_370=1,mask_run17_SL1l1fT2SRbin_370_410=1,mask_run17_SL1l1fT2SRbin_410_450=1,mask_run17_SL1l1fT2SRbin_450_490=1,mask_run17_SL1l1fT2SRbin_490_530=1,mask_run17_SL1l1fT3SRbin_250_290=1,mask_run17_SL1l1fT3SRbin_290_330=1,mask_run17_SL1l1fT3SRbin_330_370=1,mask_run17_SL1l1fT3SRbin_370_410=1,mask_run17_SL1l1fT3SRbin_410_450=1,mask_run17_SL1l1fT3SRbin_450_490=1,mask_run17_SL1l1fT3SRbin_490_530=1,mask_run17_SL1l2bT1SRbin_250_290=1,mask_run17_SL1l2bT1SRbin_290_330=1,mask_run17_SL1l2bT1SRbin_330_370=1,mask_run17_SL1l2bT1SRbin_370_410=1,mask_run17_SL1l2bT1SRbin_410_450=1,mask_run17_SL1l2bT1SRbin_450_490=1,mask_run17_SL1l2bT1SRbin_490_530=1,mask_run17_SL1l2bT2SRbin_250_290=1,mask_run17_SL1l2bT2SRbin_290_330=1,mask_run17_SL1l2bT2SRbin_330_370=1,mask_run17_SL1l2bT2SRbin_370_410=1,mask_run17_SL1l2bT2SRbin_410_450=1,mask_run17_SL1l2bT2SRbin_450_490=1,mask_run17_SL1l2bT2SRbin_490_530=1,mask_run17_SL1l2bT3SRbin_250_290=1,mask_run17_SL1l2bT3SRbin_290_330=1,mask_run17_SL1l2bT3SRbin_330_370=1,mask_run17_SL1l2bT3SRbin_370_410=1,mask_run17_SL1l2bT3SRbin_410_450=1,mask_run17_SL1l2bT3SRbin_450_490=1,mask_run17_SL1l2bT3SRbin_490_530=1,mask_run18_SL1l0fT1SRbin_250_290=1,mask_run18_SL1l0fT1SRbin_290_330=1,mask_run18_SL1l0fT1SRbin_330_370=1,mask_run18_SL1l0fT1SRbin_370_410=1,mask_run18_SL1l0fT1SRbin_410_450=1,mask_run18_SL1l0fT1SRbin_450_490=1,mask_run18_SL1l0fT1SRbin_490_530=1,mask_run18_SL1l0fT2SRbin_250_290=1,mask_run18_SL1l0fT2SRbin_290_330=1,mask_run18_SL1l0fT2SRbin_330_370=1,mask_run18_SL1l0fT2SRbin_370_410=1,mask_run18_SL1l0fT2SRbin_410_450=1,mask_run18_SL1l0fT2SRbin_450_490=1,mask_run18_SL1l0fT2SRbin_490_530=1,mask_run18_SL1l0fT3SRbin_250_290=1,mask_run18_SL1l0fT3SRbin_290_330=1,mask_run18_SL1l0fT3SRbin_330_370=1,mask_run18_SL1l0fT3SRbin_370_410=1,mask_run18_SL1l0fT3SRbin_410_450=1,mask_run18_SL1l0fT3SRbin_450_490=1,mask_run18_SL1l0fT3SRbin_490_530=1,mask_run18_SL1l1fT1SRbin_250_290=1,mask_run18_SL1l1fT1SRbin_290_330=1,mask_run18_SL1l1fT1SRbin_330_370=1,mask_run18_SL1l1fT1SRbin_370_410=1,mask_run18_SL1l1fT1SRbin_410_450=1,mask_run18_SL1l1fT1SRbin_450_490=1,mask_run18_SL1l1fT1SRbin_490_530=1,mask_run18_SL1l1fT2SRbin_250_290=1,mask_run18_SL1l1fT2SRbin_290_330=1,mask_run18_SL1l1fT2SRbin_330_370=1,mask_run18_SL1l1fT2SRbin_370_410=1,mask_run18_SL1l1fT2SRbin_410_450=1,mask_run18_SL1l1fT2SRbin_450_490=1,mask_run18_SL1l1fT2SRbin_490_530=1,mask_run18_SL1l1fT3SRbin_250_290=1,mask_run18_SL1l1fT3SRbin_290_330=1,mask_run18_SL1l1fT3SRbin_330_370=1,mask_run18_SL1l1fT3SRbin_370_410=1,mask_run18_SL1l1fT3SRbin_410_450=1,mask_run18_SL1l1fT3SRbin_450_490=1,mask_run18_SL1l1fT3SRbin_490_530=1,mask_run18_SL1l2bT1SRbin_250_290=1,mask_run18_SL1l2bT1SRbin_290_330=1,mask_run18_SL1l2bT1SRbin_330_370=1,mask_run18_SL1l2bT1SRbin_370_410=1,mask_run18_SL1l2bT1SRbin_410_450=1,mask_run18_SL1l2bT1SRbin_450_490=1,mask_run18_SL1l2bT1SRbin_490_530=1,mask_run18_SL1l2bT2SRbin_250_290=1,mask_run18_SL1l2bT2SRbin_290_330=1,mask_run18_SL1l2bT2SRbin_330_370=1,mask_run18_SL1l2bT2SRbin_370_410=1,mask_run18_SL1l2bT2SRbin_410_450=1,mask_run18_SL1l2bT2SRbin_450_490=1,mask_run18_SL1l2bT2SRbin_490_530=1,mask_run18_SL1l2bT3SRbin_250_290=1,mask_run18_SL1l2bT3SRbin_290_330=1,mask_run18_SL1l2bT3SRbin_330_370=1,mask_run18_SL1l2bT3SRbin_370_410=1,mask_run18_SL1l2bT3SRbin_410_450=1,mask_run18_SL1l2bT3SRbin_450_490=1,mask_run18_SL1l2bT3SRbin_490_530=1,mask_run16_SL1l0fT1SRbin_250_290=1,mask_run16_SL1l0fT1SRbin_290_330=1,mask_run16_SL1l0fT1SRbin_330_370=1,mask_run16_SL1l0fT1SRbin_370_410=1,mask_run16_SL1l0fT1SRbin_410_450=1,mask_run16_SL1l0fT1SRbin_450_490=1,mask_run16_SL1l0fT1SRbin_490_530=1,mask_run16_SL1l0fT2SRbin_250_290=1,mask_run16_SL1l0fT2SRbin_290_330=1,mask_run16_SL1l0fT2SRbin_330_370=1,mask_run16_SL1l0fT2SRbin_370_410=1,mask_run16_SL1l0fT2SRbin_410_450=1,mask_run16_SL1l0fT2SRbin_450_490=1,mask_run16_SL1l0fT2SRbin_490_530=1,mask_run16_SL1l0fT3SRbin_250_290=1,mask_run16_SL1l0fT3SRbin_290_330=1,mask_run16_SL1l0fT3SRbin_330_370=1,mask_run16_SL1l0fT3SRbin_370_410=1,mask_run16_SL1l0fT3SRbin_410_450=1,mask_run16_SL1l0fT3SRbin_450_490=1,mask_run16_SL1l0fT3SRbin_490_530=1,mask_run16_SL1l1fT1SRbin_250_290=1,mask_run16_SL1l1fT1SRbin_290_330=1,mask_run16_SL1l1fT1SRbin_330_370=1,mask_run16_SL1l1fT1SRbin_370_410=1,mask_run16_SL1l1fT1SRbin_410_450=1,mask_run16_SL1l1fT1SRbin_450_490=1,mask_run16_SL1l1fT1SRbin_490_530=1,mask_run16_SL1l1fT2SRbin_250_290=1,mask_run16_SL1l1fT2SRbin_290_330=1,mask_run16_SL1l1fT2SRbin_330_370=1,mask_run16_SL1l1fT2SRbin_370_410=1,mask_run16_SL1l1fT2SRbin_410_450=1,mask_run16_SL1l1fT2SRbin_450_490=1,mask_run16_SL1l1fT2SRbin_490_530=1,mask_run16_SL1l1fT3SRbin_250_290=1,mask_run16_SL1l1fT3SRbin_290_330=1,mask_run16_SL1l1fT3SRbin_330_370=1,mask_run16_SL1l1fT3SRbin_370_410=1,mask_run16_SL1l1fT3SRbin_410_450=1,mask_run16_SL1l1fT3SRbin_450_490=1,mask_run16_SL1l1fT3SRbin_490_530=1,mask_run16_SL1l2bT1SRbin_250_290=1,mask_run16_SL1l2bT1SRbin_290_330=1,mask_run16_SL1l2bT1SRbin_330_370=1,mask_run16_SL1l2bT1SRbin_370_410=1,mask_run16_SL1l2bT1SRbin_410_450=1,mask_run16_SL1l2bT1SRbin_450_490=1,mask_run16_SL1l2bT1SRbin_490_530=1,mask_run16_SL1l2bT2SRbin_250_290=1,mask_run16_SL1l2bT2SRbin_290_330=1,mask_run16_SL1l2bT2SRbin_330_370=1,mask_run16_SL1l2bT2SRbin_370_410=1,mask_run16_SL1l2bT2SRbin_410_450=1,mask_run16_SL1l2bT2SRbin_450_490=1,mask_run16_SL1l2bT2SRbin_490_530=1,mask_run16_SL1l2bT3SRbin_250_290=1,mask_run16_SL1l2bT3SRbin_290_330=1,mask_run16_SL1l2bT3SRbin_330_370=1,mask_run16_SL1l2bT3SRbin_370_410=1,mask_run16_SL1l2bT3SRbin_410_450=1,mask_run16_SL1l2bT3SRbin_450_490=1,mask_run16_SL1l2bT3SRbin_490_530=1


mv -f fitDiagnostics_$name.root $dir

python $CMSSW_8_0_26_patch1/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py $dir/fitDiagnostics_$name.root --vtol=0.0000001  --histograms=$dir/pulls_$name.root

 
