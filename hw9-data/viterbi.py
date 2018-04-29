
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
        

def write_to_txt(word, likely_transition):
    dev_txt.write(word + "_" + likely_transition + " ")
    
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

dev_txt = open("dev-tag.txt", "w")

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
Q_table = []

# let's look at every sentence we want to analyse
for sentences in Dev:
    table = []
    Q_table = []
    alf = {}
    QQ = ['PR', 'PC', 'VB', 'RB', 'NN', 'JJ','OT','DT']
    Q = [0, 1, 2, 3, 4, 5, 6 ,7]
    
    # Lets begin with finding alpha1: PIi*Bi(O1)
    PI = math.log(float(Prior['PR']))
    BI0 = math.log(float(ePR[sentences[0]]))
    alf.update({'PR':PI+BI0})
    
    PI = math.log(float(Prior['PC']))
    BI0 = math.log(float(ePC[sentences[0]]))
    alf.update({'PC':PI+BI0})
    
    PI = math.log(float(Prior['VB']))
    BI0 = math.log(float(eVB[sentences[0]]))
    alf.update({'VB':PI+BI0})
    
    PI = math.log(float(Prior['RB']))
    BI0 = math.log(float(eRB[sentences[0]]))
    alf.update({'RB':PI+BI0})
    
    PI = math.log(float(Prior['NN']))
    BI0 = math.log(float(eNN[sentences[0]]))
    alf.update({'NN':PI+BI0})
    
    PI = math.log(float(Prior['JJ']))
    BI0 = math.log(float(eJJ[sentences[0]]))
    alf.update({'JJ':PI+BI0})
    
    PI = math.log(float(Prior['OT']))
    BI0 = math.log(float(eOT[sentences[0]]))
    alf.update({'OT':PI+BI0})
    
    PI = math.log(float(Prior['DT']))
    BI0 = math.log(float(eDT[sentences[0]]))
    alf.update({'DT':PI+BI0})

    table.append(alf)
    Q_table.append(Q)

    # Now lets find all of the next alphas until we have exhausted all of the symbols/words in the sentence
    for i in range(1, len(sentences), 1):
        alf = {}
        Q = [0,0,0,0,0,0,0,0]
        
        BI0 = float(ePR[sentences[i]])
        prod = math.log(BI0)
        I,X,Y, INDEX = 0,0,0, 0
        for J in transmit_dictionary:
            #print J
            transition_prob = table[-1][J] + math.log(float(transmit_dictionary[J]['PR']))
            #print transition_prob
            if (I == 0):
                X = transition_prob
                INDEX = I
            if (I > 0):
                Y = transition_prob
                if Y > X:
                    X = Y
                    INDEX = I
            I += 1
        #print X
        #print ("-----")
        alpha_i = prod + X
        alf.update({'PR':alpha_i})
        Q[0] = INDEX
        
        #---------
        BI0 = float(ePC[sentences[i]])
        prod = math.log(BI0)
        I,X,Y, INDEX = 0,0,0, 0
        for J in transmit_dictionary:
            transition_prob = table[-1][J] + math.log(float(transmit_dictionary[J]['PC']))
            if (I == 0):
                X = transition_prob
                INDEX = I
            if (I > 0):
                Y = transition_prob
                if Y > X:
                    X = Y
                    INDEX = I
            I += 1
        alpha_i = prod + X          # This might be a source of error later
        alf.update({'PC':alpha_i})
        Q[1] = INDEX
        #----------
        BI0 = float(eVB[sentences[i]])
        prod = math.log(BI0)
        I,X,Y,INDEX = 0,0,0, 0
        for J in transmit_dictionary:
            transition_prob = table[-1][J] + math.log(float(transmit_dictionary[J]['VB']))
            if (I == 0):
                X = transition_prob
                INDEX = I
            if (I > 0):
                Y = transition_prob
                if Y > X:
                    X = Y
                    INDEX = I
            I += 1
        alpha_i = prod + X
        alf.update({'VB':alpha_i})
        Q[2] = INDEX
        #-----------
        BI0 = float(eRB[sentences[i]])
        prod = math.log(BI0)
        I,X,Y, INDEX = 0,0,0, 0
        for J in transmit_dictionary:
            transition_prob = table[-1][J] + math.log(float(transmit_dictionary[J]['RB']))
            if (I == 0):
                X = transition_prob
                INDEX = I
            if (I > 0):
                Y = transition_prob
                if Y > X:
                    X = Y
                    INDEX = I
            I += 1
        alpha_i = prod + X
        alf.update({'RB':alpha_i})
        Q[3] = INDEX
        #-------------
        BI0 = float(eNN[sentences[i]])
        prod = math.log(BI0)
        I,X,Y, INDEX = 0,0,0, 0
        for J in transmit_dictionary:
            transition_prob = table[-1][J] + math.log(float(transmit_dictionary[J]['NN']))
            if (I == 0):
                X = transition_prob
                INDEX = I
            if (I > 0):
                Y = transition_prob
                if Y > X:
                    X = Y
                    INDEX = I
            I += 1
        alpha_i = prod + X
        alf.update({'NN':alpha_i})
        Q[4] = INDEX
        #-------------
        BI0 = float(eJJ[sentences[i]])
        prod = math.log(BI0)
        I,X,Y, INDEX = 0,0,0, 0
        for J in transmit_dictionary:
            transition_prob = table[-1][J] + math.log(float(transmit_dictionary[J]['JJ']))
            if (I == 0):
                X = transition_prob
                INDEX = I
            if (I > 0):
                Y = transition_prob
                if Y > X:
                    X = Y
                    INDEX = I
            I += 1
        alpha_i = prod + X
        alf.update({'JJ':alpha_i})
        Q[5] = INDEX
        #---------------
        BI0 = float(eOT[sentences[i]])
        prod = math.log(BI0)
        I,X,Y, INDEX = 0,0,0, 0
        for J in transmit_dictionary:
            transition_prob = table[-1][J] + math.log(float(transmit_dictionary[J]['OT']))
            if (I == 0):
                X = transition_prob
                INDEX = I
            if (I > 0):
                Y = transition_prob
                if Y > X:
                    X = Y
                    INDEX = I
            I += 1
        alpha_i = prod + X
        alf.update({'OT':alpha_i})  # these coud be the problm
        Q[6] = INDEX
        #print Q[6]
        #print QQ[6]
        #--------------
        BI0 = float(eDT[sentences[i]])
        prod = math.log(BI0)
        I,X,Y, INDEX = 0,0,0, 0
        for J in transmit_dictionary:
            transition_prob = table[-1][J] + math.log(float(transmit_dictionary[J]['DT']))
            if (I == 0):
                X = transition_prob
                INDEX = I
            if (I > 0):
                Y = transition_prob
                if Y > X:
                    X = Y
                    INDEX = I
            I += 1
        alpha_i = prod + X
        alf.update({'DT':alpha_i})
        Q[7] = INDEX

        table.append(alf)
        Q_table.append(Q)
    
    '''
    
    #print sentences
    for qr in Q_table:
        print qr
    
    for kkk in table:
        print kkk
    print ("")
    '''


    # You can now find what the max value and in your Q table set that state as your end state
    # you then go backwards towards the beginning, each time following what they left off from

    # Find the largest value at the end
    node = max(table[len(Q_table)-1], key = table[len(Q_table)-1].get)
    #print node
    #print Q_table[-1]
    reference_index = ['PR', 'PC', 'VB', 'RB', 'NN', 'JJ','OT','DT']
    index_array = []
    index_array.append(reference_index.index(node))
    #print reference_index.index(node)
    node = Q_table[-1][reference_index.index(node)]
    #print node
    #print ("((((((((")

    
    for k in range(len(Q_table)-2, -1, -1):

        index_array.append(node)
        #print Q_table[k]        # Prints out an array

        index_ = Q_table[k][node]
        #print index_

        #print ("node: "+ str(node))

        # Find the value stored in Q_table that is at the index of reference index
        node = Q_table[k][node]# you may need to change this


    reversed_Array = index_array[::-1]
    #print reversed_Array

    sentence_rewrite = []
    for z in range(0, len(index_array), 1):
        write_to_txt(sentences[z], reference_index[reversed_Array[z]])
        sentence_rewrite.append(sentences[z] + "_" + reference_index[reversed_Array[z]] + " ")
    print (''.join(sentence_rewrite))
        
    # You now need to add a new line
    dev_txt.write("\n")

# Close the file when you are done
dev_txt.close()    
