#!/usr/bin/python -tt

'''
Created on Nov 14, 2012

@author: niklas
'''

import argparse
import re

## TODO: Create a class for an entry
## Chr, start, end, type, score, strand

class BEDentry:
    def __init__(self, chr, start, end, type, score, strand):
        self.chr = chr
        self.start = start
        self.end = end
        self.type = type
        self.score = score
        self.strand = strand
        
    def printEntry(self):
        return self.chr + '\t' + self.start + '\t' + self.end + '\t' + self.type + '\t' + self.score + '\t' + self.strand + '\n'

def convertScore(bdscore):
    return str(int(bdscore) * 10)

def getOrientationInfo(orientation):
    ## Orientation is: <no_reads><pos_strand><no_reads><neg_strand>. E.g. 12+12-
    ori_parts = re.search(r'(\d+)(\+)(\d+)(\-)', orientation)
    posReads = ori_parts.group(1)
    negReads = ori_parts.group(3)
    return (posReads, negReads)

def isNotZero(numReads):
    if numReads == "0":
        return False
    else:
        return True

def main():
    
    argparser = argparse.ArgumentParser()
    
    argparser.add_argument("input",
                           help="Path to the input file. This is the output file from BreakDancer")
    
    argparser.add_argument("output",
                           help="Path to the output BED file")
                  
    args = argparser.parse_args()
    
    # TODO: Input sanity check
    inputFile = args.input
    outputFile = args.output
    
    FH_INPUT = open(inputFile, "rU")
    FH_OUTPUT = open(outputFile, "w")
    
    ## Read input
    for line in FH_INPUT:
        
        ## Skip the header
        if not re.search(r'^#', line):
            splitline = line.split('\t')
            
            chromosomes = [splitline[0], splitline[3]]
            start_pos = splitline[1]
            end_pos = splitline[4]
            score = convertScore(splitline[8])
            sv_type = splitline[6]
            
            ## Check whether or not the chromosomes in the SV breakpoints are the same
            if chromosomes[0] == chromosomes[1]:
                
                oInfo = (getOrientationInfo(splitline[2]), getOrientationInfo(splitline[5]))
                                                      
                ## Check if the strands are the same
                ## Positive strand:
                if isNotZero(oInfo[0][0]) and isNotZero(oInfo[0][1]):
                    ## If yes: move on to printing
                    
                    entry = BEDentry(chromosomes[0], start_pos, end_pos, sv_type, score, "+")
                    print entry.printEntry(),
                    FH_OUTPUT.write(entry.printEntry())
                
                ## Check if only one breakpoint has reads on the positive strand    
#                else:                    
#                    
#                    if isNotZero(oInfo[0][0]):
#                        ## Reads are present only at the first position
#                        ## TODO: Figure out how to handle this
#                        
#                    elif isNotZero(oInfo[0][1]):
#                        ## Reads are present only at the first position
#                        ## TODO: Figure out how to handle this
                
                ## Negative strand:
                if isNotZero(oInfo[1][0]) and isNotZero(oInfo[1][1]):
                    ## If yes: move on to printing
                    entry = BEDentry(chromosomes[0], start_pos, end_pos, sv_type, score, "-")
                    print entry.printEntry(),
                    FH_OUTPUT.write(entry.printEntry())
            
            else:

                for chromosome in chromosomes:
                    
                    oInfo = (getOrientationInfo(splitline[2]), getOrientationInfo(splitline[5]))
                                                          
                    ## Check if the strands are the same
                    ## Positive strand:
                    if isNotZero(oInfo[0][0]) and isNotZero(oInfo[0][1]):
                        ## If yes: move on to printing
                        entry = BEDentry(chromosome, start_pos, end_pos, sv_type, score, "+")
                        print entry.printEntry(),
                        FH_OUTPUT.write(entry.printEntry())
                    
                    ## Check if only one breakpoint has reads on the positive strand    
    #                else:                    
    #                    
    #                    if isNotZero(oInfo[0][0]):
    #                        ## Reads are present only at the first position
    #                        ## TODO: Figure out how to handle this
    #                        
    #                    elif isNotZero(oInfo[0][1]):
    #                        ## Reads are present only at the first position
    #                        ## TODO: Figure out how to handle this
                    
                    ## Negative strand:
                    if isNotZero(oInfo[1][0]) and isNotZero(oInfo[1][1]):
                        ## If yes: move on to printing
                        entry = BEDentry(chromosome, start_pos, end_pos, sv_type, score, "-")
                        print entry.printEntry(),
                        FH_OUTPUT.write(entry.printEntry())
            
            #FH_OUTPUT.write("\n")
    
    FH_INPUT.close()
    FH_OUTPUT.close()
        
if __name__ == '__main__':
    main()