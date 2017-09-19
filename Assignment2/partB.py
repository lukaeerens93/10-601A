def createHypothesis():
    # List of all possible hypothesis
    for a in range(0,2):
        for b in range(0,2):
            for c in range(0,2):
                for d in range(0,2):
                    for e in range(0,2):
                        for f in range(0,2):
                            for g in range(0,2):
                                for h in range(0,2):
                                    for i in range(0,2):
                                        for j in range(0,2):
                                            for k in range(0,2):
                                                for l in range(0,2):
                                                    for m in range(0,2):
                                                        for n in range(0,2):
                                                            for o in range(0,2):
                                                                for p in range(0,2):
                                                                    hypothesisSpace.append(a)
                                                                    hypothesisSpace.append(b)
                                                                    hypothesisSpace.append(c)
                                                                    hypothesisSpace.append(d)
                                                                    hypothesisSpace.append(e)
                                                                    hypothesisSpace.append(f)
                                                                    hypothesisSpace.append(g)
                                                                    hypothesisSpace.append(h)
                                                                    hypothesisSpace.append(i)
                                                                    hypothesisSpace.append(j)
                                                                    hypothesisSpace.append(k)
                                                                    hypothesisSpace.append(l)
                                                                    hypothesisSpace.append(m)
                                                                    hypothesisSpace.append(n)                                             
                                                                    hypothesisSpace.append(o)
                                                                    hypothesisSpace.append(p)

    '''
     The format of this file is:
     [Male1|Male0|Female1|Female0 | Young1|Young0|Old1|Old0 | Yes1|Yes0|No1|No0 | Yes1|Yes0|No1|No0]
     Where 1 shows the + training examples
     and
     Where 2 shows the - training examples
    '''

    #print hypothesisSpace
    #for i in range(0, len(hypothesisSpace)-1, 16):
        #print (hypothesisSpace[i:i+4])
        
    #print len(hypothesisSpace)/16
    #print ("-----------------------------")
    return hypothesisSpace




    
def parseFile(dataset):

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
            
    #for i in range(0, len(data_)-1, 5):   # Now only contains 10 collumns (just values and no attribute names)
     #   print (data_[i:i+5])
        

    del data[:]         # Delete the list which contains attribute names and values together
    return data_





def convertParsedFile(data__):

    converted_Parsed_File_Array = []
    for i in range(0, len(data__)-1, 5):


        '''
        The format of the file at the top is mentioned here again for convenience and ease of understanding when reading :
        [Male1|Male0|Female1|Female0 | Young1|Young0|Old1|Old0 | Yes1|Yes0|No1|No0 | Yes1|Yes0|No1|No0]
        Where 1 shows the + training examples
        and
        Where 0 shows the - training examples
        '''

        #If the data is negative, then you will fill in all of the items above (ie: Male, Female, etc... WHICH HAVE
        #A 0 NEXT TO THEM) with a 1 only for attribute values in the training example.
        # So if it is a low risk investment (-) and it is a woman, you will fill the index for Female0 (remember 0 shows - training example)
        # with 1, and you will list the Male0, Female1, Male 1 all with 0 etc...
        if (data__[i+4] == 'low'):

            # SOMETHING TO REMEMBER: Within each if (data__[i+n) == ???) you need to have 4 nested array appends
            # So either you are male, in which case you fill out the female parts as 0 as well, or you are a female
            # in which case you fill out the male as 0 as well...
            # Gender
            if (data__[i] == 'Male'):
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(1)
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(0)
            if (data__[i] == 'Female'):
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(1)
            # Age
            if (data__[i+1] == 'Young'):
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(1)
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(0)
            if (data__[i+1] == 'Old'):
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(1)
            # Student
            if (data__[i+2] == 'Yes'):
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(1)
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(0)
            if (data__[i+2] == 'No'):
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(1)
            # Previously Declined
            if (data__[i+3] == 'Yes'):
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(1)
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(0)
            if (data__[i+3] == 'No'):
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(1)

        if (data__[i+4] == 'high'):
            # Gender
            if (data__[i] == 'Male'):
                converted_Parsed_File_Array.append(1)
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(0)
                
            if (data__[i] == 'Female'):
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(1)
                converted_Parsed_File_Array.append(0)
            # Age
            if (data__[i+1] == 'Young'):
                converted_Parsed_File_Array.append(1)
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(0)
            if (data__[i+1] == 'Old'):
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(1)
                converted_Parsed_File_Array.append(0)
            # Student
            if (data__[i+2] == 'Yes'):
                converted_Parsed_File_Array.append(1)
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(0)
            if (data__[i+2] == 'No'):
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(1)
                converted_Parsed_File_Array.append(0)
            # Previously Declined
            if (data__[i+3] == 'Yes'):
                converted_Parsed_File_Array.append(1)
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(0)
            if (data__[i+3] == 'No'):
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(0)
                converted_Parsed_File_Array.append(1)
                converted_Parsed_File_Array.append(0)
                
                
        # This is a bit vector transormation of the original string data for all concept space
    #print (converted_Parsed_File_Array[i:i+16])
    #print ("")
    return converted_Parsed_File_Array






