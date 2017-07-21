# Main program for executing classifiers

import os
import samples
import sys
#import util

USAGE_STRING = """python dataClassifier.py <options>
Examples:   (1) python dataClassifier.py
              - trains the default mostFrequent classifier on the spambase dataset
              using the default 100 training examples and
              then test the classifier on test data
            (2) python dataClassifier.py -c dt -d restaurant.arff -t 10 -s 2 -a max_depth=1
              - would run the DecisionTreeClassifer on 10 training examples from the 
              restaurant dataset, passing the optional parameter max_depth on to the 
              DecisionTreeClassifer, and would test on the remaining 2 examples (the 
              restaurant dataset has only 12 examples!).
             """

def default(str):
    return str + ' [Default: %default]'

def isFloat(s):
    if s.count('.') != 1:
        return False
    a, b = s.split('.')
    return a.isdigit() and b.isdigit()

def parseArgs(str):
    if str == None: return {}
    pieces = str.split(',')
    opts = {}
    for p in pieces:
        if '=' in p:
            key, val = p.split('=')
            if val.isdigit():
                val = int(val)
            elif isFloat(val):
                val = float(val)
        else:
            assert False, 'Cannot parse optional argument:' + p
        opts[key] = val
    return opts


def readCommand( argv ):
    "Processes the command used to run from the command line."
    from optparse import OptionParser
    parser = OptionParser(USAGE_STRING)

    parser.add_option('-c', '--classifier', help=default('The type of classifier'), choices=['mostFrequent', 'nb', 'naiveBayes', 'dt', 'decisionTree', 'stump', 'perceptron', 'mira'], default='mostFrequent')
    parser.add_option('-d', '--data', help=default('Dataset to use'), default='spambase.arff')
    parser.add_option('-t', '--training', help=default('The size of the training set'), default=100, type="int")
    parser.add_option('-s', '--test', help=default("Amount of test data to use"), default=100, type="int")
    parser.add_option('-f', '--features', help=default('Whether to use enhanced features'), default=False, action="store_true")
    parser.add_option('-a','--classifierArgs',dest='classifierArgs',
                      help='Comma separated values sent to classifier. e.g. "opt1=val1,opt2,opt3=val3"')
    parser.add_option('--student-code',
                      dest = 'studentCode',
                      default = default('.'),
                      help = 'path to directory containing extractors and classifiers')

    options, otherjunk = parser.parse_args(argv)
    if len(otherjunk) != 0: raise Exception('Command line input not understood: ' + str(otherjunk))
    args = {}

    # Set up variables according to the command line input.
    print "Doing classification"
    print "--------------------"
    print "data:\t\t\t" + options.data
    print "classifier:\t\t" + options.classifier + (" with arguments: " + options.classifierArgs if options.classifierArgs else '')
    print "use enhanced features?:\t" + str(options.features)
    print "training set size:\t" + str(options.training)
    print "test set size:\t\t" + str(options.test)

    sys.path.insert(0, os.path.abspath(options.studentCode))

    args['classifier'] = options.classifier
    args['classifierArgs'] = parseArgs(options.classifierArgs)

    return args, options




def runClassifier(args, options):
    classifier = args['classifier']
    classifierArgs = args['classifierArgs']

    # import statements here because sys.path may be altered to point
    # to student code

    import featureExtractorsBasic
    import decisionTree

    # Load data
    numTraining = options.training
    numTest = options.test
    if(options.data.endswith('.arff')):
        data, labels = samples.loadARFFDataFile(options.data, numTraining+numTest)
        rawTrainingData, rawTestData = data[:numTraining], data[numTraining:numTraining+numTest]
        trainingLabels, testLabels = labels[:numTraining], labels[numTraining:numTraining+numTest]
        legalLabels = set(trainingLabels)
    else:
        print "Unknown dataset", options.data
        print USAGE_STRING
        sys.exit(2)

    # Load classifier
    if(options.classifier == "dt" or options.classifier == "decisionTree"):
        classifier = decisionTree.DecisionTreeClassifer(legalLabels, **classifierArgs)

    # Load feature extractors
    if (options.data.endswith('.arff')):
        if options.classifier in ['nb', 'perceptron', 'mira']:
            make_binary = True
        else:
            make_binary = False
        extractor = featureExtractorsBasic.IdentityFeatureExtractor(make_binary)


    if options.training <= 0:
        print "Training set size should be a positive integer (you provided: %d)" % options.training
        print USAGE_STRING
        sys.exit(2)

    featureFunction = extractor.extractFeatures

    # Preprocess data
    print "Preprocessing data..."
    map(extractor.preProcess, rawTrainingData)
    extractor.finalizeFeatures()

    assert len(rawTrainingData) == len(trainingLabels)

    # Extract features
    print "Extracting features..."
    trainingData = map(featureFunction, rawTrainingData)
    # validationData = map(featureFunction, rawValidationData)
    testData = map(featureFunction, rawTestData)

    assert len(rawTrainingData) == len(trainingLabels)

    # Conduct training and testing
    print "Training..."
    classifier.train(trainingData, trainingLabels)
    guesses = classifier.classify(trainingData)
    correct = [guesses[i] == trainingLabels[i] for i in range(len(trainingLabels))].count(True)
    print str(correct), ("correct out of " + str(len(trainingLabels)) + " (%.1f%%) on training data.") % (100.0 * correct / len(trainingLabels))


    if len(testData) > 0:
        print "Testing..."
        guesses = classifier.classify(testData)
        correct = [guesses[i] == testLabels[i] for i in range(len(testLabels))].count(True)
        print str(correct), ("correct out of " + str(len(testLabels)) + " (%.1f%%) on test data.") % (100.0 * correct / len(testLabels))
    else:
        print "The test data set is empty."

    # have classifier print out some helpful information
    # classifier.printDiagnostics()


if __name__ == '__main__':
    # Read input
    args, options = readCommand( sys.argv[1:] )
    # Run classifier
    runClassifier(args, options)












# Note: this is a significantly modified version of the dataClassifier.py
# available at http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

# dataClassifier.py
# -----------------
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



