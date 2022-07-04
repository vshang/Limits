dir=$1
name=$(basename $2 .txt)
read num1 mass num3 <<<${name//[^0-9]/ }
echo "$num1 / $num2"

#mass=125
echo 'mass' $mass

ulimit -s unlimited

#workspace
text2workspace.py -m $mass --channel-masks $dir/$name.txt -o $dir/$name.root

#Danyer's settings
# combineTool.py -M Impacts --expectSignal=0 --rMin -10 --rMax 10 -d $dir/$name.root -m $mass -t -1 --doInitialFit --robustFit 1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --X-rtd FITTER_NEW_CROSSING_ALGO --parallel 40
# combineTool.py -M Impacts --expectSignal=0 --rMin -10 --rMax 10 -d $dir/$name.root -m $mass -t -1 --robustFit 1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --X-rtd FITTER_NEW_CROSSING_ALGO --doFits --parallel 40
# combineTool.py -M Impacts -d $dir/$name.root -m $mass -o $dir/impacts_r0_$name.json
# plotImpacts.py -i $dir/impacts_r0_$name.json --cms-label Preliminary -o $dir/impacts_r0_$name
# pdftoppm -png -f 1 $dir/impacts_r0_$name.pdf $dir/impacts_r0_$name

#No constraint on r
# combineTool.py -M Impacts -d $dir/$name.root -m $mass -t -1 --doInitialFit --robustFit 1 --parallel 40 
# combineTool.py -M Impacts -d $dir/$name.root -m $mass -t -1 --robustFit 1 --doFits --parallel 40
# combineTool.py -M Impacts -d $dir/$name.root -m $mass -t -1 -o $dir/impacts_$name.json
# plotImpacts.py -i $dir/impacts_$name.json --cms-label Preliminary -o $dir/impacts_$name
# pdftoppm -png -f 1 $dir/impacts_$name.pdf $dir/impacts_$name

#r=0
combineTool.py -M Impacts --expectSignal=0  --rMin -10 --rMax 10 -d $dir/$name.root -m $mass -t -1 --doInitialFit --robustFit 1 --parallel 40 
combineTool.py -M Impacts --expectSignal=0  --rMin -10 --rMax 10 -d $dir/$name.root -m $mass -t -1 --robustFit 1 --doFits --parallel 40
combineTool.py -M Impacts --expectSignal=0  -d $dir/$name.root -m $mass -t -1 -o $dir/impacts_r0_$name.json
plotImpacts.py -i $dir/impacts_r0_$name.json --cms-label Preliminary -o $dir/impacts_r0_$name
pdftoppm -png -f 1 $dir/impacts_r0_$name.pdf $dir/impacts_r0_$name

# #r=1
# combineTool.py -M Impacts --expectSignal=1  -d $dir/$name.root -m $mass -t -1 --doInitialFit --robustFit 1 --parallel 40 
# combineTool.py -M Impacts --expectSignal=1  -d $dir/$name.root -m $mass -t -1 --robustFit 1 --doFits --parallel 40
# combineTool.py -M Impacts --expectSignal=1  -d $dir/$name.root -m $mass -t -1 -o $dir/impacts_r1_$name.json
# plotImpacts.py -i $dir/impacts_r1_$name.json --cms-label Preliminary -o $dir/impacts_r1_$name
# pdftoppm -png -f 1 $dir/impacts_r1_$name.pdf $dir/impacts_r1_$name


#impacts
#r0
# combineTool.py -M Impacts --doInitialFit -t -1 --rMin -10 --rMax 10 --expectSignal=0 --robustFit=1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --X-rtd FITTER_NEW_CROSSING_ALGO -m $mass -d $dir/$name.root
# combineTool.py -M Impacts --doFits -t -1 --rMin -10 --rMax 10 --expectSignal=0 --robustFit=1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --X-rtd FITTER_NEW_CROSSING_ALGO -m $mass -d $dir/$name.root
# combineTool.py -M Impacts --expectSignal=0 -o $dir/impacts_r0_$name.json -m $mass -d $dir/$name.root
# plotImpacts.py -i $dir/impacts_r0_$name.json --cms-label Preliminary -o $dir/impacts_r0_$name
# pdftoppm -png -f 1 $dir/impacts_r0_$name.pdf $dir/impacts_r0_$name
###
# text2workspace.py $dir/$name.txt -m $mass
# combine -M MultiDimFit -n _initialFit_Test --algo singles --redefineSignalPOIs r --robustFit 1 --mass $mass $option -d $dir/$name.root
# combineTool.py -M Impacts -d $dir/$name.root -m $mass -t -1 --doInitialFit --robustFit 1 --parallel 40
# combineTool.py -M Impacts -d $dir/$name.root -m $mass -t -1 --robustFit 1 --doFits --parallel 40
# combineTool.py -M Impacts -d $dir/$name.root -m $mass -t -1 -o $dir/impacts_$name.json
# plotImpacts.py -i $dir/impacts_$name.json --cms-label Preliminary -o $dir/impacts_$name
# pdftoppm -png -f 1 $dir/impacts_$name.pdf $dir/impacts_$name
