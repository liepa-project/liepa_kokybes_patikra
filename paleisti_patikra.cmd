@echo off

echo Paskaitykite informaciją faile README.txt

echo Segmentuojami garso įrašai rezultatai target\patikra.ctl. Laukite

bin\tool\segment_files.py > target\patikra.ctl

echo Segmentų atpažinimas. rezultatai target\patikra.match. Laukite


"bin\sphinx-20150402(r12906)-win32\pocketsphinx\bin\pocketsphinx_batch" ^
    -hmm bin/hmm/G20150114_EZ15_FZ1.3semi750-sph20141812 ^
    -jsgf bin/lm/liepa_patikra.gram ^
    -dict bin/dict/liepa_patikra.dic ^
    -backtrace yes ^
    -ctl target/patikra.ctl ^
    -adcin true ^
    -cepext .wav ^
    -cepdir wav/patikra ^
    -hyp target/patikra.match ^
    > target/patikra_batch.log 2>&1

bin\tool\match_align.py

echo Rezultatai: target/patikra_results.txt
pause
