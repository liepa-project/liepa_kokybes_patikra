#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
import phrase_align, phrase2function
import uuid, logging, logging.config



TMP_DIR="./target"
experiment_uuid=str(uuid.uuid1())

if not os.path.exists(TMP_DIR):
    os.makedirs(TMP_DIR)

logging.config.dictConfig({
    'version': 1,              
    'disable_existing_loggers': False,  # this fixes the problem

    'formatters': {
        'simple': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        "console": {
            "class": "logging.StreamHandler",
            "level": "ERROR",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },
        "info_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "simple",
            "filename": TMP_DIR+'/batch_aligner_'+experiment_uuid+'.log',
            "maxBytes": 10485760,
            "backupCount": 20,
            "encoding": "utf8"
        },
    },
    'loggers': {
        '': {                  
            'handlers': ['console'],        
            'level': 'ERROR',  
            'propagate': True  
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "info_file_handler"]
    }
})

LOG = logging.getLogger(__name__)




class MultiPhraseAligner:
    def __init__(self):
        self.aligner = phrase_align.PhraseAligner()
        self.phraseTransformer = phrase2function.NopTransformer()
        self.output_result = "./target/patikra.csv"
        self.file_result = "./target/patikra_results.txt"
        
        
    def writeComparisonMessage(self, wav_file_name, hypotesis, reference, match, insertion, deletion, substitution, rejection):
        '''
            write message to file using CSV format(more semicolon SSV).
        '''
        if not self.output_result: 
            return        
        baseName = os.path.basename(wav_file_name)
        baseName = os.path.splitext(baseName)[0]
        baseDirName = os.path.basename(os.path.dirname(wav_file_name ))

        message=u"{hypotesis};{reference};{match};{insertion};{deletion};{substitution};{rejection};{baseName};{baseDirName}\n".format(hypotesis=hypotesis,
          reference=reference, match=match, insertion=insertion, deletion=deletion, substitution=substitution, rejection=rejection,baseName=baseName, baseDirName=baseDirName)
        
        #print ">>>> [writeComparisonMessage]" + message
        
        with codecs.open(self.output_result,'a',encoding='utf8') as f: f.write(message)
        
        
    def writeFileSummary(self, wav_file_name,file_match,file_substitution, file_deletion, file_insertion, file_target, file_rejection,hypothesisArr, refernceArr):
        '''
        prints to given file agregated recongnition information 
        '''
        if not self.file_result:
            return
        baseName = os.path.basename(wav_file_name)
        baseName = os.path.splitext(baseName)[0]

        total=float(file_target)
        correct= ((file_target - file_deletion - file_substitution)/total)*100.0
        accuracy= ((file_target - file_deletion - file_substitution - file_insertion)/total)*100

        message=u"{wav_file_name}:{correct:6.2f}({accuracy:6.2f})  [H={matched:3}, D={deletion:3}, S={substitution:3}, I={insertion:3}, N={target:3}]\n".format(
            wav_file_name= baseName,correct=correct,accuracy=accuracy,matched=file_match,deletion=file_deletion, substitution=file_substitution,
                insertion=file_insertion,target=file_target)
        
        #print ">>>> [writeFileSummary]: " + message
        
        LOG.info("[writeFileSummary]" +  message)
        if not (file_match+file_deletion+file_substitution)== file_target:
            raise Exception("Results does not match. see log. guid:" + experiment_uuid)
        with codecs.open(self.file_result,'a',encoding='utf8') as f: 
            f.write(message)
            if file_deletion > 0 or file_substitution > 0 or file_insertion > 0:
                f.write("Aligned transcription: {}\n".format(wav_file_name))
                f.write ( u" LAB: {}\n".format("\t".join(refernceArr)) )
                f.write (u" REC: {}\n".format("\t".join(hypothesisArr)) )
                
                
    def extractTargetList(self, wavFileName):
        '''
        Read transcription for the wav file and post process it by replacing some unnecessary instruction in transcriptions
        '''
        targetList = []
        txtFileName = wavFileName.replace(".wav", ".txt")
        #for line in txtFile:
        with open(txtFileName, "rb") as infile:
            line = infile.read()
            line = line.decode('utf-8')
            line = line.strip(u' \t\n\r')
            line = line.replace(u"\ufeff", "")
            #line = line.replace(u" _ikvepimas ", u" ")
            #line = line.replace(u" _iskvepimas ", u" ")
            line = line.replace(u"_kosejimas", u"_pauze")
            line = line.replace(u" _ikvepimas ", u"_pauze")
            line = line.replace(u" _iskvepimas ", u"_pauze")
            line = line.replace(u"_ikvepimas", u"_pauze")
            line = line.replace(u"_iskvepimas", u"_pauze")
            line = line.replace(u"_puslapis", u"_pauze")
            line = line.replace(u"_pilvas", u"_pauze")
            line = line.replace(u"_nurijimas", u"_pauze")
            line = line.replace(u"_tyla", u"_pauze")
            line = line.replace(u"_kede", u"_pauze")
            line = line.replace(u"_garsas", u"_pauze")
            line = line.replace(u"_puskapis", u"_pauze")

            targetList.extend([x.strip() for x in line.split(u'_pauze')])
        return [x for x in targetList if x != '']





    def compareRecogntionResults(self, wav_file_name, targetList, testList):
        '''
        compare recognition results with transcriptions of text file
        '''
        file_match=0
        file_substitution=0
        file_deletion=0
        file_insertion=0
        file_target=0
        file_rejection=0
         
        #print ">>>> [compareRecogntionResults]testList:   " + u", ".join(testList)
        #print ">>>> [compareRecogntionResults]targetList: " + u", ".join(targetList)
        postTestResult=self.phraseTransformer.transformToFunction(testList)
        postTargetResult=self.phraseTransformer.transformToFunction(targetList)
        LOG.info(wav_file_name + u" testList:   " + u", ".join(postTestResult))
        LOG.info(wav_file_name + u" targetList: " + u", ".join(postTargetResult))  
        
        hypothesisArr = []
        refernceArr = []
        
        file_target=len(postTargetResult)    
        if len(testList) == 0:
            file_deletion += len(postTargetResult)
            for deletedPhrase in postTargetResult:
                hypothesisArr.append("***")
                refernceArr.append(deletedPhrase)
                self.writeComparisonMessage(wav_file_name,hypotesis="***", reference=deletedPhrase, match="0", insertion="0", deletion="1", substitution="0", rejection="0")    
        else:
