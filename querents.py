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
            self.customers = pd.read_csv(self.customers_fp, index_col = 0)
        else:
            self.customers = pd.DataFrame()
        
        if self.bids_fp.is_file():
            self.bids = pd.read_csv(self.bids_fp, index_col = 0)
        else:
            self.bids = pd.DataFrame()
        
        self.api_key = api_key
    #END
    
    def get_next_user(self):
        payload = {'api_key': self.api_key}
        
        ## Query the server, and unpack the JSON to a dict
        response = requests.post(self.url['next_user'], json = payload)
        json_response = json.loads(response.text)
        
        ## Handle errors:
        if json_response['result'] == 'failure':
            return json_response
        
        ## Convert the dict to a data frame, using the appripriate index, and
        ## making sure there is space to record the bid
        json_response['bid'] = -1
        ind = json_response['user_index']
        df_response = pd.DataFrame(json_response, index = [ind])
        
        ## Append the data frame to the list of users already known, and
        ## persist the new data frame
        self.customers.append(df_response)
        self.customers.to_csv(self.customers_fp)
        
        
        return df_response
    #END
    
    
    def place_bid(self, bid):
        pass
        
    #END
    
    
#END class
