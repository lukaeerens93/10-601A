import numpy as np
import math
import csv
import sys

#=================================== Data Preprocessing =================================
def parseLabel(labelset):
    lbl = labelset.splitlines()
    for row in lbl:
        l = row.split('\n')
        if l[0] == 'yes':
            labels.append(1)
        if l[0] == 'no':
            labels.append(0)
    return labels

def parseData(Dataset, inp_vec):
    fst = True
    for row in Dataset:
        # If got passed the collumn names
        if fst == False:
            for i in range(0, len(row), 4):
                inp_vec.append(float(row[i]))
                inp_vec.append(float(row[i+1]))
                if (row[i+2] == 'yes'):
                    inp_vec.append(1.0)
                if (row[i+2] == 'no'):
                    inp_vec.append(0.0)
                    
                if (row[i+3] == 'yes'):
                    inp_vec.append(1.0)
                if (row[i+3] == 'no'):
                    inp_vec.append(0.0)             
        # First row is names only
        if fst == True:
            fst = False
            continue
    return inp_vec

def normaliseData(input_vec):
    #normalisation: (x - in_min) * (out_max - out_min)
    for i in range(0, len(input_vec), 4):
        input_vec[i] = float(float(input_vec[i]) - 1900)/float(2000-1900)
        input_vec[i+1] = float(float(input_vec[i]) - 0)/float(7-0)
    return input_vec 


#=================================== Data Preprocessing =================================

# Number of units in the hidden layer: Try first with 5 + bias
# Network connectivity: Fully Connected

'''
Network:
4 inputs,           5 weights to each node,                7 weights to each node
Input (1*4):            Hidden Layer (5*5)                      Output (6*1):
                                  
                    [w1_1,w2_1,w3_1,w4_1,wBias1_1]
[1]                 [w1_2,w2_2,w3_2,w4_2,wBias1_2]              
[2]                 [w1_3,w2_3,w3_3,w4_3,wBias1_3]           [w1_1,w2_1,w3_1,w4_1,w5_1,wB2_1] = Yes or No
[3]                 [w1_4,w2_4,w3_4,w4_4,wBias1_4]           
[4]                 [w1_5,w2_5,w3_5,w4_5,wBias1_5]
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
            weights[i] = np.random.normal(loc = 0, scale = 0.1, size = (5,))        # 5 weights (4 input nodes + 1 bias) from input to 5 hidden nodes excluding the bias
    if (len(weights) == 1):
        weights[0] = np.random.normal(loc = 0, scale = 0.1, size = (6,))            # 6 weights from hidden to output (5 hidden nodes + 1 bias)
    '''
    # These intialized random weights seem to perform best
    if (len(weights) == 5):
        weights[0] = np.array([0.18608089, -0.03129441, -0.10320558,  0.03309806, -0.04963245])
        weights[1] = np.array([0.01035584,  0.00266096, -0.07877621,  0.16897222, -0.13473166])
        weights[2] = np.array([-0.04365084, -0.04689223,  0.06010894, -0.073003  , -0.0058238 ])
        weights[3] = np.array([-0.00259586,  0.08761321,  0.09400949,  0.27440824,  0.06528786])
        weights[4] = np.array([0.16547524,  0.03254001, -0.04997804,  0.03414878,  0.01424539])
    if (len(weights) == 1):
        weights[0] = np.array([-0.21735425,  0.06123535,  0.09409971,  0.06574627,  0.01083311, -0.02812257])
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
        for i in range(0, len(inputs), 4):
            j = 0           # j is here because u want to append to a different index of the vector that outputs the result of hidden layer
            for w_Vec in weights:       # For weights of all connections to each node                                         # 1 is a bias
                sumVec[j] = sigmoid(w_Vec[0]*inputs[i] + w_Vec[1]*inputs[i+1] + w_Vec[2]*inputs[i+2] + w_Vec[3]*inputs[i+3] + w_Vec[4]*1.0) # Last part is the weighed bias
                j = j + 1   

    # if output layer
    if (len(weights) == 1):
        sumVec = [0]              
        for w_Vec in weights:                                                        
            sumVec[0] = sigmoid(w_Vec[0]*inputs[0] + w_Vec[1]*inputs[1] + w_Vec[2]*inputs[2] + w_Vec[3]*inputs[3] + w_Vec[4]*inputs[4] + w_Vec[5]*1.0)      
    return sumVec
    
        
    
