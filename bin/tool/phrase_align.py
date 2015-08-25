#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Mindaugas Greibus

'''
import sys
import csv
import logging
#logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)



class PhraseAligner:

    align_matrix = None
    backtrace_matrix = None
    INS = 1;
    DEL = 2;
    MATCH = 3;
    SUBST = 4;

    def __init__(self):
        pass

    def initMatrix(self, ref, hyp):
        LOG.debug("[[[initialize]]]")
        self.align_matrix = [[0 for x in xrange(len(hyp)+1)] for x in xrange(len(ref)+1)] 
        self.backtrace_matrix =  [[0 for x in xrange(len(hyp)+1)] for x in xrange(len(ref)+1)]
        
        for j in range(0,len(hyp)+1):
        #for idx, val in enumerate(hyp): 
            self.align_matrix[0][j] = j;
            self.backtrace_matrix[0][j] = self.INS;
        
        for i in range(0,len(ref)+1):
        #for idx, val in enumerate(ref): 
            self.align_matrix[i][0] = i;
            self.backtrace_matrix[i][0] = self.DEL;
            



    def align(self, ref, hyp):
        LOG.debug("[[[align]]]")
        for i in range(1,len(ref)+1):
            for j in range(1,len(hyp)+1):
                cost = 0
                if ref[i-1] != hyp[j-1] :
                    cost = 1
                insertion = self.align_matrix[i][j-1]+1
                deletion = self.align_matrix[i-1][j]+1
                substitution = self.align_matrix[i-1][j-1] + cost
                LOG.debug("Costs at {} {}: INS {} DEL {} SUBST {}".format(i,j,insertion,deletion,substitution))
                
                minimum = min(insertion, deletion, substitution)
                self.align_matrix[i][j] = minimum
                if minimum == substitution:
                    if cost:
                        LOG.debug(u"SUBSTITUTION ({} <=> {})".format(ref[i-1], hyp[j-1]))
                    else:
                        LOG.debug(u"MATCH ({} <=> {})".format(ref[i-1], hyp[j-1]))
                    self.backtrace_matrix[i][j] = self.MATCH+cost;
                elif minimum == insertion:
                    LOG.debug(u"INSERTION (0 => {})".format(hyp[j-1]))
                    self.backtrace_matrix[i][j] = self.INS;
                elif minimum == deletion:
                     LOG.debug(u"DELETION ({} => 0)".format(ref[i-1]))
                     self.backtrace_matrix[i][j] = self.DEL;
                else:
                    LOG.debug("Error filling: %f (%i, %i)" % (minimum, i, j))
                    raise Exception("Error filling")
    
    def backtrace(self, ref, hyp):
        i = len(ref)
        j = len(hyp)
        refPath = []
        hypPath = []
        matchPath = []
        insertionPath = []
        deletionPath = []
        substitutionPath = []
        rejectionPath = []
        LOG.debug( "[[[backtrace]]]")
        #inspen = delpen = substpen = match =0
        while i > 0 or j > 0:
            pointer = self.backtrace_matrix[i][j];
            LOG.debug( "Cost at {} {}: {}".format(i,j, self.align_matrix[i][j]))

            if pointer == self.INS:
                LOG.debug( u"INSERTION {} => {}".format ('***',hyp[j-1]))
                refPath.insert(0, u"***")
                hypPath.insert(0, hyp[j-1])
                matchPath.insert(0,u"0")
                insertionPath.insert(0,u"1")
                deletionPath.insert(0,u"0")
                substitutionPath.insert(0,u"0")
                rejectionPath.insert(0,u"0")
                #inspen +=1
                j -= 1
                LOG.debug (u" - moving to {} {}\n".format(i,j))
            elif pointer == self.DEL:
                LOG.debug(u"DELETION {} => {}".format(ref[i-1],"***"))
                refPath.insert(0, ref[i-1])
                hypPath.insert(0,u"***")
                matchPath.insert(0,u"0")
                insertionPath.insert(0,u"0")
                deletionPath.insert(0,u"1")
                substitutionPath.insert(0,u"0")
                rejectionPath.insert(0,u"0")                                
                #delpen +=1
                i -= 1        
                LOG.debug(u" - moving to {} {}\n".format(i,j))
            elif pointer == self.MATCH:
                LOG.debug( u"MATCH {} => {}".format(ref[i-1],hyp[j-1]))
                refPath.insert(0, ref[i-1])
                hypPath.insert(0,hyp[j-1])
                matchPath.insert(0,u"1")
                insertionPath.insert(0,u"0")
                deletionPath.insert(0,u"0")
                substitutionPath.insert(0,u"0")                
                rejectionPath.insert(0,u"0")                
                #match +=1
                i -= 1 
                j -= 1
                LOG.debug(u" - moving to {} {}\n".format(i,j))
            elif pointer == self.SUBST:
                LOG.debug( u"SUBST {} => {}".format(ref[i-1],hyp[j-1]))
                insertionPath.insert(0,u"0")
                deletionPath.insert(0,u"0")
                substitutionPath.insert(0,u"1")            
                refPath.insert(0, ref[i-1].upper())
                hypPath.insert(0, hyp[j-1].upper())
                matchPath.insert(0,u"0")
                rejectionPath.insert(0,u"0")
                #substpen +=1
                i -= 1 
                j -= 1
                LOG.debug(u" - moving to {} {}\n".format(i,j))
            else:
                #print "Error path calc: %i (%i, %i)" % (pointer, i, j), 
                #print align_matrix
                raise Exception("Error path calc")
                #print "BREAK????"
                #break;
        result = [rejectionPath, substitutionPath, deletionPath, insertionPath,matchPath, refPath, hypPath]
        return zip(*result[::-1])


    def process_align(self, pref, phyp): 
        ref = pref[:]
        hyp = phyp[:]
        #ref.append("")
        #hyp.append("")
        #ref.insert(0,"")
        #hyp.insert(0,"")
        self.initMatrix(ref,hyp)
        self.align(ref, hyp)
        return self.backtrace(ref, hyp)
                    
                     
        


def mainTwoFiles(aFile, bFile):
    aligner = PhraseAligner()
    aList = []
    with open(aFile, 'rb') as csvfile:
        aCsv = csv.reader(csvfile, delimiter=';')
        for aRow in aCsv:
            aList.append(unicode(aRow[0].strip(), "utf-8"))
    bList = []
    with open(bFile, 'rb') as csvfile:
        bCsv = csv.reader(csvfile, delimiter=';')
        for bRow in bCsv:
            #if unicode(bRow[1].strip(), "utf-8") == u"(null)":
            #    print u"%s; %s; 0; 0; 0; 0; 1" % (bRow[0],bRow[1])   
            #else:
            bList.append(unicode(bRow[0].strip(), "utf-8"))

    targetList =  bList
    testList = aList
    result = aligner.process_align(targetList, testList)
    print(u'\n'.join([';'.join([u'{:2}'.format(item) for item in row]) for row in result]))
    for row in result:
        print "%s;%s;%s;%s;%s;%s;%s" % (row[0].encode("utf-8"), row[1].encode("utf-8"), row[2].encode("utf-8"), row[3].encode("utf-8"), row[4].encode("utf-8"),row[5].encode("utf-8"),row[6].encode("utf-8"))
    


def mainStream(aFile, bCsv):
    aligner = PhraseAligner()
    aList = []
    with open(aFile, 'rb') as csvfile:
        aCsv = csv.reader(csvfile, delimiter=';')
        for aRow in aCsv:
            print "aRow: {}".format(aRow)
            if len(aRow) > 0:
                aList.append(unicode(aRow[0].strip(), "utf-8"))
    bList = []
    for bRowStr in bCsv:
        print "aRow: {}".format(aRow)
        bRow = unicode(bRowStr, "utf-8").split(':')
        print "bRow: {}".format(bRow)
        #if bRow[1].strip() == u"(null)":
        #    print u"%s; %s; 0; 0; 0; 0; 1" % (bRow[0],bRow[1])   
        #else:
        print bRow
        bList.append(bRow[1].strip()) 

    targetList =  bList
    testList = aList
    result = aligner.process_align(targetList, testList)
    #print result
    #print(u'\n'.join([u';'.join([u'{%s}'.format(item) for item in row]) for row in result]))
    for row in result:
        print "%s;%s;%s;%s;%s;%s;%s" % (row[0].encode("utf-8"), row[1].encode("utf-8"), row[2].encode("utf-8"), row[3].encode("utf-8"), row[4].encode("utf-8"),row[5].encode("utf-8"),row[6].encode("utf-8"))

if __name__ == "__main__":
    if len(sys.argv[1:]) == 2:
        if sys.argv[2] == '-':
            mainStream(sys.argv[1], sys.stdin.readlines())
        else:
            mainTwoFiles(sys.argv[1], sys.argv[2])
    else:
        print "Error. should be more params"
        raise Exception("Error. should be more params")


