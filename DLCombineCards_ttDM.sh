#!/bin/bash

name=$1
RUNDIR="combinedCards_${name}_RunIIFull"

echo "Making full combination datacards (AH+SL+DL) for ttDM..."

if [ ! -d "${RUNDIR}" ]; then 
    echo "using ${RUNDIR}"
    mkdir $RUNDIR
fi

echo "Copying datacards..."
cd combinedCards_${name}_RunII
for card in ttDM*_ALL.txt
do
    if [[ "$card" == "ttDM_MChi1_MPhi125"* ]]; then
	continue
    fi
    scp $card ../${RUNDIR}/${card/.txt/_RunII.txt}
done
echo "Copied AH+SL RunII datacards."

cd ../$RUNDIR
if [ ! -d "dilepton/cards/ttDM/" ]; then 
    echo "Making DL directory..."
    if [ ! -d "dilepton/" ]; then
	mkdir dilepton
    fi
    cd dilepton
    mkdir cards
    cd cards
    mkdir ttDM
    cd ../..
fi


scp ../dilepton/cards/ttDM/full_run2_ttDM_scalar.txt dilepton/cards/ttDM/full_run2_ttDM_scalar.txt
scp ../dilepton/cards/ttDM/full_run2_ttDM_pseudo.txt dilepton/cards/ttDM/full_run2_ttDM_pseudo.txt
echo "Copied DL RunII datacards."

echo "Merging datacards..."
for card in ttDM*scalar*_RunII.txt
do
    if [[ "$card" == "ttDM_MChi1_MPhi125"* ]]; then
	continue
    fi
    combineCards.py AHSL=$card DL=dilepton/cards/ttDM/full_run2_ttDM_scalar.txt > ${card/_RunII.txt/.txt}
    echo "done ${card/_RunII.txt/.txt}"
done

for card in ttDM*pseudo*_RunII.txt
do
    if [[ "$card" == "ttDM_MChi1_MPhi125"* ]]; then
	continue
    fi
    combineCards.py AHSL=$card DL=dilepton/cards/ttDM/full_run2_ttDM_pseudo.txt > ${card/_RunII.txt/.txt}
    echo "done ${card/_RunII.txt/.txt}"
done

rm *_RunII.txt
cd ../

echo -e "\e[00;32mAll clear\e[00m"