def forward_pass(inputs2hidden, weights2hidden, weights2out):

    # Pass values through hidden layer
    out_hidden = weighedSum(inputs2hidden[0:4], weights2hidden)                                  # (1)
    
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

    # ------------------- ERROR COULD LIE OVER HERE TOO ARE U SURE THAT YOUR ERRORVECHIDDEN[5] IS CORRECT
    for i in range(0, len(sig_hidden), 1):
        #print i
        errorVecHidden[i] = diff_sigmoid(sig_hidden[i]) * sum_of_weighed_errors
    errorVecHidden[5] = 1+ sum_of_weighed_errors #////// you can't add diff_sigmoid over here because a bias doesn't come from a sigmoid... so what do you use instead
    # The above part is probably not correct, what you might need to do is probably use the weight of that one sigmoid output
    


    # 3) Update the network weights
    # outer layer:
    for x in range(0, len(W_Output[0])-1, 1):   # len-2 because you have more sigmoid activations than inputs in hidden layer (bias is 1 and not the result of a sigmoid)
        W_Output[0][x] = W_Output[0][x] - learning_rate * ErO * sig_hidden[x]
    W_Output[0][len(W_Output[0])-1] = W_Output[0][x] - learning_rate * ErO * 1
    
    # hidden layer:
    for x in range(0, len(W_hidden), 1):

        for y in range(0, len(W_hidden[x])-1,1):

            W_hidden[x][y] = W_hidden[x][y] - learning_rate * errorVecHidden[x] * input_attributes[y]
        W_hidden[x][len(W_hidden[x])-1] = W_hidden[x][len(W_hidden[x])-1] - learning_rate * errorVecHidden[len(W_hidden)-1] * 1

    

    
#================================================  Main Code ================================================ 


output_hidden = [0,0,0,0,0,0]     # Contains sigmoids of sums for each node, and the single 1 value of the bias

error = 0       # Get updated as the code runs

learning_rate = 0.15

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
normal_input = normaliseData(Input)                 # Normalise
raw_data.close()

# Get testing data
input_vector_test = []                                                                                  # Array: Input
raw_data2 = open(testfilename, "rb")
data2 = csv.reader(raw_data2, delimiter = ',')
Input2 = parseData(data2, input_vector_test)        # Store data in memory
normal_input2 = normaliseData(Input2)               # Normalise
raw_data2.close()
    
# Initialise Weights
weight_vector_to_hidden = [0,0,0,0,0]     # 0s converted later in weight_init()             # Array: weight matrix to hidden layer
weight_vector_to_output = [0]                                                               # Array: weight matrix to output layer
w1 = weight_init(weight_vector_to_hidden)
w2 = weight_init(weight_vector_to_output)
'''
print ("w1:" + str(w1))
print ("w2 " + str(w2))
'''

iteration = 0

# ------------ TRAINING ------------
while( iteration < 4500):

    TotalLoss = 0
    
    for i in range(0, len(normal_input), 4):
        
        # Forward Pass-----------
        activationHidden, activationOutput = forward_pass(normal_input[i:i+4], w1, w2)
        
        # Computer Error of the forward pass
        E = loss(activationOutput, labels[i/4])
        TotalLoss += E
        
        # Backpropagate
        back_prop(normal_input[i:i+4], activationHidden, activationOutput, labels[i/4], w1, w2)

    print (TotalLoss)
    
    iteration = iteration + 1

print ("TRAINING COMPLETED! NOW PREDICTING.")    
    

# ------------ TESTING ------------
for i in range(0, len(normal_input2), 4):
    #print normal_input2[i:i+4]
    
    # Forward Pass-----------
    activationHidden, activationOutput = forward_pass(normal_input2[i:i+4], w1, w2)
    
    # Computer Error of the forward pass
    if (activationOutput[0] < 0.5):
        print "no"
    if (activationOutput[0] > 0.5):
        print "yes"

