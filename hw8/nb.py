
def whichFiles(file_list):
    l = []
    f = open(file_list)
    content = f.read()
    c = content.splitlines()
    for line in c:
        l.append(line)
    f.close()
    return l

def readFiles(file_list, words):
    for File in file_list:
        f = open(File)
        content = f.read()
        c = content.splitlines()
        for line in c:
            line = line.lower()         # ignore capital cases
            if line not in words:
                words.update({line:1})
        f.close()
    
def calculatePrior(file_list):
    # Calculate what fraction of blogs are conservative or liberal
    liberal, conservative = 0, 0
    for f in file_list:
        if ("con" in f):
            conservative += 1
        else:
            liberal += 1
    total_files = len(file_list)
    conservative = float(conservative)/float(total_files)
    liberal = float(liberal)/float(total_files)
    return conservative, liberal
            
def count_target_value_words(file_list, targetValue):
    if (targetValue == "conservative"):
        for File in file_list:
            if ("con" in File):
                f = open(File)
                content = f.read()
                c = content.splitlines()
                for line in c:
                    line = line.lower()
                    if line not in conservative_words:
                        conservative_words.update({line:1})
                    else:
                        conservative_words[line] += 1
                f.close()
    if (targetValue == "liberal"):
        for File in file_list:
            if ("lib" in File):
                f = open(File)
                content = f.read()
                c = content.splitlines()
                for line in c:
                    line = line.lower()
                    if line not in liberal_words:
                        liberal_words.update({line:1})
                    else:
                        liberal_words[line] += 1    
                f.close()
    

def calculateLikelihood(wordList, vocabSize, prob_list):
    n = sum(wordList.values())
    for word in wordList:
        P = float(wordList[word]+1)/float(n+vocabSize)
        prob_list.update({word:P})
    return n

       
def classify_Naive_Bayes(file_list, vocabSize, numCon, numLib):
    conRight, libRight = 0,0
    for File in file_list:
        f = open(File)
        content = f.read()
        c = content.splitlines()
        probC, probL = 0,0
        for line in c:                  # for each word
            line = line.lower()
            if line in training_words:
                if line in conservative_words:
                    prob = P_w_given_v_con[line]
                    prob = math.log(prob)
                    probC += prob
                
                else:
                    prob = float(1)/float(numCon+vocabSize)
                    prob = math.log(prob)
                    probC += prob
                
                if line in liberal_words:
                    prob = P_w_given_v_lib[line]
                    prob = math.log(prob)
                    probL += prob
                
                else:
                    prob = float(1)/float(numLib+vocabSize)
                    prob = math.log(prob)
                    probL += prob
            
                
        c_ = math.log(con) + probC
        l_ = math.log(lib) + probL
        Vnb = max(c_, l_)

        if (Vnb == c_):
            print ("C")
            if ("con" in File):
                conRight += 1
        if (Vnb == l_):
            print ("L")
            if ("lib" in File):
                libRight += 1
        f.close()
        # When you have gone through all of the files find accuracy
    
    accuracy = float(conRight+libRight) / float(len(file_list))
    print ("Accuracy: " + str(round(accuracy,4)))



#================== Main Code =======================
import numpy as np
import sys
import math

filename = sys.argv
trainingList, testList = filename[1], filename[2]


# Generate the list of files that need to be read by the computer
tr_list = whichFiles(trainingList)
te_list = whichFiles(testList)


# Collect all distinct words and tokens
training_words = {}
readFiles(tr_list, training_words)  # len(training_words) = 45431 compared to total 849463 words

# n: total number of distinct word positions in Textj (see Tom Mitchell Page 183)
n_tr = len(training_words)


# Calculate the prior
con, lib = calculatePrior(tr_list)  # con = 0.518518518519, lib = 0.481481481481


# Find distinctive words in target value (conservative or liberal) and count their occurence
conservative_words, liberal_words = {},{}
count_target_value_words(tr_list, "conservative")   # Conservative words
count_target_value_words(tr_list, "liberal")        # Liberal words


# Calculate the likelihood
P_w_given_v_con, P_w_given_v_lib = {},{}          # Will hold probabilities of word given vocab values
n_c = calculateLikelihood(conservative_words, n_tr, P_w_given_v_con)
n_l = calculateLikelihood(liberal_words, n_tr, P_w_given_v_lib)

# Apply Naive Bayes Classification
classify_Naive_Bayes(te_list, n_tr, n_c, n_l)

