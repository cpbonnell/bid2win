import pandas as pd
import requests, json
from pathlib import Path


class Querent:
    """
    This class handles all the HTTP communication for the project,
    persisting all communications for future analysis.
    """
    
    customers_fp = None
    bids_fp = None
    customers = None
    bids = None
    
    api_key = None
    url = {
        'next_user':'http://34.224.89.130:5000/get_next_user',
        'place_bid': 'http://34.224.89.130:5000/submit_bid',
        'how_am_doing': 'http://34.224.89.130:5000/how_am_i_doing'
    }
    
    def __init__(self, archive_dir, api_key):
        
        self.customers_fp = Path(archive_dir + '/customers.csv')
        self.bids_fp = Path(archive_dir + '/bids.csv')
        
        if self.customers_fp.is_file():
            self.customers = pd.read_csv(self.customers_fp)
        else:
            self.customers = pd.DataFrame()
        
        if self.bids_fp.is_file():
            self.bids = pd.read_csv(self.bids_fp)
        else:
            self.bids = pd.DataFrame()
        
        self.api_key = api_key
    #END
    
    
    
    
    
#END class