def listThenEliminate(Dataset, HypothesisSpace):
    '''
    You had an issue with deleting from a list which is being looped over, when you deleted a range of indeces
    from that list, the range of indeces that precedes these deleted ones, will have the first index in that range
    take up the index of the first index of the deleted range. (All values up ahead are pushed to the front of the
    the list and this causes problems because the for loop increments by x units in a range at a time, and will miss
    out completed the range of values that are after the deleted ones, as they will be indexed as the deleted ones

    The solution that I will follow is to create a new list that will be filled up with all the hypothesis that tick
    the boxes, and have for loops that parse through that Hypothesis Space. To save memory, there will only be 2 lists
    which delete the other list after the version space is computed for dataset[i] for i in range(0, len(dataset)-1,1)
    '''
    # Other array for hypothesis space whose use is explained above
    hypothesisSpace2 = []
    hypothesisSpace3 = []

    classification = 1

    for i in range(0, len(Dataset)-1, 16):
        #print Dataset[i:i+16]

        # For each training example (x, c(x))  <-- Need to know what the function is for each
        # Knowing whether this is a positive or negative training example can be done by just looking at
        # the first 4 elements in each 16 input hypothesis.
        # If: 1 is located in the index 1 or 3 (2nd and 4th spot)
        #        is a negative c(x)
        # else:
        #        is a positive c(x)
        
        if (Dataset[i] == 0 and Dataset[i+2] == 0):
            labelData = 1   # This is a high loan risk
        if (Dataset[i+1] == 0 and Dataset[i+3] == 0):
            labelData = 0   # This is a low load risk
    
        
        for j in range(0, len(HypothesisSpace)-1, 16):

            if (HypothesisSpace[j] == 0 and HypothesisSpace[j+2] == 0):
                labelHypo = 1   # This is a high loan risk
            if (HypothesisSpace[j+1] == 0 and HypothesisSpace[j+3] == 0):
                labelHypo = 0   # This is a low load risk

            # If they are both low labels
            '''
            print HypothesisSpace[j:j+4]
            print Dataset[i:i+4]

            print ("potato")
            print (len(hypothesisSpace2)/16)
            print ("potato")
            '''
                    
            if(labelHypo == 1 and labelData == 1):

                yesCounter = 0
                
                if (HypothesisSpace[j] == Dataset[i]):                  # First element to first element
                    yesCounter = yesCounter + 1

                if (HypothesisSpace[j+2] == Dataset[i+2]):              # Third element to third element
                    yesCounter = yesCounter + 1

                if (HypothesisSpace[j+4] == Dataset[i+4]):              # Fifth element to fifth element
                    yesCounter = yesCounter + 1

                if (HypothesisSpace[j+6] == Dataset[i+6]):              # Seventh element to seventh element
                    yesCounter = yesCounter + 1

                if (HypothesisSpace[j+8] == Dataset[i+8]):              # Ninth element to ninth element
                    yesCounter = yesCounter + 1

                if (HypothesisSpace[j+10] == Dataset[i+10]):              # Eleventh element to second element
                    yesCounter = yesCounter + 1

                if (HypothesisSpace[j+12] == Dataset[i+12]):              # Thirteenth element to fourth element
                    yesCounter = yesCounter + 1

                if (HypothesisSpace[j+14] == Dataset[i+14]):              # Fifteenth element to sixth element
                    yesCounter = yesCounter + 1

                #print yesCounter
                if (yesCounter == 8):
                    hypothesisSpace2.append(HypothesisSpace[j:j+16])


            if(labelHypo == 0 and labelData == 0):

                yesCounter = 0

                if (HypothesisSpace[j+1] == Dataset[i+1]):              # Second element to second element
                    yesCounter = yesCounter + 1

                if (HypothesisSpace[j+3] == Dataset[i+3]):              # Fourth element to fourth element
                    yesCounter = yesCounter + 1

                if (HypothesisSpace[j+5] == Dataset[i+5]):              # Sixth element to sixth element
                    yesCounter = yesCounter + 1

                if (HypothesisSpace[j+7] == Dataset[i+7]):              # Eighth element to eighth element
                    yesCounter = yesCounter + 1

                if (HypothesisSpace[j+9] == Dataset[i+9]):                # Tenth element to first element
                    yesCounter = yesCounter + 1

                if (HypothesisSpace[j+11] == Dataset[i+11]):              # Twelfth element to third element
                    yesCounter = yesCounter + 1

                if (HypothesisSpace[j+13] == Dataset[i+13]):              # Fourteenth element to fifth element
                    yesCounter = yesCounter + 1

                if (HypothesisSpace[j+15] == Dataset[i+15]):              # Sixteenth element to seventh element
                    yesCounter = yesCounter + 1

                #print yesCounter
                if (yesCounter == 8):
                    hypothesisSpace2.append(HypothesisSpace[j:j+16])

        
        del HypothesisSpace[:]
        
    #HypothesisSpace = hypothesisSpace2
    #del hypothesisSpace2[:]
        

    print len(hypothesisSpace2)
    # There are prbably multiple of the same training examples in there so scan through this whole loop and
    # if there is no other value in the whole list like it, append it to a new array

    for element in hypothesisSpace2:
        if element not in HypothesisSpace:
            HypothesisSpace.append(element)

    # This cannot be correct, as it is obvious that the version space should yield all possible combinations
    # of values from 4 binary inputs, and 1 binary output (2^5) = 32
    print (len(HypothesisSpace)/16)
    
    return HypothesisSpace
    
    




    
  

#==============================================================================================================================================================================
# Questions 1 -> 2
# 1) 
input_space = 2**4 # Can be one value, another, or ? for 4 attributes
print (input_space)

# 2)
concept_space = 2**input_space # 2^2^4
print (concept_space)



#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# MAIN CODE

import sys

# Initialise all arrays of attributes with their respective values

'''
genderArray = ["Male", "Female"]
ageArray = ["Young", "Old"]
studentArray = ["Yes", "No"]
previouslyDeclinedArray = ["Yes", "No"]
labelArray = ["high", "low"]
'''

# Array that will hold all of the possible hypothesis
hypothesisSpace = []


# Create the Hypothesis Space from all arrays above
H = createHypothesis()


parsedData = parseFile(['partB.py', '4Cat-Train.labeled'])
transformed_data = convertParsedFile(parsedData)

                                          
version1 = listThenEliminate(transformed_data, H)


# Part 5
# Read the daset file from terminal arguement provided (ie: python partA.py testFileName)
example = sys.argv
parsedDataTerminal = parseFile(example)
print parsedDataTerminal
                                                                

