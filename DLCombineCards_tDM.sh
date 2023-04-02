#!/bin/bash

name=$1
RUNDIR="combinedCards_${name}_RunIIFull"

echo "Making full combination datacards (AH+SL+DL) for tDM..."

if [ ! -d "${RUNDIR}" ]; then 
    echo "using ${RUNDIR}"
    mkdir $RUNDIR
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
if [ ! -d "dilepton/cards/tDM/" ]; then 
    echo "Making DL directory..."
    if [ ! -d "dilepton/" ]; then
	mkdir dilepton
    fi
    cd dilepton
    mkdir cards
    cd cards
    mkdir tDM
    cd ../..
fi


scp ../dilepton/cards/tDM/full_run2_tDM_scalar.txt dilepton/cards/tDM/full_run2_tDM_scalar.txt
scp ../dilepton/cards/tDM/full_run2_tDM_pseudo.txt dilepton/cards/tDM/full_run2_tDM_pseudo.txt
echo "Copied DL RunII datacards."

echo "Merging datacards..."
for card in tDM*scalar*_RunII.txt
do
    if [[ "$card" == *"_MChi1_MPhi125"* ]]; then
	continue
    fi
    combineCards.py AHSL=$card DL=dilepton/cards/tDM/full_run2_tDM_scalar.txt > ${card/_RunII.txt/.txt}
    echo "done ${card/_RunII.txt/.txt}"
done

for card in tDM*pseudo*_RunII.txt
do
    if [[ "$card" == *"_MChi1_MPhi125"* ]]; then
	continue
    fi
    combineCards.py AHSL=$card DL=dilepton/cards/tDM/full_run2_tDM_pseudo.txt > ${card/_RunII.txt/.txt}
    echo "done ${card/_RunII.txt/.txt}"
done

rm *_RunII.txt
cd ../

echo -e "\e[00;32mAll clear\e[00m"