#            try:
            result = self.aligner.process_align(postTargetResult, postTestResult)
            for row in result:
                (hypotesis, reference, match, insertion, deletion, substitution, rejection)=row
                max_length=max(len(hypotesis), len(reference))
                hypothesisArr.append(hypotesis.ljust(max_length))
                refernceArr.append(reference.ljust(max_length))
                file_match+=int(match)
                file_substitution+=int(substitution)
                file_deletion+=int(deletion)
                file_insertion+=int(insertion)
                file_rejection+=int(rejection)
                #print ">>>>  [compareRecogntionResults] AAAAAAAAAAAAAAAAAAA: match: {}, deletion: {}, subs {}, target {}".format(file_match,  file_deletion, file_substitution, file_target)
                self.writeComparisonMessage(wav_file_name, hypotesis, reference, match, insertion, deletion, substitution, rejection)

#            except Exception,e:
#                print ">>>>>>>>>>>>>>> not alligned! " + wav_file_name
#                raise e
        if not (file_match+file_deletion+file_substitution)== file_target:
            raise Exception("Results does not match. see log. guid:" + experiment_uuid)            
        return file_match,file_substitution, file_deletion, file_insertion, file_target, file_rejection, hypothesisArr, refernceArr


    def createFinalResult(self, sum_matched, sum_substitution, sum_deletion, sum_insertion, sum_target,total):
        correct= ((total - sum_deletion - sum_substitution)/total)*100.0
        accuracy= ((total - sum_deletion - sum_substitution - sum_insertion)/total)*100
        processing_ratio = 0#porcessingDelta.total_seconds()/sum_length
        final_message = ""
        
        final_message += "\n===================== Liepa Results Analysis =======================\n"
        #final_message += "\tEngine: {}\n".format(self.engine)
        #if self.info:
        #    final_message += "\tInformation on experiment: {}\n".format(self.info)
        #final_message += "\tDate: {}\n".format(datetime.datetime.now().isoformat())
        #final_message += "\tPhrase transformation: {}\n".format(self.phraseTransformer.get_name())
        #final_message += "\tAudio signal length in {}s. Processed in {}s. Processing ratio {}\n".format(sum_length, porcessingDelta.total_seconds(), processing_ratio)
        #final_message += "\tResult file: {}\n".format(self.output_result)
        #final_message += "\tFile Summary result file: {}\n".format(self.file_result)
        #final_message += "\tAdditional noise added: {}\n".format(self.add_noise)
        #final_message += "\tpocket_sphinx: grammar: ./models/lm/{grammar}; acoustic_model: ./models/hmm/{acoustic_model}; dictionary=./models/dic/{dictionary}\n".format(
        #        grammar=self.sphinx_grammar,acoustic_model=self.sphinx_acoustic_model, dictionary=self.sphinx_dictionary)
        #cmd = self.POCKETSPHINX_CMD_TEMPLATE.format(rootDir=self.rootDir,
        #   acoustic_model=self.sphinx_acoustic_model,grammar=self.sphinx_grammar, dictionary=self.sphinx_dictionary, wav_file_name="***.wav",bin_dir=self.bin_dir)
        #final_message += "\tSphinx command sample: {}\n".format(cmd)
        final_message +=  "------------------------ Overall Results --------------------------\n"
        final_message +=  "COMMAND: %Corr={correct:.2f}, Acc={accuracy:.2f} [H={matched}, D={deletion}, S={substitution}, I={insertion}, N={target}]\n".format(
            correct=correct, accuracy=accuracy, matched=sum_matched, deletion=sum_deletion, substitution=sum_substitution, insertion=sum_insertion, target=sum_target)
        final_message += "===================================================================\n"
        
        if self.file_result:
            with codecs.open(self.file_result,'a',encoding='utf8') as f: f.write(final_message)
        
        print final_message
        LOG.info(final_message)
