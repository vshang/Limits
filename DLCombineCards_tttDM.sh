#!/bin/bash

name=$1
RUNDIR="combinedCards_${name}_RunIIFull"

echo "Making full combination datacards (AH+SL+DL) for tttDM..."

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
for card in tttDM*_ALL.txt
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


scp ../dilepton/cards/full_run2_scalar.txt dilepton/cards/test/full_run2_scalar.txt
scp ../dilepton/cards/full_run2_pseudo.txt dilepton/cards/test/full_run2_pseudo.txt
echo "Copied DL RunII datacards."

echo "Merging datacards..."
for card in tttDM*scalar*_RunII.txt
do
    if [[ "$card" == *"_MChi1_MPhi125"* ]]; then
	continue
    fi
    combineCards.py -S AHSL=$card DL=dilepton/cards/test/full_run2_scalar.txt > ${card/_RunII.txt/.txt}
    echo "done ${card/_RunII.txt/.txt}"
done

for card in tttDM*pseudo*_RunII.txt
do
    if [[ "$card" == *"_MChi1_MPhi125"* ]]; then
	continue
    fi
    combineCards.py -S AHSL=$card DL=dilepton/cards/test/full_run2_pseudo.txt > ${card/_RunII.txt/.txt}
    echo "done ${card/_RunII.txt/.txt}"
done

rm *_RunII.txt
cd ../

echo -e "\e[00;32mAll clear\e[00m"
