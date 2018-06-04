
import utils
import pickle
from random import random
from sklearn.neighbors import NearestNeighborss

import querents
import strategies



class Bidder:
    """
    Parent bidder class for other types of bidder.

    NOTE: Consider removing this if it looks unneeded after further work
       on concrete classes.
    """
    
    def execute_bid(self):
        raise NotImplementedError
    
#END class


class AnnealingBidder(Bidder):
    """
    Bidder class that starts low and increases bid over time.
    
    The strategy for this bidder is to start bidding very low on all users, and increase
    bids as time goes on. Bidding stops when either a) we start winning bids for this type
    of user, or b) we reach our threshhold above which we think this kind of user will
    just not be profitable.
    
    The amount by which we raise the bid each time should go down over time, allowing the
    algorithm to settle into a steady pattern of bidding.
    """
    
    def __init__(self, purchase_model, querent, timescale = 500):
        """
        """
        self._timescale = timescale
        self._qr = querent
        self._mod = purchase_model
        
    #END
    
    
#END class


class StrategicBidder(Bidder):
    
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
        comps = self.qr.customers.iloc[ind].sort_values(['bid']).loc[:, ['bid', 'win']]
        
        ## Step 5: Use buy-prob to select a strategy
        
        ## First see if we need to explore
        if self.explore():
            upper = 10 if buy_prob > 0.8 else 6
            strat = strategies.random_bid(upper_bound = upper)
        else:
            #TODO: Finish implementing this class
            pass
        
        
        ## Step 6: Use the strategy function to calculate a bid amount
        
        ## Step 7: Place the bid
        
    #END
    
    
#END class
