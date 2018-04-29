import numpy as np
import math
import csv
import sys

#=================================== Data Preprocessing =================================
def parseLabel(labelset):
    lbl = labelset.splitlines()
    for row in lbl:
        l = row.split('\n')
        # Each label lies b/w 0 and 100 and so normalized by diving by 100
        labels.append(float(l[0])/float(100))
    return labels

def parseData(Dataset, inp_vec):
    fst = True
    for row in Dataset:
        # If got passed the collumn names
        if fst == False:
            for i in range(0, len(row), 6):
                inp_vec.append(float(row[i])/float(100))
                inp_vec.append(float(row[i+1])/float(100))
                inp_vec.append(float(row[i+2])/float(100))
                inp_vec.append(float(row[i+3])/float(100))
                inp_vec.append(float(row[i+4])/float(100))

        # First row is names only
        if fst == True:
            fst = False
            continue  
    return inp_vec


#=================================== Data Preprocessing =================================

# Number of units in the hidden layer: Try first with 5 + bias
# Network connectivity: Fully Connected

'''
Network:
4 inputs,           5 weights to each node,                7 weights to each node
Input (1*4):            Hidden Layer (5*5)                      Output (6*1):
                                  
[1]                 [w1_1,w2_1,w3_1,w4_1,wBias1_1]
[2]                 [w1_2,w2_2,w3_2,w4_2,wBias1_2]              
[3]                 [w1_3,w2_3,w3_3,w4_3,wBias1_3]           [w1_1,w2_1,w3_1,w4_1,w5_1,wB2_1] = Yes or No
[4]                 [w1_4,w2_4,w3_4,w4_4,wBias1_4]           
[5]                 [w1_5,w2_5,w3_5,w4_5,wBias1_5]
[bias1 = 1.0]                      [bias2 = 1.0]
                                  
You also have: 2 additional vectors for weighted sum only these being:
[6 elements long for input  -> hidden... with an additional 7th element for the bias of 1]
[2 elements long for hidden -> output... with an additional 3rd element for the bias of 1]
'''

# Initialise the weights
def weight_init(weights):
    '''
    if (len(weights) == 5):
        for i in range(0, len(weights), 1):
            weights[i] = np.random.normal(loc = 0, scale = 0.15, size = (6,))        # 6 weights (5 input nodes + 1 bias) from input to 5 hidden nodes excluding the bias
    if (len(weights) == 1):
        weights[0] = np.random.normal(loc = 0, scale = 0.15, size = (6,))            # 6 weights from hidden to output (5 hidden nodes + 1 bias)
    '''
    # These intialized random weights seem to perform best
    if (len(weights) == 5):
        weights[0] = np.array([ 0.21703038,  0.10704256, -0.13586394,  0.03636778,  0.15685674, -0.0223433 ])
        weights[1] = np.array([-0.06740402, -0.12525631, -0.13574764,  0.01592027,  0.24001636, -0.26669211])
        weights[2] = np.array([-0.01184921, -0.23604243, -0.18108271,  0.00425088,  0.21076315, -0.06017267])
        weights[3] = np.array([-0.0279291 , -0.13001513,  0.14562383,  0.08247737, -0.22131027, 0.06595536])
        weights[4] = np.array([-0.05658501,  0.11115274,  0.19716727, -0.03655446, -0.10204568, -0.14348928])
    if (len(weights) == 1):
        weights[0] = np.array([ 0.12580798, -0.0763356 , -0.112926  , -0.15041116, -0.04293949, -0.13333615])
    
    return weights



# Activation Function
def sigmoid(val):
    return 1/(1 + np.exp(-val))

# Derrivate of the Activation function (used in gradient descent and backpropagation)
def diff_sigmoid(sig):
    d_sigmoid = sig*(1-sig)
    return d_sigmoid

# Error
def loss(output, label):
    # if label is 1 it is 0.5(1-ffwOutput)^ 2 and if label is 0 it is 0.5(1-ffwOutput)^ 2
    error = 0.5*(label - output[0])*(label - output[0])
    return error

def diff_loss(output, label):
    # Derivative of 0.5(t-x)^2 wrt to x is 2*0.5(t-x) * (-1) = -(t-x)
    d_error = -(label - output[0])
    return d_error
    

