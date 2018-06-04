
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
    
    def max_bid(self, score):
        """
        Return the maximum bid that should be placed for a user with a given score.

        Values taken from analysis of the purchase model's performance conducted in
        purchase_model.ipynb.
        """
        if score < 0.25:
            num = 1.7326895418122046
        elif score < 0.5:
            num = 3.6039537983118612
        else:
            num = 5.481774960380348
        
        return num

    
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
    
    def __init__(self, purchase_model, querent, timescale = 500, initial_increment = 0.50, minimum_increment = 0.001, bids_performed = 0):
        """
        """
        self._timescale = timescale
        self._increment = initial_increment
        self._min_inc = minimum_increment
        self._timestep = bids_performed
        self._qr = querent
        self._mod = purchase_model

        ## We need a minimum of 10 items in the customers table in order for
        ## NearestNeighbors to not throw an error, so if it is lacking that
        ## number, we just bid without really looking. The Querent class keeps
        ## track of everything for us.
        while self._qr.customers.shape[0] < 10:
            usr = self._qr.get_next_user()
            b = self.bid_increment()
            res = self._qr.place_bid(b)
            self._timestep += 1
        
    #END
    
    def temperature(self):
        """
        Get the 'temperature' of the search for the purposes of simulated annealing.
        """
        t = (self._timescale - self._timestep)/self._timescale
        return t if t > 0 else 0

    def bid_increment(self):
        """
        Get the amount that the next bid should be incremented by.
        """
        b = self._increment * self.temperature()
        return b if b > self._min_inc else self._min_inc

    def execute_bid(self):
        """
        """

    #END
    
#END class


class StrategicBidder(Bidder):
    """
    Bidder class that uses a different bidding strategy based on users likelihood of buying.

    The strategy for this class is to look at whether a user is likely to buy, and construct
    a bid based on comparison to bids on similar users in the past. The class chooses an 
    aggressive, balanced, or low-ball strategy based on whether the model thinks the iser is
    highly likely, uncertian or not likely to purchase.

    To help fill out the data quickly, the class starts off placing a number of random 
    "exploratory" bids early on in the bidding process. As bidding progresses it places fewer
    and fewer exploratory bids.
    """
    
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
