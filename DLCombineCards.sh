#!/bin/bash

name=$1
RUNDIR="combinedCards_${name}_RunIIFull"

if [ ! -d "${RUNDIR}" ]; then 
    echo "using ${RUNDIR}"
    mkdir $RUNDIR
fi

echo "Copying datacards..."
cd combinedCards_${name}_RunII
for card in tt*_ALL.txt
do
    scp $card ../${RUNDIR}/${card/.txt/_RunII.txt}
done
echo "Copied AH+SL RunII datacards."

cd ../$RUNDIR
if [ ! -d "dilepton/cards/test/" ]; then 
    echo "Making DL directory..."
    mkdir dilepton
    cd dilepton
    mkdir cards
    cd cards
    mkdir test
    cd ../..
fi

# if [ ! -d "dilepton/ttH_inv_cards/" ]; then 
#     echo "Making DL directory..."
#     mkdir dilepton
#     cd dilepton
#     mkdir ttH_inv_cards
#     cd ..
# fi


scp ../dilepton/cards/full_run2_scalar_ttDM.txt dilepton/cards/test/full_run2_scalar_ttDM.txt
scp ../dilepton/cards/full_run2_pseudo_ttDM.txt dilepton/cards/test/full_run2_pseudo_ttDM.txt
# scp ../dilepton/ttH_inv_cards/full_run2_scalar.txt dilepton/ttH_inv_cards/full_run2_scalar.txt
echo "Copied DL RunII datacards."

echo "Merging datacards..."
for card in tt*scalar*_RunII.txt
do
    combineCards.py AHSL=$card DL=dilepton/cards/test/full_run2_scalar_ttDM.txt > ${card/_RunII.txt/.txt}
    echo "done ${card/_RunII.txt/.txt}"
done

for card in tt*pseudo*_RunII.txt
do
    combineCards.py AHSL=$card DL=dilepton/cards/test/full_run2_pseudo_ttDM.txt > ${card/_RunII.txt/.txt}
    echo "done ${card/_RunII.txt/.txt}"
done

# for card in tt*scalar*_RunII.txt
# do
#     combineCards.py AHSL=$card DL=dilepton/ttH_inv_cards/full_run2_scalar.txt > ${card/_RunII.txt/.txt}
#     echo "done ${card/_RunII.txt/.txt}"
# done

rm *_RunII.txt
cd ../

echo -e "\e[00;32mAll clear\e[00m"
