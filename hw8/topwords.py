
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

        

#================== Main Code =======================
import numpy as np
import sys
import operator

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

n_con = sum(conservative_words.values())
n_lib = sum(liberal_words.values())

conserv_words =  sorted(conservative_words, key=conservative_words.get, reverse=True)[:20]
liber_words = sorted(liberal_words, key=liberal_words.get, reverse=True)[:20]


for word in liber_words:
    prob = float(liberal_words[word] + 1)/float(n_tr + n_lib)
    prob = round(prob,4)
    print (word + " " + str(prob) )

print ("")
for word in conserv_words:
    prob = float(conservative_words[word] + 1)/float(n_tr + n_con)
    prob = round(prob,4)
    print (word + " " + str(prob) )
