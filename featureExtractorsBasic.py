import util

class FeatureExtractor:
    """
    FeatureExtractor is an abstract superclass.

    As such, you need not add any code to this file.  You can write
    enhanced extractors in featureExtractors.py
    """
    def __init__(self):
        """
        Initialize data structures before any data is seen.
        """
        pass

    def preProcess(self, datum):
        """
        This function is called on each training datum.  This function can be 
        used to update data structures based on each datum in training data. 
        Should returns None.
        """
        pass

    def finalizeFeatures(self):
        """
        Called after all training data has been pre-processed.
        """
        pass

    def extractFeatures(self, datum):
        """
        This function is called on each training datum.  This function 
        should return a dictionary of features.
        """
        abstract


class IdentityFeatureExtractor(FeatureExtractor):
    '''
    Handles data that comes in feature form (dict of attribute-value pairs).  
    Has the option of transforming into binary features: the feature 
    would be attribute=value for each possible value.

    Example of binary featurization:
    Suppose datum is {'gender':'female', 'age':25} then the binary features
    would be { 'gender=female':1.0, 'age=25':1.0 } with all other ages and
    genders being implicitly zero.
    '''
    def __init__(self, make_binary = False):
        self.make_binary = make_binary

    def extractFeatures(self, datum):
        if self.make_binary:
            binaryFeatures = util.Counter()
            for feature,value in datum.items():
                binaryFeatures['{0}={1}'.format(feature, value)] = 1.0
            return binaryFeatures
        return datum


