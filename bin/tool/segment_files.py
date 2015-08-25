#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,glob,subprocess,re

seg_output_regex=re.compile("Utterance \d+: file (.*)\.wav\.raw start ([\d\.]+) sec length 0 samples \( 0\.00 sec \)")
FRAMES_IN_SEC=100

def toFrame(sec):
    return int(round(sec*FRAMES_IN_SEC))

def iterate_files(src_dir):
    for corpus_dir in os.listdir(src_dir):
        read_files = glob.glob(src_dir + "/" + corpus_dir  + "/*.wav")
        for wav_file in read_files:
            cmd = '"bin\sphinx-20150402(r12906)-win32/sphinxbase/bin/sphinx_seg" -infile {} -singlefile yes'.format(wav_file)
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            result, err = p.communicate()
            #print result
            startTime = toFrame(0.0)
            for line in result.split("\n"):
                m = seg_output_regex.search(line)
                if not m:
                    continue
                fileName = m.group(1)
                fileName = fileName.replace(src_dir+"/","")
                endTime = toFrame(float(m.group(2)))
                if endTime != 0:
                    print "{} {} {}".format(fileName, startTime, endTime    )
                startTime = endTime
            print "{} {} {}".format(fileName, startTime, "-1")#write end segment
        
def main():
    src_dir = "wav/patikra"
    iterate_files(src_dir)
    
if __name__ == "__main__":
    main()
