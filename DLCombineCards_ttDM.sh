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


scp ../dilepton/cards/full_run2_scalar_ttDM.txt dilepton/cards/test/full_run2_scalar_ttDM.txt
scp ../dilepton/cards/full_run2_pseudo_ttDM.txt dilepton/cards/test/full_run2_pseudo_ttDM.txt
echo "Copied DL RunII datacards."

echo "Merging datacards..."
for card in ttDM*scalar*_RunII.txt
do
    if [[ "$card" == "ttDM_MChi1_MPhi125"* ]]; then
	continue
    fi
    combineCards.py AHSL=$card DL=dilepton/cards/test/full_run2_scalar_ttDM.txt > ${card/_RunII.txt/.txt}
    echo "done ${card/_RunII.txt/.txt}"
done

for card in ttDM*pseudo*_RunII.txt
do
    if [[ "$card" == "ttDM_MChi1_MPhi125"* ]]; then
	continue
    fi
    combineCards.py AHSL=$card DL=dilepton/cards/test/full_run2_pseudo_ttDM.txt > ${card/_RunII.txt/.txt}
    echo "done ${card/_RunII.txt/.txt}"
done

rm *_RunII.txt
cd ../

echo -e "\e[00;32mAll clear\e[00m"
