#Homework 1
#---- Remember that this program should not be run from IDLE but from terminal:
#---- go to directory where files are and enter: python hw1b.py input.txt

import sys

# Void function that reads the name of the file as input
def readFromFile(filename):

        
    # OPEN the file as read only
    txtFile = open(filename[1], 'r')

    # READ the file, split the lines up and print each line
    content = txtFile.read()

    # Split up file into lines
    splitContent = content.splitlines()

    # Within each line split up string based on presence of \n
    allHashtagThingies = []
    for lines in splitContent:
        subsplits = lines.split(r'\n')
        reverseOfLineContent = subsplits[: :-1]
        allHashtagThingies.append(reverseOfLineContent)

    # Reverse order of string components
    reversed = allHashtagThingies[: :-1]
    
    # Print everything back in standard output
    array = []
    for i in reversed:
        for j in i:
            print j
            
    # Close file after read            
    txtFile.close()

#==================================================================    

# Main Code:

# read the arguements from terminal:
# ie: python hw1b.py example.txt
#
# the input.txt is the arguement in question (sys.argv)

example = sys.argv

readFromFile(example)

