
def read_emit(emit):
    '''
    Watch out! Within the text file, you have markers like: \nVB, \nRB etc...
    '''
    dictPR, dictVB, dictRB, dictNN, dictPC, dictJJ, dictDT, dictOT = {},{},{},{},{},{},{},{}
    e = open(emit)
    content_e = e.read()
    e_segments = content_e.split(' ')
    dict_key = 0
    list_of_dicts = [dictPR, dictVB, dictRB, dictNN, dictPC, dictJJ, dictDT, dictOT]
    list_of_things = ['PR', '\nVB', '\nRB', '\nNN', '\nPC', '\nJJ', '\nDT', '\nOT']
    i = 0
    for segment in e_segments:
        split = segment.split(':')
        if (segment == "PR"):
            x = 0
        if (segment == '\nVB'):
            x = 1
        if (segment == "\nRB"):
            x = 2
        if (segment == "\nNN"):
            x = 3
        if (segment == "\nPC"):
            x = 4
        if (segment == "\nJJ"):
            x = 5
        if (segment == "\nDT"):
            x = 6
        if (segment == "\nOT"):
            x = 7
        if (segment != "\n" and segment not in list_of_things):
            list_of_dicts[x].update({split[0]:split[1]})
        i += 1
    return dictPR, dictVB, dictRB, dictNN, dictPC, dictJJ, dictDT, dictOT
    
    

def read_transmit(transmit):
    '''
    One line at a time, conditional probability for any one of PR, RB etc given first segment of line
    which is itself one of PR, RB etc...
    '''
    t = open(transmit)
    content_t = t.read()
    t_lines = content_t.splitlines()
    little_dict = {}

    for lines in t_lines:
        line_segments = lines.split(' ')

        for i in range(1, len(line_segments)-1, 1):
            split = line_segments[i].split(':')
            little_dict.update({split[0]: split[1]})
        # You need a dictionary inside dictionary. make the key of the mother dictionary the line_segments[0]
        transmit_dictionary.update({line_segments[0]:little_dict})
        little_dict = {}

    

def read_dev(File):
    '''
    You need to get the words of each sentence in a list that you can iterate through
    and you want to be able to iterate through all of the lists...

    You don't need to remove the full stops, question marks etc...
    '''
    F = open(File)
    content_d = F.read()
    D_lines = content_d.splitlines()
    for lines in D_lines:
        line_segment = lines.split(' ')
        Dev.append(line_segment)



def read_prior(File):
    '''
    Simple to parse through this one
    '''
    F = open(File)
    content_f = F.read()
    F_lines = content_f.splitlines()
    for lines in F_lines:
        prior_segments = lines.split(' ')
        Prior.update({prior_segments[0]:prior_segments[1]})
        


    
#================== Main Code =======================

import numpy as np
import sys
import operator
import math
from logsum import log_sum

# Define command line arguements
filename = sys.argv
dev = filename[1]
transmission = filename[2]
emission = filename[3]
prior = filename[4]


'''Organise all the data'''

# read dev file
Dev = []
read_dev(dev)

# read the transmission file
transmit_dictionary = {}
read_transmit(transmission)

# read emission probability file
ePR, eVB, eRB, eNN, ePC, eJJ, eDT, eOT = read_emit(emission)

# read prior file
Prior = {}
read_prior(prior)

'''
--------------------- Reminder of what the data contains:
- Dev:
    contains a list of all sentences, where each element in the
    list is a list containing all the words of that same sentence
    
- transmit_dictionary:
    contains a dictionary of dictionaries where the keys of the outer dictionary are
    all word types (pronoun, verb, etc) and the values of those keys are a dictionary showing the
    transition probability to every other word type, where this inner dictionary has as keys the word types
    and as values the probability to go to those keys from the key of the associated larger dictionary

- ePR, eVB, ... , eOT:
    each of them are individual dictionaries with keys being a word, and their values being the probability
    of those very words being used given the type of word that they are (pronoun, verb etc..)

- Prior:
    contains a dictionary with the keys being the type of word, and the values being the probability of those
    types of words being employed    
'''


table = []

