
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
    return n    # Tells u how many words there are per target value

def logOdds(probList1, probList2, probList3, vocabSize, numList2):
    for prob in probList1:
        if prob in probList2:
            val = float(probList1[prob])/float(probList2[prob])
            val = math.log(val)
            probList3.update({prob: val})
        else:
            val = float(probList1[prob]) / (float(1)/float(numList2 + vocabSize))
            val = math.log(val)
            # If this word that doesn't exhist has already been added to the dictionary
            # add the value to the log likelihood that already exhists for it
            if prob in probList3:
                val += probList3[prob]
            probList3.update({prob: val})
            

        
#================== Main Code =======================
import numpy as np
import sys
import operator
import math

filename = sys.argv
trainingList = filename[1]

# Generate the list of files that need to be read by the computer
tr_list = whichFiles(trainingList)


# Collect all distinct words and tokens
training_words = {}
readFiles(tr_list, training_words)

# n: total number of distinct word positions in Textj (see Tom Mitchell Page 183)
n_tr = len(training_words)

# Find distinctive words in target value (conservative or liberal) and count their occurence
conservative_words, liberal_words = {},{}
count_target_value_words(tr_list, "conservative")   # Conservative words
count_target_value_words(tr_list, "liberal")        # Liberal words

# Calculate the likelihood
P_w_given_v_con, P_w_given_v_lib = {},{}          # Will hold probabilities of word given vocab values
n_c = calculateLikelihood(conservative_words, n_tr, P_w_given_v_con)
n_l = calculateLikelihood(liberal_words, n_tr, P_w_given_v_lib)

# Calculate the log odds
logLC, logCL = {},{}
logOdds(P_w_given_v_lib, P_w_given_v_con, logLC, n_tr, n_c)
logOdds(P_w_given_v_con, P_w_given_v_lib, logCL, n_tr, n_l)



# Find the 20 largest
lc_log20 =  sorted(logLC, key=logLC.get, reverse=True)[:20]
cl_log20 = sorted(logCL, key=logCL.get, reverse=True)[:20]


for word in lc_log20:
    prob = round(logLC[word],4)
    print (word + " " + str(prob) )

print ("")
for word in cl_log20:
    prob = round(logCL[word],4)
    print (word + " " + str(prob) )
