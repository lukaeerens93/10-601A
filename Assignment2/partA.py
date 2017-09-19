

def parseFile(dataset):
    '''
    Dataset is a txt file that uses whitespaces instead of collumn borders, these whitespaces have varrying width
    so parseFile is a function that returns an organised usable representation of this dataset which can make us
    of iterators.
    All the code below can be used in order to read the other dataset too although you will need to replace the 20 
    in [for i in range(1, len(data)-1, 20)] to 10 if there are 5 collumns (4 attributes, 1 risk label)
    '''
    txtFile = open(dataset[1], 'r')
    content = txtFile.read()
    splitContent = content.splitlines()
    loopCount = 0   #Only to count the first line

    # For all lines in the dataset
    for lines in splitContent:
        loopCount = loopCount + 1

        # Extract the words by whitespace
        subsplits = lines.split(' ')
        
        # Some elements will be seperated by \t which is a tab
        for i in range(0,len(subsplits)):
            
            subsplits[i] = subsplits[i].split('\t')
            
            # Fill up data array with initial string element
            if i == 0 and loopCount == 1:
                data = subsplits[i]
                
            # Fill it up with all subsequent string elements
            else:
                data += subsplits[i]

    # data_ = only the values of the attributes and not the names of attributes themselves
    data_ = data[1::2]
    #print data_
    
    '''
    
    for i in range(0, len(data_)-1, 10):   # Now only contains 10 collumns (just values and no attribute names)
        print (data_[i:i+10])
    '''
        
    del data[:]         # Delete the list which contains attribute names and values together
    return data_
        
    


def findS(parsed_data):
    '''
    Find -s Algorithm:

    1. Initialize h to most specific hypothesis in H
    2. For each positive training instance x
           if contraint (a)i in h is satisfied by x
                   continue
           else:
                   replace (a)i in h by the next more general contraint that is satified by x
     Output hypothesis h
    '''
    pos = 0 # Used to ensure the first high training case is used to initialise h for high    
    #neg = 0 # Used to ensure the first low training case is used to initialise h for low
    LoopCount = 0
    #Arrays that hold hypothesis from initial training examples for high and low
    h_pos = []
    #h_neg = []

    partA6TxtFile = open("partA6.txt", "w")     # Open the file for writing
    
    for i in range(0, len(parsed_data)-1, 10):  # For every 10th item (for start of every line)
        
        if (parsed_data[i+9] == 'high'):     #Positive Cases of High Risk ONLY (Hypothesis updates should only occure for examples that relate to the label in question)
            pos = pos + 1
            if (pos == 1):
                # Append the value of the attributes
                h_pos.append(parsed_data[i])
                h_pos.append(parsed_data[i+1])
                h_pos.append(parsed_data[i+2])
                h_pos.append(parsed_data[i+3])
                h_pos.append(parsed_data[i+4])
                h_pos.append(parsed_data[i+5])
                h_pos.append(parsed_data[i+6])
                h_pos.append(parsed_data[i+7])
                h_pos.append(parsed_data[i+8])
                #print (h_pos)      <This is the hypothesis h being tested>


            if (pos > 1):
                # Compare the initial hypothesis with each successive training example attribute values
                # If h values are the same, continue, if they are different replace h value in question with ?
                # Also ensure that if the h value has already been converted to ?

                if (h_pos[0] != parsed_data[i]):                # First element to first element
                    h_pos[0] = '?'
                    
                if (h_pos[1] != parsed_data[i+1]):              # Second element to second element
                    h_pos[1] = '?'
                    
                if (h_pos[2] != parsed_data[i+2]):              # Third element to third element
                    h_pos[2] = '?'
                     
                if (h_pos[3] != parsed_data[i+3]):              # Fourth element to fourth element
                    h_pos[3] = '?'

                if (h_pos[4] != parsed_data[i+4]):              # Fifth element to fifth element
                    h_pos[4] = '?'

                if (h_pos[5] != parsed_data[i+5]):              # Sixth element to sixth element
                    h_pos[5] = '?'

                if (h_pos[6] != parsed_data[i+6]):              # Seventh element to seventh element
                    h_pos[6] = '?'

                if (h_pos[7] != parsed_data[i+7]):              # Eighth element to eighth element
                    h_pos[7] = '?'

                if (h_pos[8] != parsed_data[i+8]):              # Ninth element to ninth element
                    h_pos[8] = '?'

                #print ("h_pos: " + str(h_pos))
    
        
        # Write the hypothesis in the txt file in requested format
        LoopCount = LoopCount + 1
        #print LoopCount
        if (LoopCount % 30 == 29):
            for item in h_pos:
                partA6TxtFile.write(item)
                partA6TxtFile.write("\t")
            partA6TxtFile.write("\n")
            #print h_pos

    partA6TxtFile.close()   # Close the file after you are done
    return h_pos            