# let's look at every sentence we want to analyse
for sentences in Dev:
    table = []
    alf = {}
    
    alf.update({'PR':math.log(1)})
    alf.update({'PC':math.log(1)})
    alf.update({'VB':math.log(1)})
    alf.update({'RB':math.log(1)})
    alf.update({'NN':math.log(1)})
    alf.update({'JJ':math.log(1)})
    alf.update({'OT':math.log(1)})
    alf.update({'DT':math.log(1)})

    table.append(alf)
    
    # Now lets find all of the next alphas until we have exhausted all of the symbols/words in the sentence
    for i in range(len(sentences)-2, -1, -1):

        alf = {}

        I,X,Y = 0,0,0
        for J in transmit_dictionary:

            if J == 'PR':
                BIO = float(ePR[sentences[i+1]])
            if J == 'PC':
                BIO = float(ePC[sentences[i+1]])
            if J == 'VB':
                BIO = float(eVB[sentences[i+1]])
            if J == 'RB':
                BIO = float(eRB[sentences[i+1]])
            if J == 'NN':
                BIO = float(eNN[sentences[i+1]])
            if J == 'JJ':
                BIO = float(eJJ[sentences[i+1]])
            if J == 'OT':
                BIO = float(eOT[sentences[i+1]])
            if J == 'DT':
                BIO = float(eDT[sentences[i+1]])

            prod = math.log(BIO)
            
            transition_prob = table[-1][J] + math.log(float(transmit_dictionary['PR'][J]))
           
            if (I == 0):
                X = transition_prob + prod
            if (I > 0):
                Y = transition_prob + prod
                X = log_sum(X,Y)

            I += 1

        alf.update({'PR':X})

        #---------

        I,X,Y = 0,0,0
        for J in transmit_dictionary:

            if J == 'PR':
                BIO = float(ePR[sentences[i+1]])
            if J == 'PC':
                BIO = float(ePC[sentences[i+1]])
            if J == 'VB':
                BIO = float(eVB[sentences[i+1]])
            if J == 'RB':
                BIO = float(eRB[sentences[i+1]])
            if J == 'NN':
                BIO = float(eNN[sentences[i+1]])
            if J == 'JJ':
                BIO = float(eJJ[sentences[i+1]])
            if J == 'OT':
                BIO = float(eOT[sentences[i+1]])
            if J == 'DT':
                BIO = float(eDT[sentences[i+1]])
            prod = math.log(BIO)
                
            transition_prob = table[-1][J] + math.log(float(transmit_dictionary['PC'][J]))
            if (I == 0):
                X = transition_prob + prod
            if (I > 0):
                Y = transition_prob + prod
                X = log_sum(X,Y)
            I += 1
        alf.update({'PC':X})
        #----------

        I,X,Y = 0,0,0
        for J in transmit_dictionary:

            if J == 'PR':
                BIO = float(ePR[sentences[i+1]])
            if J == 'PC':
                BIO = float(ePC[sentences[i+1]])
            if J == 'VB':
                BIO = float(eVB[sentences[i+1]])
            if J == 'RB':
                BIO = float(eRB[sentences[i+1]])
            if J == 'NN':
                BIO = float(eNN[sentences[i+1]])
            if J == 'JJ':
                BIO = float(eJJ[sentences[i+1]])
            if J == 'OT':
                BIO = float(eOT[sentences[i+1]])
            if J == 'DT':
                BIO = float(eDT[sentences[i+1]])
            prod = math.log(BIO)
            
            transition_prob = table[-1][J] + math.log(float(transmit_dictionary['VB'][J]))
            if (I == 0):
                X = transition_prob + prod
            if (I > 0):
                Y = transition_prob + prod
                X = log_sum(X,Y)
            I += 1
        alf.update({'VB':X})
        #-----------
        I,X,Y = 0,0,0
        for J in transmit_dictionary:
            if J == 'PR':
                BIO = float(ePR[sentences[i+1]])
            if J == 'PC':
                BIO = float(ePC[sentences[i+1]])
            if J == 'VB':
                BIO = float(eVB[sentences[i+1]])
            if J == 'RB':
                BIO = float(eRB[sentences[i+1]])
            if J == 'NN':
                BIO = float(eNN[sentences[i+1]])
            if J == 'JJ':
                BIO = float(eJJ[sentences[i+1]])
            if J == 'OT':
                BIO = float(eOT[sentences[i+1]])
            if J == 'DT':
                BIO = float(eDT[sentences[i+1]])
            prod = math.log(BIO)
            transition_prob = table[-1][J] + math.log(float(transmit_dictionary['RB'][J]))
            if (I == 0):
                X = transition_prob + prod
            if (I > 0):
                Y = transition_prob + prod
                X = log_sum(X,Y)
            I += 1
        alf.update({'RB':X})
        #-------------

        I,X,Y = 0,0,0
        for J in transmit_dictionary:
            if J == 'PR':
                BIO = float(ePR[sentences[i+1]])
            if J == 'PC':
                BIO = float(ePC[sentences[i+1]])
            if J == 'VB':
                BIO = float(eVB[sentences[i+1]])
            if J == 'RB':
                BIO = float(eRB[sentences[i+1]])
            if J == 'NN':
                BIO = float(eNN[sentences[i+1]])
            if J == 'JJ':
                BIO = float(eJJ[sentences[i+1]])
            if J == 'OT':
                BIO = float(eOT[sentences[i+1]])
            if J == 'DT':
                BIO = float(eDT[sentences[i+1]])
            prod = math.log(BIO)
            transition_prob = table[-1][J] + math.log(float(transmit_dictionary['NN'][J]))
            if (I == 0):
                X = transition_prob + prod
            if (I > 0):
                Y = transition_prob + prod
                X = log_sum(X,Y)
            I += 1
        alf.update({'NN':X})
        #-------------
        I,X,Y = 0,0,0
        for J in transmit_dictionary:
            if J == 'PR':
                BIO = float(ePR[sentences[i+1]])
            if J == 'PC':
                BIO = float(ePC[sentences[i+1]])
            if J == 'VB':
                BIO = float(eVB[sentences[i+1]])
            if J == 'RB':
                BIO = float(eRB[sentences[i+1]])
            if J == 'NN':
                BIO = float(eNN[sentences[i+1]])
            if J == 'JJ':
                BIO = float(eJJ[sentences[i+1]])
            if J == 'OT':
                BIO = float(eOT[sentences[i+1]])
            if J == 'DT':
                BIO = float(eDT[sentences[i+1]])
            prod = math.log(BIO)
            transition_prob = table[-1][J] + math.log(float(transmit_dictionary['JJ'][J]))
            if (I == 0):
                X = transition_prob + prod
            if (I > 0):
                Y = transition_prob + prod
                X = log_sum(X,Y)
            I += 1
        alf.update({'JJ':X})
        #---------------

        I,X,Y = 0,0,0
        for J in transmit_dictionary:
            if J == 'PR':
                BIO = float(ePR[sentences[i+1]])
            if J == 'PC':
                BIO = float(ePC[sentences[i+1]])
            if J == 'VB':
                BIO = float(eVB[sentences[i+1]])
            if J == 'RB':
                BIO = float(eRB[sentences[i+1]])
            if J == 'NN':
                BIO = float(eNN[sentences[i+1]])
            if J == 'JJ':
                BIO = float(eJJ[sentences[i+1]])
            if J == 'OT':
                BIO = float(eOT[sentences[i+1]])
            if J == 'DT':
                BIO = float(eDT[sentences[i+1]])
            prod = math.log(BIO)
            
            transition_prob = table[-1][J] + math.log(float(transmit_dictionary['OT'][J]))
            if (I == 0):
                X = transition_prob + prod
            if (I > 0):
                Y = transition_prob + prod
                X = log_sum(X,Y)
            I += 1
        alf.update({'OT':X})
        #--------------

        I,X,Y = 0,0,0
        for J in transmit_dictionary:
            if J == 'PR':
                BIO = float(ePR[sentences[i+1]])
            if J == 'PC':
                BIO = float(ePC[sentences[i+1]])
            if J == 'VB':
                BIO = float(eVB[sentences[i+1]])
            if J == 'RB':
                BIO = float(eRB[sentences[i+1]])
            if J == 'NN':
                BIO = float(eNN[sentences[i+1]])
            if J == 'JJ':
                BIO = float(eJJ[sentences[i+1]])
            if J == 'OT':
                BIO = float(eOT[sentences[i+1]])
            if J == 'DT':
                BIO = float(eDT[sentences[i+1]])
            prod = math.log(BIO)
            transition_prob = table[-1][J] + math.log(float(transmit_dictionary['DT'][J]))
            if (I == 0):
                X = transition_prob + prod
            if (I > 0):
                Y = transition_prob + prod
                X = log_sum(X,Y)
            I += 1
        alf.update({'DT':X})
        #print alf

        table.append(alf)


    # Once you have appended all those bloody things into one big beautiful wal...table you want
    # to find the end probability...
    PO_given_lambda = 0
    I,X,Y = 0,0,0
    for value in table[-1]:
        PO_given_lambda = table[-1][value]
        PI = float(Prior[value])
        if value == 'PR':
            BIO = float(ePR[sentences[0]])
        if value == 'PC':
            BIO = float(ePC[sentences[0]])
        if value == 'VB':
            BIO = float(eVB[sentences[0]])
        if value == 'RB':
            BIO = float(eRB[sentences[0]])
        if value == 'NN':
            BIO = float(eNN[sentences[0]])
        if value == 'JJ':
            BIO = float(eJJ[sentences[0]])
        if value == 'OT':
            BIO = float(eOT[sentences[0]])
        if value == 'DT':
            BIO = float(eDT[sentences[0]])

        if (I == 0):
            X = PO_given_lambda + math.log(PI) + math.log(BIO)
        if (I > 0):
            Y = PO_given_lambda + math.log(PI) + math.log(BIO)
            X = log_sum(X,Y)
        I += 1
    print X

