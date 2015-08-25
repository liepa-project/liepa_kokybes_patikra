#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re,sys
import phrase2function, phrase_align
import codecs
import multiphrasealiner

RESULT_REGEX = re.compile("(.*) \((.*) -\d*\)")
multiphrasealiner = multiphrasealiner.MultiPhraseAligner()




def compareResults(fileName, testList):
    '''
    Compare results
    '''
    txt_file_name = "wav/patikra/"+fileName + ".txt"
    print txt_file_name
    targetList = multiphrasealiner.extractTargetList(txt_file_name)
    wav_file_name = u"" + fileName + ".wav"
    #print u"{} => {}".format(targetList, testList)
    (file_match,file_substitution, file_deletion, file_insertion, file_target, file_rejection, hypothesisArr, refernceArr)=multiphrasealiner.compareRecogntionResults(wav_file_name, targetList, testList)
    multiphrasealiner.writeFileSummary(wav_file_name,file_match,file_substitution, file_deletion, file_insertion, file_target, file_rejection,hypothesisArr, refernceArr)
    return (file_match,file_substitution, file_deletion, file_insertion, file_target, file_rejection, hypothesisArr, refernceArr)

def loopHyp(hyp_file):
    sum_matched=0
    sum_substitution= 0 
    sum_deletion= 0 
    sum_insertion= 0
    sum_target = 0
    sum_length = 0
    hypothesis = []
    #with open(hyp_file, "rb") as infile:
    with codecs.open(hyp_file,'rb',encoding='utf8') as infile:
        hypothesis= infile.readlines()
    processingFileName = ""#RESULT_REGEX.search(hypothesis[0]).group(2)
    processingPhrases = []
    total_hyp = len(hypothesis)
    #for line in infile:
    for idx,line in enumerate(hypothesis):
        m = RESULT_REGEX.search(line)
        if not(m):
            continue
        phrase = m.group(1)
        fileName = m.group(2)
        phrase = phrase.strip()
        if processingFileName == "":
            processingFileName = fileName

        if fileName == processingFileName:
            pass
        else:
            (file_match,file_substitution, file_deletion, file_insertion, file_target, file_rejection, hypothesisArr, refernceArr) = compareResults(processingFileName, processingPhrases)
            sum_matched+=file_match
            sum_substitution += file_substitution
            sum_deletion += file_deletion
            sum_insertion += file_insertion
            sum_target += file_target
            processingPhrases=[]
            processingFileName=fileName
        #print u"{}: {}".format(fileName, phrase)
        progress=float(idx)/total_hyp
        sys.stdout.write("\rFiles processed: {:.2f}%".format(progress*100))
        sys.stdout.flush()
        if(len(phrase) > 0):
            processingPhrases.append(phrase.strip())

    (file_match,file_substitution, file_deletion, file_insertion, file_target, file_rejection, hypothesisArr, refernceArr) = compareResults(processingFileName, processingPhrases)
    sum_matched+=file_match
    sum_substitution += file_substitution
    sum_deletion += file_deletion
    sum_insertion += file_insertion
    sum_target += file_target
    total=float(sum_target)
    multiphrasealiner.createFinalResult(sum_matched, sum_substitution, sum_deletion, sum_insertion, sum_target,total)


def main():
    hyp_file = "target/patikra.match"
    loopHyp(hyp_file)
    
if __name__ == "__main__":
    main()
