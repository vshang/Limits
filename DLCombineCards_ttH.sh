#!/bin/bash

name=$1
RUNDIR="combinedCards_${name}_RunIIFull"

if [ ! -d "${RUNDIR}" ]; then 
    echo "using ${RUNDIR}"
    mkdir $RUNDIR
fi

echo "Copying datacards..."
cd combinedCards_${name}_RunII
for card in ttDM_MChi1_MPhi125_scalar*_ALL.txt
do
    scp $card ../${RUNDIR}/${card/.txt/_RunII.txt}
done
echo "Copied AH+SL RunII datacards."

cd ../$RUNDIR
if [ ! -d "dilepton/ttH_inv_cards/" ]; then 
    echo "Making DL directory..."
    if [ ! -d "dilepton/" ]; then
	mkdir dilepton
    fi
    cd dilepton
    mkdir ttH_inv_cards
    cd ..
fi

scp ../dilepton/ttH_inv_cards/full_run2_scalar.txt dilepton/ttH_inv_cards/full_run2_scalar.txt
echo "Copied DL RunII datacards."

echo "Merging datacards..."
for card in ttDM_MChi1_MPhi125_scalar*_RunII.txt
do
    combineCards.py AHSL=$card DL=dilepton/ttH_inv_cards/full_run2_scalar.txt > ${card/_RunII.txt/.txt}
    echo "done ${card/_RunII.txt/.txt}"
done

rm *_RunII.txt
cd ../

echo -e "\e[00;32mAll clear\e[00m"
