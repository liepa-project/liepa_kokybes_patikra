#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Mindaugas Greibus

'''
import sys 

class NopTransformer:
    def get_name(self):
        return "No tranformation"
    def transformToFunction(self, commandList):
        return commandList
        
class PhraseFunctionTransformer:

    def get_name(self):
        return "phrases to function"


    def transformToFunction(self, commandList):
        unifiedCommandList = []
        for command in commandList:
            unifiedCommand = command
            unifiedCommand = unifiedCommand.replace(u"  ", u" ")
            unifiedCommand = unifiedCommand.replace(u"parodyk", u"rodyk")
            unifiedCommand = unifiedCommand.replace(u"paeik", u"eik")
            unifiedCommand = unifiedCommand.replace(u"sugrįžti", u"grįžk")
            unifiedCommand = unifiedCommand.replace(u"grįžti", u"grįžk")
            unifiedCommand = unifiedCommand.replace(u"išeiti", u"išeik")
            unifiedCommand = unifiedCommand.replace(u"atsisakyk", u"atsakyk")


            unifiedCommand = unifiedCommand.replace(u"sumažink", u"mažink")
            unifiedCommand = unifiedCommand.replace(u"padidink", u"didink")
            unifiedCommand = unifiedCommand.replace(u"pereik", u"eik")
            unifiedCommand = unifiedCommand.replace(u"paslink", u"eik")
            unifiedCommand = unifiedCommand.replace(u"slink", u"eik")
            unifiedCommand = unifiedCommand.replace(u"patikrink", u"tikrink")
            unifiedCommand = unifiedCommand.replace(u"pašalink", u"šalink")
            unifiedCommand = unifiedCommand.replace(u"įterpti", u"įterpk")
            unifiedCommand = unifiedCommand.replace(u"vykdyti", u"vykdyk")
            unifiedCommand = unifiedCommand.replace(u"funkcia", u"funkcija")
            
            
            unifiedCommand = unifiedCommand.replace(u"vieną", u"1")
            unifiedCommand = unifiedCommand.replace(u"pirmas", u"1")
            unifiedCommand = unifiedCommand.replace(u"pirma", u"1")
            unifiedCommand = unifiedCommand.replace(u"pirmą", u"1")
            
            unifiedCommand = unifiedCommand.replace(u" du ", u" 2 ")
            unifiedCommand = unifiedCommand.replace(u"antras", u"2")
            unifiedCommand = unifiedCommand.replace(u"antra", u"2")
            unifiedCommand = unifiedCommand.replace(u"antrą", u"2")
            
            unifiedCommand = unifiedCommand.replace(u"trys", u"3")
            unifiedCommand = unifiedCommand.replace(u"tris", u"3")
            unifiedCommand = unifiedCommand.replace(u"trečias", u"3")
            unifiedCommand = unifiedCommand.replace(u"trečia", u"3")



            
            unifiedCommand = unifiedCommand.replace(u"keturis", u"4")
            unifiedCommand = unifiedCommand.replace(u"keturi", u"4")
            unifiedCommand = unifiedCommand.replace(u"ketvirtas", u"4")
            unifiedCommand = unifiedCommand.replace(u"ketvirta", u"4")
            unifiedCommand = unifiedCommand.replace(u"ketvirtą", u"4")
            
            unifiedCommand = unifiedCommand.replace(u"penkis", u"5")
            unifiedCommand = unifiedCommand.replace(u"penki", u"5")
            unifiedCommand = unifiedCommand.replace(u"penktas", u"5")
            unifiedCommand = unifiedCommand.replace(u"penkta", u"5")
            unifiedCommand = unifiedCommand.replace(u"penktą", u"5")


            unifiedCommand = unifiedCommand.replace(u"šeštas", u"6")
            unifiedCommand = unifiedCommand.replace(u"šešta", u"6")


            unifiedCommand = unifiedCommand.replace(u"septintas", u"7")
            unifiedCommand = unifiedCommand.replace(u"septinta", u"7")


            unifiedCommand = unifiedCommand.replace(u"aštuntas", u"8")
            unifiedCommand = unifiedCommand.replace(u"aštuntą", u"8")
            unifiedCommand = unifiedCommand.replace(u"aštunta", u"8")

            unifiedCommand = unifiedCommand.replace(u"devintas", u"9")
            unifiedCommand = unifiedCommand.replace(u"devinta", u"9")

            
            unifiedCommand = unifiedCommand.replace(u"dešimtas", u"10")
            unifiedCommand = unifiedCommand.replace(u"dešimtą", u"10")
            unifiedCommand = unifiedCommand.replace(u"dešimta", u"10")
            unifiedCommand = unifiedCommand.replace(u"dešimt", u"10")

            unifiedCommand = unifiedCommand.replace(u"vienuoliktas", u"11")
            unifiedCommand = unifiedCommand.replace(u"vienuolikta", u"11")

            unifiedCommand = unifiedCommand.replace(u"dvyliktas", u"12")
            unifiedCommand = unifiedCommand.replace(u"dvylikta", u"12")


            unifiedCommand = unifiedCommand.replace(u"stop", u"stabdyk")
            unifiedCommand = unifiedCommand.replace(u"taikyk", u"vykdyk")
            unifiedCommand = unifiedCommand.replace(u"užbaik", u"baik")

            unifiedCommand = unifiedCommand.replace(u"funkciją", u"funkcija")
            unifiedCommand = unifiedCommand.replace(u"mano ", u"")
            unifiedCommand = unifiedCommand.replace(u"režimą", u"rėžimą")
            unifiedCommand = unifiedCommand.replace(u"rodyk savybės", u"rodyk savybes")
            unifiedCommand = unifiedCommand.replace(u"vykdyk 2 funkcija", u"2 funkcija")
            unifiedCommand = unifiedCommand.replace(u"vykdyk 8 funkcija", u"8 funkcija")
            unifiedCommand = unifiedCommand.replace(u"vykdyk 5 funkcija", u"5 funkcija")
            unifiedCommand = unifiedCommand.replace(u"vykdyk 4 funkcija", u"4 funkcija")
            unifiedCommand = unifiedCommand.replace(u"vykdyk 10 funkcija", u"10 funkcija")
            unifiedCommand = unifiedCommand.replace(u"atverk valdymo skydelį", u"valdymo skydelis")
            unifiedCommand = unifiedCommand.replace(u"eik į viršaplankį", u"į viršaplankį")
            unifiedCommand = unifiedCommand.replace(u"eik į pradžią", u"pradžion")
            unifiedCommand = unifiedCommand.replace(u"į pradžią", u"pradžion")
            unifiedCommand = unifiedCommand.replace(u"eik į pabaigą", u"pabaigon")
            unifiedCommand = unifiedCommand.replace(u"į pabaigą", u"pabaigon")
            unifiedCommand = unifiedCommand.replace(u"eik į kairę", u"kairėn")
            unifiedCommand = unifiedCommand.replace(u"eik į kaire", u"kairėn")
            unifiedCommand = unifiedCommand.replace(u"į kairę", u"kairėn")
            unifiedCommand = unifiedCommand.replace(u"eik kairėn", u"kairėn")
            unifiedCommand = unifiedCommand.replace(u"eik į dešinę", u"dešinėn")
            unifiedCommand = unifiedCommand.replace(u"eik į dešine", u"dešinėn")
            unifiedCommand = unifiedCommand.replace(u"į dešinę", u"dešinėn")
            unifiedCommand = unifiedCommand.replace(u"kairinė lygiuotė", u"kairinę lygiuotę")
            unifiedCommand = unifiedCommand.replace(u"įjunk dešininė lygiuotė", u"dešininė lygiuotė")
            unifiedCommand = unifiedCommand.replace(u"įjunk dešininę lygiuotę", u"dešininė lygiuotė")
            unifiedCommand = unifiedCommand.replace(u"dešininė lygiuotę", u"dešininė lygiuotė")
            unifiedCommand = unifiedCommand.replace(u"įjunk miego rėžimą", u"įjunk miego būseną")
            unifiedCommand = unifiedCommand.replace(u"įjunk pabraukimą", u"pabraukimas")
            unifiedCommand = unifiedCommand.replace(u"įjunk pusjuodį", u"pusjuodis")
            unifiedCommand = unifiedCommand.replace(u"eik į tolesnį elementą", u"į tolesnį elementą")
            unifiedCommand = unifiedCommand.replace(u"į adreso juostą", u"adreso juosta")
            unifiedCommand = unifiedCommand.replace(u"adreso juostą", u"adreso juosta")
            unifiedCommand = unifiedCommand.replace(u"įrašyk į tinklalapio adresą", u"įrašyk tinklalapio adresą")
            unifiedCommand = unifiedCommand.replace(u"pastumk puslapį žemyn vieną kartą", u"puslapį žemyn vieną kartą")
            unifiedCommand = unifiedCommand.replace(u"teisėms",u"teisėmis")
            unifiedCommand = unifiedCommand.replace(u"į ankstesnę programą",u"ankstesnė programa")
            
            

            unifiedCommand = unifiedCommand.replace(u"anuliuok veiksma", u"anuliuok veiksmą")

            #print command + "->" + unifiedCommand


            unifiedCommandList.append(unifiedCommand)
        return unifiedCommandList

def mainString(pString):
    transformer = PhraseFunctionTransformer()
    aList = []
    #print "pString: {}".format(pString)
    phraseList = unicode(pString, "utf-8").split(',')
    aList.extend(phraseList)
    result = transformer.transformToFunction(aList);
    print ", ".join(result)
        
def mainStream(pStream):
    transformer = PhraseFunctionTransformer()
    aList = []
    for iLine in pStream:
        #print "iLine: {}".format(iLine)
        phraseList = unicode(iLine, "utf-8").split(',')
        aList.extend(phraseList)
    result = transformer.transformToFunction(aList);
    print u", ".join(result)


if __name__ == "__main__":
    if len(sys.argv[1:]) == 1:
        if sys.argv[1] == '-':
            mainStream(sys.stdin.readlines())
        else:
            mainString(sys.argv[1])
    else:
        print "Error. should be more params"
        raise Exception("Error. should be more params")



