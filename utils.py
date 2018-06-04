import pandas as pd
import numpy as np


def frame_to_features(df):
    """
    Take a 'customers' data frame of one or more rows and
    construct features ready for sklearn. Superfluous columns
    will be ignored, bit there will of course be an error if
    the required columns are missing.
    """
    features = pd.DataFrame(index = df.index)
    
    features['sunday'] = (df['day_of_week'] == 'Sunday').astype(np.float64)
    features['monday'] = (df['day_of_week'] == 'Monday').astype(np.float64)
    features['tuesday'] = (df['day_of_week'] == 'Tuesday').astype(np.float64)
    features['wednesday'] = (df['day_of_week'] == 'Wednesday').astype(np.float64)
    features['thursday'] = (df['day_of_week'] == 'Thursday').astype(np.float64)
    features['friday'] = (df['day_of_week'] == 'Friday').astype(np.float64)
    features['saturday'] = (df['day_of_week'] == 'Saturday').astype(np.float64)
    features['female'] = (df['gender'] == 'F').astype(np.float64)
    features['marital_status'] = (df['marital_status'] == 'M').astype(np.float64)
    features['age'] = (df['age'] - df.age.mean()) / df.age.std()
    features['income'] = (df['income'] - df.income.mean()) / df.income.std()
    
    return reatures
#END