def finalH_missclassRate(finalHypothesis, parsed_file):
    
    highclass = 0
    missclassRate = 0
    actualClass = []        #Holds the actual classifications
    classification = 1 
    lc = 0  # loop count
    
    for i in range(0, len(parsed_file)-1, 10):   # Now only contains 10 collumns (just values and no attribute names)

        '''
        print (parsed_file[i:i+10])
        print finalHypothesis
        '''
    
        # Compare the final hypothesis with each example and find fraction of misclassified data points
    
        if (finalHypothesis[0] == parsed_file[i] and finalHypothesis[0] != "?"):                # First element to first element
            highclass = highclass + 1
            actualClass.append(parsed_file[i+9])
            classification = 0          #0 means false, 1 means true

        if (classification == 1):    
            if (finalHypothesis[1] == parsed_file[i+1] and finalHypothesis[1] != "?"):              # Second element to second element
                highclass = highclass + 1
                actualClass.append(parsed_file[i+9])
                classification = 0

        if (classification == 1):     
            if (finalHypothesis[2] == parsed_file[i+2] and finalHypothesis[2] != "?"):              # Third element to third element
                highclass = highclass + 1
                actualClass.append(parsed_file[i+9])
                classification = 0
                 
        if (classification == 1): 
            if (finalHypothesis[3] == parsed_file[i+3] and finalHypothesis[3] != "?"):              # Fourth element to fourth element
                highclass = highclass + 1
                actualClass.append(parsed_file[i+9])
                classification = 0

        if (classification == 1): 
            if (finalHypothesis[4] == parsed_file[i+4] and finalHypothesis[4] != "?"):              # Fifth element to fifth element
                highclass = highclass + 1
                actualClass.append(parsed_file[i+9])
                classification = 0

        if (classification == 1): 
            if (finalHypothesis[5] == parsed_file[i+5] and finalHypothesis[5] != "?"):              # Sixth element to sixth element
                highclass = highclass + 1
                actualClass.append(parsed_file[i+9])
                classification = 0

        if (classification == 1): 
            if (finalHypothesis[6] == parsed_file[i+6] and finalHypothesis[6] != "?"):              # Seventh element to seventh element
                highclass = highclass + 1
                actualClass.append(parsed_file[i+9])
                classification = 0

        if (classification == 1): 
            if (finalHypothesis[7] == parsed_file[i+7] and finalHypothesis[7] != "?"):              # Eighth element to eighth element
                highclass = highclass + 1
                actualClass.append(parsed_file[i+9])
                classification = 0

        if (classification == 1): 
            if (finalHypothesis[8] == parsed_file[i+8] and finalHypothesis[8] != "?"):              # Ninth element to ninth element
                highclass = highclass + 1
                actualClass.append(parsed_file[i+9])
                classification = 0

        #Reset the classification to 1
        classification = 1

        #Increment the overall loop count
        lc = lc + 1


    #Count the number of negative training examples in array that holds all positively predicted ones
    negativeEx = actualClass.count("low")
    #print negativeEx

    # Calculate the rate of high classification (the overall missclassification for all examples)
    missclassRate = float(negativeEx)/float(lc)

    print missclassRate





def finalH_RiskClassifer(finalHypothesis, parsed_file):


    for i in range(0, len(parsed_file)-1, 10):   # Now only contains 10 collumns (just values and no attribute names)

        check = 0       # A check that checks out the checkboxes for each attribute
        
        #print (parsed_file[i:i+10])
    
        # If hypothesis matches the data in all attributes predict high
    
        if (finalHypothesis[0] == parsed_file[i] or finalHypothesis[0] == "?"):                # First element to first element
            check = check + 1
   
        if (finalHypothesis[1] == parsed_file[i+1] or finalHypothesis[1] == "?"):              # Second element to second element
            check = check + 1
  
        if (finalHypothesis[2] == parsed_file[i+2] or finalHypothesis[2] == "?"):              # Third element to third element
            check = check + 1
 
        if (finalHypothesis[3] == parsed_file[i+3] or finalHypothesis[3] == "?"):              # Fourth element to fourth element
            check = check + 1

        if (finalHypothesis[4] == parsed_file[i+4] or finalHypothesis[4] == "?"):              # Fifth element to fifth element
            check = check + 1

        if (finalHypothesis[5] == parsed_file[i+5] or finalHypothesis[5] == "?"):              # Sixth element to sixth element
            check = check + 1

        if (finalHypothesis[6] == parsed_file[i+6] or finalHypothesis[6] == "?"):              # Seventh element to seventh element
            check = check + 1

        if (finalHypothesis[7] == parsed_file[i+7] or finalHypothesis[7] == "?"):              # Eighth element to eighth element
            check = check + 1

        if (finalHypothesis[8] == parsed_file[i+8] or finalHypothesis[8] == "?"):              # Ninth element to ninth element
            check = check + 1
            

        if (check == 9):
            #Reset the classification to 1
            classification = "high"
        if (check != 9):
            classification = "low"
            

        print classification
    
#==============================================================================================================================================================================
# Questions 1 -> 5
# 1) Print (to stdout), by itself on the first line, the size of the input space (number of possible unique inputs). 
input_space = 2**9 # 3*9 distinct inputs (eg: low, high, ?) * 9
print (input_space)

# 2)
concept_space = 2**input_space # 2^3^9 = 68719476736
noOfDigits = len(str(concept_space))    #Get number of digits by convert number into a string and read the length of the string
print (noOfDigits)

# 3) 
hypothesis_space = 1 + 3**9 # There are 9 boolean attributes, the number of distinct functions of all of these put together is 2^2^n where n = number of boolean attributes
print (hypothesis_space)

# 4)
new_hypothesis_space = 1 + 3**10
print (new_hypothesis_space)

# 5)
hypothesis_space5 = 4 * 3**8 + 1
print (hypothesis_space5)


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# MAIN CODE


import sys

data = []       # A list that holds all of the values in the dataset, to make use of iterators

example = sys.argv      # Read the dataset file from terminal arguement provided (ie: python partA.py testFileName)


# Question 6
parsedData6 = parseFile(['partA.py', '9Cat-Train.labeled'])
finalH = findS(parsedData6)

# Question 7
parsedData7 = parseFile(['partA.py', '9Cat-Dev.labeled'])
finalH_missclassRate(finalH, parsedData7)

#Question 8
parsedData8 = parseFile(example)
finalH_RiskClassifer(finalH, parsedData8)       #Even though you care about misclassification


