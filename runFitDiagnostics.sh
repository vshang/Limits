dir=$1
name=$(basename $1 .root)
read num1 mass num2 <<<${name//[^0-9]/ }
echo 'using dir: ' $dir
echo "$num1 / $num2"
echo 'mass' $mass

ulimit -s unlimited

combine -M FitDiagnostics --saveNormalizations --saveShapes --saveWithUncertainties --robustFit=1 --forceRecreateNLL --rMin=-5 --rMax=5 --out=. -m $mass -d $dir --cminDefaultMinimizerStrategy=0 --ignoreCovWarning
