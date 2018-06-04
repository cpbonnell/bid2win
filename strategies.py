
from random import random



def random_bid(lower_bound = 0, upper_bound = 10):
    """
    Return a random number between the two bounds
    """
    def f():
        return random()*(upper_bound - lower_bound) + lower_bound
    
    return f


