#!/bin/bash

# How to run:
# source combineTest_ws.sh dir nameFile 

option="" 
#option="--freezeNuisanceGroups=shape2"
#option="-t -1" # Asimov dataset
#option="--freezeNuisanceGroups=theory"
#option="--freezeNuisanceGroups=theory  --minimizerAlgo=Minuit2 --minimizerStrategy=2"

dir=$1
#cp $1 $dir
name=$(basename $2 .txt)
mass=$(echo $name | tr -dc '0-9')

ulimit -s unlimited
#text2workspace.py $dir/$name.txt --channel-masks
combine -M FitDiagnostics -t -1 --datacard $dir/$name.root --saveShapes --expectSignal=0 --saveOverallShapes --saveNormalizations  $option --keepFailures -n _$name 
#combine -M FitDiagnostics --datacard $dir/$name.root --saveShapes --expectSignal=0 --saveOverallShapes --saveWithUncertainties --saveNormalizations  $option --keepFailures -n _$name #| grep Best # -t -1 generates errors 

mv -f fitDiagnostics_$name.root $dir # --plots

python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py --vtol=0.0000001 -f text $dir/fitDiagnostics_$name.root | sed -e 's/!/ /g' -e 's/,/ /g' | tail -n +2 > $dir/pulls_$name.txt # -g rootfiles/pull_$1$2\_M$3.root
sed -i -e 1,2d $dir/pulls_$name.txt
python pulls.py -b -f $dir/pulls_$name.txt -o $dir/pulls_$name

# To derive Impacts (https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsWG/SWGuideNonStandardCombineUses#Nuisance_parameter_impacts):
# text2workspace.py $dir/$name.txt # produces .root file in the same directory of the datacard
# combine -M MultiDimFit -n _initialFit_Test --algo singles --redefineSignalPOIs r --robustFit 1 --mass $mass $option -d $dir/$name.root
# combineTool.py -M Impacts -d $dir/$name.root --mass $mass --robustFit 1 --doFits --parallel 36
# combineTool.py -M Impacts -d $dir/$name.root --mass $mass -o $dir/impacts_$name.json
# plotImpacts.py -i $dir/impacts_$name.json --cms-label Preliminary -o $dir/impacts_$name # --transparent --color-groups 1,8,9,39,2
# pdftoppm -png -f 1 $dir/impacts_$name.pdf $dir/impacts_$name

## Clean
wait

#rm $dir/pulls_$name.txt $dir/$name.txt # $dir/fitDiagnostics_$name.root
#rm $dir/impacts_$name.json $dir/$name.root
#rm higgsCombine*.root
#rm roostats-*
#rm fitDiagnostics*.root

echo -e "\e[00;32mAll clear\e[00m"

# combine -M HybridNew --frequentist --datacard datacards/dijet/XVHah_M2600.txt --significance -H ProfileLikelihood --fork 32 -T 2000 -i 3

# python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/leeFromUpcrossings.py bands.root graph 1000 4500 --fit=best
