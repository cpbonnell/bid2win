
import utils
import pickle

import querents

class Bidder:
    
    def __init__(self, model_dir):
        
        self._model = pickle.load(open(model_dir + '/model.p', 'rb'))
        self.qr = querents.Querent(model_dir)
    
    
    
    def execute_bid(self):
        """
        Go through the whole process of getting a user, analysing the data
        and placing a bid based on the analysis.
        """
        
        
        
    #END
    
    
#END class
