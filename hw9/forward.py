
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

# Let's get started!

# We are looking for alphas and P(O|lambda)

# So let's create a table to store alphas for each state
table = []

# let's look at every sentence we want to analyse
for sentences in Dev:
    table = []
    alf = {}
    # Lets begin with finding alpha1: PIi*Bi(O1)
    PI = float(Prior['PR'])
    BI0 = float(ePR[sentences[0]])
    alf.update({'PR':math.log(PI*BI0)})
    
    PI = float(Prior['PC'])
    BI0 = float(ePC[sentences[0]])
    alf.update({'PC':math.log(PI*BI0)})
    
    PI = float(Prior['VB'])
    BI0 = float(eVB[sentences[0]])
    alf.update({'VB':math.log(PI*BI0)})
    
    PI = float(Prior['RB'])
    BI0 = float(eRB[sentences[0]])
    alf.update({'RB':math.log(PI*BI0)})
    
    PI = float(Prior['NN'])
    BI0 = float(eNN[sentences[0]])
    alf.update({'NN':math.log(PI*BI0)})
    
    PI = float(Prior['JJ'])
    BI0 = float(eJJ[sentences[0]])
    alf.update({'JJ':math.log(PI*BI0)})
    
    PI = float(Prior['OT'])
    BI0 = float(eOT[sentences[0]])
    alf.update({'OT':math.log(PI*BI0)})
    
    PI = float(Prior['DT'])
    BI0 = float(eDT[sentences[0]])
    alf.update({'DT':math.log(PI*BI0)})

    table.append(alf)

    # Now lets find all of the next alphas until we have exhausted all of the symbols/words in the sentence
    for i in range(1, len(sentences), 1):
        alf = {}
        # These are found by the same probabilities used before for each word, and what you then do is
        # multiply that value by a fully connected sum from previous layer,times the state transition
        # probability
        BI0 = float(ePR[sentences[i]])
        prod = math.log(BI0)
        #print ("math.log(PI*BI0)" + str(prod))
        I,X,Y = 0,0,0
        for J in transmit_dictionary:
            transition_prob = table[-1][J] + math.log(float(transmit_dictionary[J]['PR']))
            if (I == 0):
                X = transition_prob
            if (I > 0):
                Y = transition_prob
                X = log_sum(X,Y) # The error might be here, not sure that this is the correct way to go about doing this
                #print X
            I += 1
        alpha_i = prod + X
        alf.update({'PR':alpha_i})
        #---------
        BI0 = float(ePC[sentences[i]])
        prod = math.log(BI0)
        I,X,Y = 0,0,0
        for J in transmit_dictionary:
            transition_prob = table[-1][J] + math.log(float(transmit_dictionary[J]['PC']))
            if (I == 0):
                X = transition_prob
            if (I > 0):
                Y = transition_prob
                X = log_sum(X,Y)
            I += 1
        alpha_i = prod + X
        alf.update({'PC':alpha_i})
        #----------
        BI0 = float(eVB[sentences[i]])
        prod = math.log(BI0)
        I,X,Y = 0,0,0
        for J in transmit_dictionary:
            transition_prob = table[-1][J] + math.log(float(transmit_dictionary[J]['VB']))
            if (I == 0):
                X = transition_prob
            if (I > 0):
                Y = transition_prob
                X = log_sum(X,Y)
            I += 1
        alpha_i = prod + X
        alf.update({'VB':alpha_i})
        #-----------
        BI0 = float(eRB[sentences[i]])
        prod = math.log(BI0)
        I,X,Y = 0,0,0
        for J in transmit_dictionary:
            transition_prob = table[-1][J] + math.log(float(transmit_dictionary[J]['RB']))
            if (I == 0):
                X = transition_prob
            if (I > 0):
                Y = transition_prob
                X = log_sum(X,Y)
            I += 1
        alpha_i = prod + X
        alf.update({'RB':alpha_i})
        #-------------
        BI0 = float(eNN[sentences[i]])
        prod = math.log(BI0)
        I,X,Y = 0,0,0
        for J in transmit_dictionary:
            transition_prob = table[-1][J] + math.log(float(transmit_dictionary[J]['NN']))
            if (I == 0):
                X = transition_prob
            if (I > 0):
                Y = transition_prob
                X = log_sum(X,Y)
            I += 1
        alpha_i = prod + X
        alf.update({'NN':alpha_i})
        #-------------
        BI0 = float(eJJ[sentences[i]])
        prod = math.log(BI0)
        I,X,Y = 0,0,0
        for J in transmit_dictionary:
            transition_prob = table[-1][J] + math.log(float(transmit_dictionary[J]['JJ']))
            if (I == 0):
                X = transition_prob
            if (I > 0):
                Y = transition_prob
                X = log_sum(X,Y)
            I += 1
        alpha_i = prod + X
        alf.update({'JJ':alpha_i})
        #---------------
        BI0 = float(eOT[sentences[i]])
        prod = math.log(BI0)
        I,X,Y = 0,0,0
        for J in transmit_dictionary:
            transition_prob = table[-1][J] + math.log(float(transmit_dictionary[J]['OT']))
            if (I == 0):
                X = transition_prob
            if (I > 0):
                Y = transition_prob
                X = log_sum(X,Y)
            I += 1
        alpha_i = prod + X
        alf.update({'OT':alpha_i})
        #--------------
        BI0 = float(eDT[sentences[i]])
        prod = math.log(BI0)
        I,X,Y = 0,0,0
        for J in transmit_dictionary:
            transition_prob = table[-1][J] + math.log(float(transmit_dictionary[J]['DT']))
            if (I == 0):
                X = transition_prob
            if (I > 0):
                Y = transition_prob
                X = log_sum(X,Y)
            I += 1
        alpha_i = prod + X
        alf.update({'DT':alpha_i})
        #print alf

        table.append(alf)


    # Once you have appended all those bloody things into one big beautiful wal...table you want
    # to find the end probability...
    PO_given_lambda = 0
    I,X,Y = 0,0,0
    for value in table[-1]:
        PO_given_lambda = table[-1][value]
        if (I == 0):
            X = PO_given_lambda
        if (I > 0):
            Y = PO_given_lambda
            X = log_sum(X,Y)
        I += 1
    print X

    