# Weighted sum
def weighedSum(inputs, weights):                                                                       # (1)

    # if middle layer:
    if (len(weights) == 5):
        sumVec = [0,0,0,0,0]              # Vector that holds all the weighted sums
        # For each vector of weights in the layer (vector of weights represent weights inputs to THAT ONE NODE)
        for i in range(0, len(inputs), 5):
            j = 0           # j is here because u want to append to a different index of the vector that outputs the result of hidden layer
            for w_Vec in weights:       # For weights of all connections to each node                                         # 1 is a bias
                #print w_Vec
                #print inputs
                sumVec[j] = sigmoid(w_Vec[0]*inputs[i] + w_Vec[1]*inputs[i+1] + w_Vec[2]*inputs[i+2] + w_Vec[3]*inputs[i+3] + w_Vec[4]*inputs[i+4] +w_Vec[5]*1.0) # Last part is the weighed bias
                j = j + 1   

    # if output layer
    if (len(weights) == 1):
        sumVec = [0]              
        for w_Vec in weights:
            
            sumVec[0] = sigmoid(w_Vec[0]*inputs[0] + w_Vec[1]*inputs[1] + w_Vec[2]*inputs[2] + w_Vec[3]*inputs[3] + w_Vec[4]*inputs[4] + w_Vec[5]*1.0)      
    return sumVec
    
        
    
def forward_pass(inputs2hidden, weights2hidden, weights2out):

    # Pass values through hidden layer
    out_hidden = weighedSum(inputs2hidden[0:5], weights2hidden)                                  # (1)
    
    # pass values through output
    out_out = weighedSum(out_hidden, weights2out)

    return out_hidden, out_out



def back_prop(input_attributes, sig_hidden, sig_output, T, W_hidden, W_Output):

    # A thing to remember is that the length of the sig_hidden is 1 for output and 5 for input... Why because you have 5 nodes in
    # hidden layer + the bias (which has nothing connected to it. and you have 1 input node. 
    
    # 1) For single output unit at the end of the network, calculate the error term output (ErO)
    ErO = diff_sigmoid(sig_output[0]) * diff_loss(sig_output,T)

    
    # 2) For each hidden unit, calcualte its error term
    errorVecHidden = [0,0,0,0,0,0]
    sum_of_weighed_errors = 0
    for weights in W_Output[0]:
        sum_of_weighed_errors += weights*ErO

 
    for i in range(0, len(sig_hidden), 1):
        #print i
        errorVecHidden[i] = diff_sigmoid(sig_hidden[i]) * sum_of_weighed_errors
    errorVecHidden[5] = 1+ sum_of_weighed_errors #////// you can't add diff_sigmoid over here because a bias doesn't come from a sigmoid... so what do you use instead
    

    # 3) Update the network weights
    
    # outer layer:
    for x in range(0, len(W_Output[0])-2, 1):   # len-2 because you have more sigmoid activations than inputs in hidden layer (bias is 1 and not the result of a sigmoid)
        W_Output[0][x] = W_Output[0][x] - learning_rate * ErO * sig_hidden[x]
    W_Output[0][len(W_Output[0])-1] = W_Output[0][x] - learning_rate * ErO * 1

    
    # hidden layer:
    for x in range(0, len(W_hidden), 1): # For each hidden unit
        for y in range(0, len(W_hidden[x])-2,1):    # for each weight going to that hidden unit

            W_hidden[x][y] = W_hidden[x][y] - learning_rate * errorVecHidden[x] * input_attributes[y]
            
        W_hidden[x][len(W_hidden[x])-1] = W_hidden[x][len(W_hidden[x])-1] - learning_rate * errorVecHidden[len(W_hidden)-1] * 1

    

    
#================================================  Main Code ================================================ 


output_hidden = [0,0,0,0,0,0]     # Contains sigmoids of sums for each node, and the single 1 value of the bias

error = 0       # Get updated as the code runs

learning_rate = 0.1

filename = sys.argv
trainingfilename = filename[1]
labelfilename = filename[2]
testfilename = filename[3]

# Get labels
labels = []                                                                                             # Array: label
raw_label = open(labelfilename, "r")
raw = raw_label.read()
labels = parseLabel(raw)                            # Here is the label vector
raw_label.close()

