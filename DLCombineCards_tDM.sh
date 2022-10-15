#!/bin/bash

name=$1
RUNDIR="combinedCards_${name}_RunIIFull"

echo "Making full combination datacards (AH+SL+DL) for tDM..."

if [ ! -d "${RUNDIR}" ]; then 
    echo "using ${RUNDIR}"
    mkdir $RUNDIR
fi

if [ ! -d "dilepton/cards/test/" ]; then 
    echo "Adding test directory to dilepton/cards..."
    mkdir dilepton/cards/test
fi

echo "Copying datacards..."
cd combinedCards_${name}_RunII
for card in tDM*_ALL.txt
do
    if [[ "$card" == *"_MChi1_MPhi125"* ]]; then
	continue
    fi
    scp $card ../${RUNDIR}/${card/.txt/_RunII.txt}
done
echo "Copied AH+SL RunII datacards."

cd ../$RUNDIR
if [ ! -d "dilepton/cards/test/" ]; then 
    echo "Making DL directory..."
    if [ ! -d "dilepton/" ]; then
	mkdir dilepton
    fi
    cd dilepton
    mkdir cards
    cd cards
    mkdir test
    cd ../..
fi


scp ../dilepton/cards/full_run2_scalar_tDM.txt dilepton/cards/test/full_run2_scalar_tDM.txt
scp ../dilepton/cards/full_run2_pseudo_tDM.txt dilepton/cards/test/full_run2_pseudo_tDM.txt
echo "Copied DL RunII datacards."

echo "Merging datacards..."
for card in tDM*scalar*_RunII.txt
do
    if [[ "$card" == *"_MChi1_MPhi125"* ]]; then
	continue
    fi
    combineCards.py AHSL=$card DL=dilepton/cards/test/full_run2_scalar_tDM.txt > ${card/_RunII.txt/.txt}
    echo "done ${card/_RunII.txt/.txt}"
done

for card in tDM*pseudo*_RunII.txt
do
    if [[ "$card" == *"_MChi1_MPhi125"* ]]; then
	continue
    fi
    combineCards.py AHSL=$card DL=dilepton/cards/test/full_run2_pseudo_tDM.txt > ${card/_RunII.txt/.txt}
    echo "done ${card/_RunII.txt/.txt}"
done

rm *_RunII.txt
cd ../

echo -e "\e[00;32mAll clear\e[00m"
