# Paleisti testavimo įrankį 

Paprasčiausias būdas paleisti cmd failą skirta tam tikrai paslaugai: pvz 

    paleisti_patikra.cmd

Gauti rezultatai:
    
	===================== Liepa Results Analysis =======================
        Engine: ieskotuvas
        Information on experiment: testas
        Date: 2015-02-15T17:30:44.465000
        Phrase transformation: phrases to function
        Audio signal length in 2053.645812s. Processed in 13.557s. Processing ratio 0.00660143045153
        Result file: None
        File Summary result file: None
        Additional noise added: 0.0
        Sphinx command sample: bin\pocketsphinx_continuous -fdict ./models/dict/.liepa.filler -hmm ./models/hmm/liepa-20_corpus8_0_mg11.cd_semi_200/ -jsgf ./models/lm/liepa_ieskotuvas.gram -dict ./models/dict/liepa_ieskotuvas.dic -infile  ***.wav
    ------------------------ Overall Results --------------------------
    COMMAND: %Corr=98.02, Acc=98.02 [H=494, D=3, S=7, I=0, N=504]
    ===================================================================


Daugiau parinkčių siūlantis būdas naudojantis wav_align.py įrankiu tiesiogiai. daugiau informacijos: 

    bin\tool\wav_align.py --help


Paleidimo pavyzdžiai:

    rem naudoja numatytose vietose esančiu standartinius failus paslaugos ieskotuvas patikrinimui
    bin\tool\wav_align.py --engine ieskotuvas
    rem papildomi nustatymai kokį akustinį modelį, gramatika ar žodyną naudoti
    bin\tool\wav_align.py --engine ieskotuvas --info "testas" --hmm liepa-20_corpus8_0_mg11.cd_semi_200 --jsgf liepa_ieskotuvas.gram --dict liepa_ieskotuvas.dic  --compare_function


# Katalogai  

	\bin - paleidžiamieji failai
	\bin\tool - python parašyti įrankiai: 
	\bin\tool\phrase2function.py - frazė vertimas į funkciją
	\bin\tool\phrase_align.py - atpažinimo ir traskcripcijos palyginimas(perrašytas sphinx word_align.pl)
	\bin\tool\transcriber_re.py - mg1.3 trasckribatorius(be UI)
	\bin\tool\wav_align.py - pagrindinis įrankis kuris naudoja visus kitus aukščiau paminėtus
	\models\lm - Paslaugų JSGF gramatikos
	\models\hmm - Sphinx Akustinis modelis
	\models\dict - Paslaugų žodynai
	\target - direktorija laikiniems failams: logams, rezultatams ir t.t.
	\wav - testavimo garsynų direktorija

# Noriu testuoti kitus atvejus 

 * Jei reikia pakeisti nustatymus kitus nei numatyta skripto parametrais, tuomet reikia keisti skripte esančią konstantą: wav_align.py POCKETSPHINX_CMD_TEMPLATE
 * Jei reikia pridėti daugiau akustinių modelių, tai įkelkite juos į katalogą: \models\hmm ir nusakykite skriptų jį naudoti parametru "--hmm mano_hmm". NB: Jei žodynas naudoją kitą fonemų aibę tuomet reikia naujo žodyno.
 * Jei reikia pridėti naują gramatiką esamoms paslaugom, tai įkelkite gramatiką į \models\lm ir nustatykite ją naudoti parametru --jsgf mano.gram. NB: Reikia užtikrinti kad visi gramatikos žodžiai yra žodyne.
 * Jei reikia naudoti naują žodyną esamoms paslaugom, tai įkelkite naują žodyną į \models\dict ir nustatykite jį naudoti parametru --dict mano.dict