# Get training data
input_vector = []                                                                                       # Array: Input
raw_data = open(trainingfilename, "rb")
data = csv.reader(raw_data, delimiter = ',')
Input = parseData(data, input_vector)               # Store data in memory
raw_data.close()

# Get testing data
input_vector_test = []                                                                                  # Array: Input
raw_data2 = open(testfilename, "rb")
data2 = csv.reader(raw_data2, delimiter = ',')
Input2 = parseData(data2, input_vector_test)        # Store data in memory
raw_data2.close()
    
# Initialise Weights
weight_vector_to_hidden = [0,0,0,0,0]     # 0s converted later in weight_init()           # Array: weight matrix to hidden layer
weight_vector_to_output = [0]                                                               # Array: weight matrix to output layer
w1 = weight_init(weight_vector_to_hidden)
w2 = weight_init(weight_vector_to_output)
'''
print ("w1:" + str(w1))
print ("w2 " + str(w2))
'''
#print len(Input)
iteration = 0

# ------------ TRAINING ------------ (1220 Worked Well)
while( iteration < 1740):

    TotalLoss = 0
    
    for i in range(0, len(Input), 5):
        
        # Forward Pass-----------
        activationHidden, activationOutput = forward_pass(Input[i:i+5], w1, w2)
        
        # Computer Error of the forward pass
        E = loss(activationOutput, labels[i/5])
        TotalLoss += E
        
        # Backpropagate
        back_prop(Input[i:i+5], activationHidden, activationOutput, labels[i/5], w1, w2)

    print (TotalLoss)*100       # MAYBE WE NEED TO MULTPLY OUR TOTAL LOSS BY 100, I have submitted it without, but just added it in last night when i got home!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    iteration = iteration + 1

    if (iteration == 150):
        learning_rate = learning_rate*0.50
        #print ("LEARN: " + str(learning_rate) + "!!!!!!!!!!!!!!!")
    if (iteration == 300):
        learning_rate = learning_rate*0.50
        #print ("LEARN: " + str(learning_rate) + "!!!!!!!!!!!!!!!")
    if (iteration == 450):
        learning_rate = learning_rate*0.50
        #print ("LEARN: " + str(learning_rate) + "!!!!!!!!!!!!!!!")
    if (iteration == 600):
        learning_rate = learning_rate*0.50
        #print ("LEARN: " + str(learning_rate) + "!!!!!!!!!!!!!!!")
    if (iteration == 750):
        learning_rate = learning_rate*0.60
        #print ("LEARN: " + str(learning_rate) + "!!!!!!!!!!!!!!!")
    if (iteration == 900):
        learning_rate = learning_rate*0.70
        #print ("LEARN: " + str(learning_rate) + "!!!!!!!!!!!!!!!")
    if (iteration == 1050):
        learning_rate = learning_rate*0.70
        #print ("LEARN: " + str(learning_rate) + "!!!!!!!!!!!!!!!")
    if (iteration == 1300):
        learning_rate = learning_rate*0.60
        #print ("LEARN: " + str(learning_rate) + "!!!!!!!!!!!!!!!")
    if (iteration == 1450):
        learning_rate = learning_rate*0.4
        #print ("LEARN: " + str(learning_rate) + "!!!!!!!!!!!!!!!")
    if (iteration == 1550):
        learning_rate = learning_rate*0.4
        #print ("LEARN: " + str(learning_rate) + "!!!!!!!!!!!!!!!")
    if (iteration >= 1600 and iteration % 20 == 0):
        learning_rate = learning_rate*0.2
        #print ("LEARN: " + str(learning_rate) + "!!!!!!!!!!!!!!!")
    
          
        
        
    '''    
    if (iteration % 150 == 0):
        learning_rate = learning_rate*0.50
        #print ("LEARN: " + str(learning_rate) + "!!!!!!!!!!!!!!!")
    '''
print ("TRAINING COMPLETED! NOW PREDICTING.")    
    

# ------------ TESTING ------------
for i in range(0, len(Input2), 5):
    #print normal_input2[i:i+4]
    
    # Forward Pass-----------
    activationHidden, activationOutput = forward_pass(Input2[i:i+5], w1, w2)
    
    # Computer Error of the forward pass
    print (activationOutput[0])*100


