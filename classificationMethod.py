# This file contains the abstract class ClassificationMethod

class ClassificationMethod:
    """
    ClassificationMethod is the abstract superclass of
     - MostFrequentClassifier
     - NaiveBayesClassifier
     - DecisionTreeClassifer
     - and possibly others...

    As such, you need not add any code to this file.  You can write
    all of your implementation code in the files for the individual
    classification methods listed above.
    """
    def __init__(self, legalLabels):
        """
        For digits dataset, the set of legal labels will be 0,1,..,9
        For faces dataset, the set of legal labels will be 0 (non-face) or 1 (face)
        """
        self.legalLabels = legalLabels

    def train(self, trainingData, trainingLabels):
        """
        This is the supervised training function for the classifier.  The inputs 
        trainingData and trainingLabels are parallel lists meaning that trainingData[i]
        is the ith input example and trainingLabels[i] is its associated label.

        Each datum in trainingData is a dictionary mapping feature names to feature values.
        """
        abstract

    def classify(self, data):
        """
        This function returns a list of labels, each drawn from the set of legal labels
        provided to the classifier upon construction.

        Each datum in data is a dictionary mapping feature names to feature values.
        """
        abstract

    def printDiagnostics(self):
        """
        This function is called after the classifier has been trained.  

        It should print helpful diagnostic information such as an analysis of the features.
        """
        abstract














# classificationMethod.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# Note: this is a modified version of the code available from
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html