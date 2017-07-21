import classificationMethod
import math
import util
import collections
from functools import partial
import operator

class DecisionTreeClassifer(classificationMethod.ClassificationMethod):
    '''
    Decision tree classifer.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to raw data such as that produced by the loadXXX functions in samples.py).
    '''

    def __init__(self, legalLabels, max_depth=5):  # feel free to change default max_depth
        self.legalLabels = legalLabels
        self.max_depth = max_depth 
        self.root = None       # training should replace this with root of decision tree!
        self.queue = []
        self.trainingLabeled_data = []
        self.features= []
        "*** YOUR CODE HERE ***"
        # initialize any data structures here

    def build_tree(self, inputs, split_candidates= None):
        # if this is our first pass,
        # all keys of the first input are split candidates
        if split_candidates is None:
            split_candidates = inputs[0][0].keys()

        # count Trues and Falses in the inputs
        num_inputs = len(inputs)
        label_dict = {}
        #num_trues = len([label for item, label in inputs if label=='yes'])
        for item, label in inputs:
            if label in label_dict:
                label_dict[label]+=1
            else:
                label_dict[label] =1

        #num_falses = num_inputs - num_trues
        #print inputs
        #print num_inputs, num_trues, num_falses
        #print label_dict
        for entry in label_dict:
            if label_dict[entry] == num_inputs:
                return entry
        #if num_trues == 0: return False  # no Trues? return a "False" leaf
        #if num_falses == 0: return True  # no Falses? return a "True" leaf

        if not split_candidates:  # if no split candidates left
            return max(label_dict.iteritems(), key=operator.itemgetter(1))[0]  # return the majority leaf

        # otherwise, split on the best attribute
        best_attribute = min(split_candidates, key=partial(self.partition_entropy_by, inputs))

        partitions = self.partition_by(inputs, best_attribute)
        new_candidates = [a for a in split_candidates
                          if a != best_attribute]

        # recursively build the subtrees
        subtrees = {attribute_value: self.build_tree(subset, new_candidates)
                    for attribute_value, subset in partitions.iteritems()}

        subtrees[None] = max(label_dict.iteritems(), key=operator.itemgetter(1))[0]  # default case
        #print best_attribute
        #print subtrees
        #print "building tree"
        return (best_attribute, subtrees)

    def train(self, trainingData, trainingLabels):
        '''
        Train the decision tree on training data.
        '''
        # might be useful in your code later...
        # this is a list of all features in the training set.
        self.features = list(set([ f for datum in trainingData for f in datum.keys() ]))

        "*** YOUR CODE HERE ***"
        #print "in training code........"
        for i in range(len(trainingData)):
            entry = (trainingData[i],trainingLabels[i])
            self.trainingLabeled_data.append(entry)
        #print "in training code........"
        self.root = self.build_tree(self.trainingLabeled_data)
        #print "in training code........2"
        #self.root = decision_node()
        ##feat, splitingvalue = self.splitOnFeat(trainingData, trainingLabels, features)
        #self.root.set_info(feat, splitingvalue)
        #self.queue.append(self.root)
        #while len(self.queue)>0:
        #    pass
        #util.raiseNotDefined()

    def classify(self, data):
        """
        Classifies each datum by passing it through the decision tree.  

        Expects data to be a list.  Each datum in list is a feature vector (i.e., a dictionary)
        """
        "*** YOUR CODE HERE ***"
        #print "root: ", self.root
        guesses= []
        for datum in data:
            guess = self.classify_helper(self.root, datum)
            guesses.append(guess)
        return guesses

    def classify_helper(self,tree, data):

        # if this is a leaf node, return its value
        #print "tree: ", tree, " type of tree: ", type(tree)
        #print "legalLabels: ", self.legalLabels, " tyep of label: ", type(self.legalLabels)
        if type(tree) == str:
            if tree in self.legalLabels:
                #print "returning tree"
                return tree

        # otherwise this tree consists of an attribute to split on
        # and a dictionary whose keys are values of that attribute
        # and whose values of are subtrees to consider next
        attribute, subtree_dict = tree
        #print "attribute & subtree dict: ", attribute, subtree_dict
        #if attribute in data:
            #print attribute
        subtree_key = data.get(attribute)    # None if input is missing attribute
        #else:
        #    return '0'
        #if not subtree_key:
            #print subtree_key
        #    return '0'
        #print subtree_dict
        #print "subtree_key: ",subtree_key
        if subtree_key not in subtree_dict:   # if no subtree for key,
            subtree_key = None                # we'll use the None subtree
        #if subtree_key in subtree_dict:
        subtree = subtree_dict[subtree_key]   # choose the appropriate subtree
        #else:
        #    return '0'
        return self.classify_helper(subtree, data)       # and use it to classify the input


    def printDiagnostics(self):
        """
        This function is called after the classifier has been trained.  

        It should print the first five levels of the decision tree in a nicely 
        formatted way.  
        """
        "*** YOUR CODE HERE ***"
        self.print_helper(self.root, 0, " ")

    def print_helper(self,  data, indent, attribute):
        if type(data)== dict:
            for entry in data:
                #value, subdata= entry
                if type(data[entry]) == str:
                    print " "*indent,attribute,"=", entry, " ==>"
                    print " "* (indent+5)," Label = ", data[entry]
                else:
                    print " " *indent, attribute, "=", entry, " ==>"
                    self.print_helper(data[entry], (indent+4), " ")
        else:
            attribute_data, input = data
            print " "*indent, "Split on: ", attribute_data
            self.print_helper(input, indent,attribute_data)

    def partition_by(self,inputs, attribute):
        """each input is a pair (attribute_dict, label).
        returns a dict : attribute_value -> inputs"""
        groups = collections.defaultdict(list)
        #print "inputs", inputs
        for input in inputs:

            #print "input", input
            #print attribute
            key = input[0][attribute]  # get the value of the specified attribute
            groups[key].append(input)  # then add this input to the correct list
        #print "keys: ",groups.keys()
        #print "values: ", groups.values()
        return groups

    def partition_entropy_by(self,inputs, attribute):
        """computes the entropy corresponding to the given partition"""
        partitions = self.partition_by(inputs, attribute)
        return self.partition_entropy(partitions.values())

    def partition_entropy(self,subsets):
        """find the entropy from this partition of data into subsets
        subsets is a list of lists of labeled data"""

        total_count = sum(len(subset) for subset in subsets)

        return sum(self.data_entropy(subset) * len(subset) / total_count
                   for subset in subsets)

    def data_entropy(self,labeled_data):
        #print "labeled_data: ", labeled_data
        #for i in labeled_data:
        #    print i
        labels = [label for _, label in labeled_data]
        #print "labels: ", labels
        probabilities = self.class_probabilities(labels)
        #print probabilities
        #print self.entropy(probabilities)
        return self.entropy(probabilities)

    def class_probabilities(self,labels):
        total_count = float(len(labels))
        #print total_count
        #print "class prob", [count / total_count
        #        for count in collections.Counter(labels).values()]
        return [count / total_count
                for count in collections.Counter(labels).values()]

    def entropy(self,class_probabilities):
        """given a list of class probabilities, compute the entropy"""
        return sum(-p * math.log(p, 2)
                   for p in class_probabilities
                   if p)


"""
You may find it helpful to create additional classes/functions
such as making a DecisionNode class that represents a single 
node in the decision tree.
"""



