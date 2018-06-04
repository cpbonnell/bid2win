
import utils
import pickle
from random import random
from sklearn.neighbors import NearestNeighborss

import querents

class Bidder:
    
    _bids_placed = 0
    
    _explore_prob = 1
    _rate = 0.001
    
    def __init__(self, model_dir, api_key, explore_prob = 1, exploitation_rate = 0.001, bids_placed = 0):
        
        self._model = pickle.load(open(model_dir + '/model.p', 'rb'))
        self.qr = querents.Querent(model_dir, api_key)
        
        self._bids_placed = bids_placed
        self._explore_prob = explore_prob
        self._rate = exploitation_rate
    
    
    def explore(self):
        """
        Returns True if this round should be an exploration round, False if
        this round should exploit available knowledge.
        """
        num = random()
        expl = num < self._explore_prob
        
        self._explore_prob -= _rate
        
        return expl
    
    
    def execute_bid(self):
        """
        Go through the whole process of getting a user, analysing the data
        and placing a bid based on the analysis.
        """
        
        ## Step 0: Initialization
        previous_feat = frame_to_features(self.qr.customers)
        nb = NearestNeighbors(n_neighbors = 10)
        
        
        
        ## Step 1: Get a user
        user = self.qr.get_next_user()
        
        ## Step 2: put the data into form for a model
        user_feat = utils.frame_to_features(user)
        
        ## Step 3: Use model to get an estimate of how likely to buy the individual is
        buy_prob = self._model.predict(user_feat)
        
        ## Step 4: Look up previous bids on comparable users
        ind = nb.kneighbors(user_feat,  return_distance=False).flatten()
        comps = self.qr.customers.iloc[ind]
        
        ## Step 5: Use buy-prob to select a strategy
        
        ## First see if we need to explore
        #if self.explore():
        #    recommended_bid = 
        
        
        ## Step 6: Use the strategy function to calculate a bid amount
        
        ## Step 7: Place the bid
        
    #END
    
    
#END class
