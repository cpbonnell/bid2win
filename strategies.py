
from random import random



def random_bid(lower_bound = 0, upper_bound = 10):
    """
    Return a recommender that gives random number between the two bounds
    """
    def f():
        return random()*(upper_bound - lower_bound) + lower_bound
    
    return f



def aggressive_bid(prob, comps):
    """
    Returns a recommender that bids aggressively for the given user.
    
    The strategy for this function is to look at the comps and select the smallest bid
    for a comparable user that has not already been outbid.
    """
    
    ## If the top bid is a loss, then we need to bid higher
    low = None
    high = None
    if comps.iloc[0].win == False:
        bid = compl.iloc[0].bid + random()
    else:
        for i in range(comps.shape[0]):
            high = low
            low = comps.iloc[i].bid
            #TODO: finish this logic & test it
            
    
    def f():
        num = bid if bid < 8 else 8
        
        return num
    
    return f