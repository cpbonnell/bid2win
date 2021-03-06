import pandas as pd
import requests, json
from pathlib import Path

from sklearn.neighbors import NearestNeighbors

import utils


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
        
        self.customers_fp = Path(archive_dir + '/customers.csv').as_posix()
        self.bids_fp = Path(archive_dir + '/bids.csv').as_posix()
        
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
        self.customers = self.customers.append(df_response)
        self.customers.to_csv(self.customers_fp)
        
        
        return df_response
    #END
    
    
    def place_bid(self, bid, user_id = None):
        
        ## First handle the case where we have lost data and need to bid
        ## on someone listed in an error
        if user_id is not None:
            payload = {
                'api_key':self.api_key,
                'user_id':user_id,
                'bid_amount':bid
            }
            response = requests.post(self.url['place_bid'], json = payload)
            json_response = json.loads(response.text)
            return json_response
        #END emergency handling
        
        ## Start by grabbing the user we need to place a bit on...
        #for_bid_ix = self.customers.bid < 0
        #for_bid = self.customers.loc[for_bid_ix, :]
        for_bid = self.up_for_bid()
        if for_bid.shape[0] > 1:
            raise ValueError('The number of customers needing a bid is greater than 1. Please repair table.')
        elif for_bid.shape[0] < 1:
            raise ValueError('No customers currently need a bid. Please use get_nextuser().')
        
            
        
        ## Construct the payload
        ind = for_bid.index[0]
        payload = {
            'api_key':self.api_key,
            'user_id':for_bid.loc[ind, 'user_id'],
            'bid_amount':bid
        }
        
        ## Send the bid and record the results
        response = requests.post(self.url['place_bid'], json = payload)
        json_response = json.loads(response.text)
        
        ## Handle errors:
        if json_response['result'] != 'success':
            return json_response
        
        ## Package the results, add to the data frame
        df_response = pd.DataFrame(json_response, index = [ind])
        
        ## Put the relevant info in the customers table
        self.customers.loc[ind, 'bid'] = bid
        self.customers.loc[ind, 'win'] = json_response['win']
        self.customers.loc[ind, 'profit'] = 0
        
        if json_response['win'] == True and json_response['purchase'] == True:
            self.customers.loc[ind, 'profit'] = json_response['profit']
        
        
        self.bids = self.bids.append(df_response)
        
        self.customers.to_csv(self.customers_fp)
        self.bids.to_csv(self.bids_fp)
        
        return df_response
    #END
    
    
    def get_progress(self):
        
        response = requests.post(self.url['how_am_doing'], json = {'api_key':self.api_key})
        json_response = json.loads(response.text)
        return json_response
    
    def get_comps(self, user_id = None, n = 6):
        """
        Get a data frame of the n most similar users to the one currently up
        for bid (or another if specified)
        """

        ## Look up the customer who is up for bid and calculate their features.
        if user_id is None:
            user = self.up_for_bid()
        else:
            match_ind = self.customers.user_id == user_id
            user = self.customers.loc[match_ind, :]
            if user.shape[0] == 0:
                raise ValueError('No users matching the specified user_id')
        
        user_feat = utils.frame_to_features(user)

        ## Make a NearestNeighbors finder to do the lookup for us
        no_bid = self.not_up_for_bid()
        no_bid_feat = utils.frame_to_features(no_bid)
        nbf = NearestNeighbors(n_neighbors = n)
        nbf.fit(no_bid_feat)

        ## Now use the neighbor finder to get indices (positional, not from df.index)
        ind = nbf.kneighbors(user_feat, return_distance=False).flatten()

        ## The indices we have are NOT from the actual existing indices of the df, but
        ## a relative index of position
        df = self.customers.iloc[ind]

        return df
    
    def up_for_bid(self):
        """
        Return the record of the user record currently up for bid.

        Return None if there is no user up for bid.
        """
        for_bid_ind = self.customers.bid < 0
        for_bid_df = self.customers.loc[for_bid_ind, :]
        
        return for_bid_df

    def not_up_for_bid(self):
        """
        Return the customers data frame, minus any customer(s) currently
        up for bid.
        """
        for_bid_ind = self.customers.bid < 0
        for_bid_df = self.customers.loc[~for_bid_ind, :]
        
        return for_bid_df

#END class
