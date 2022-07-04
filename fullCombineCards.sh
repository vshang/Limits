#!/bin/bash

name=$1
RUNDIR="combinedCards_${name}_RunII"

if [ ! -d "${RUNDIR}" ]; then 
    echo "using ${RUNDIR}"
    mkdir $RUNDIR
fi

echo "Copying datacards..."
cd combinedCards_${name}_2016
for card in *tDM*.txt
do
    scp $card ../${RUNDIR}/${card/.txt/_2016.txt}
done
echo "Copied 2016 datacards."

cd ../combinedCards_${name}_2017
for card in *tDM*.txt
do
    scp $card ../${RUNDIR}/${card/.txt/_2017.txt}
done
echo "Copied 2017 datacards."

cd ../combinedCards_${name}_2018
for card in *tDM*.txt
do
    scp $card ../${RUNDIR}/${card/.txt/_2018.txt}
done
echo "Copied 2018 datacards."

cd ../$RUNDIR

echo Merging datacards...
for card in *tDM*_2016.txt
do
    combineCards.py run16=$card run17=${card/_2016.txt/_2017.txt} run18=${card/_2016.txt/_2018.txt} > ${card/_2016.txt/.txt}
    echo "done ${card/_2016.txt/.txt}"

done

rm *_2016.txt
rm *_2017.txt
rm *_2018.txt
cd ../

echo -e "\e[00;32mAll clear\e[00m"

