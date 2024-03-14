# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 14:33:22 2024

@author: H244746
"""

import pandas as pd
from datetime import datetime
from sklearn.base import BaseEstimator, TransformerMixin


def testfunction():
    return None


class CalculateCustomerAge(BaseEstimator, TransformerMixin):
    """
    A class to calculate the age of a customer that can be used in an sklearn pipeline.

    ...

    Methods
    -------
    transform(X):
        Takes the input dataframe X and calculates the age of the customer.
    """
    def __init__(self):
        None
    # Trivial method to be compatible with Sklearn pipeline
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        """
        Calculates the age of a customer.


        Parameters
        ----------
        X : pd.DataFrame

        Returns
        -------
        df (pd.DataFrame): Pandas data frame with customer age appended.
        """
        
        df = X.copy()
        
        today = datetime.today().strftime('%Y-%m-%d')
        today = pd.to_datetime(today, format = '%Y-%m-%d')
        
        df['CUSTOMER_AGE'] = ((today - pd.to_datetime(df['DATE_OF_BIRTH'], format = '%d-%m-%Y'))).astype('<m8[Y]')
        
        df = df.drop(columns = 'DATE_OF_BIRTH')
        

        return df
    
    
    
    
    
    
    
    
    
class CalculateCreditHistoryLength(BaseEstimator, TransformerMixin):
    """
    A class to calculate a customer's credit history length that can be used in an sklearn pipeline.

    ...

    Methods
    -------
    transform(X):
        Takes the input dataframe X and calculates the credit history length of the customer.
    """
    def __init__(self):
        None
    # Trivial method to be compatible with Sklearn pipeline
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        """
        Calculates the credit history length of a customer.


        Parameters
        ----------
        X : pd.DataFrame

        Returns
        -------
        df (pd.DataFrame): Pandas data frame with customer credit history length appended.
        """
        
        df = X.copy()
        
        credit_history_length = df['CREDIT_HISTORY_LENGTH'].str.split(' ', expand = True)
        
        months_credit_history_length = pd.Series(credit_history_length[1].str.extract('(\d+)')[0]).astype(int)
        years_credit_history_length = pd.Series(credit_history_length[0].str.extract('(\d+)')[0]).astype(int) * 12
        
        df['CREDIT_HISTORY_LENGTH'] = months_credit_history_length + years_credit_history_length
        

        return df
    
    
    
    
    
    
    
    
    
    
    
    
    
class CalculateAverageAccountLength(BaseEstimator, TransformerMixin):
    """
    A class to calculate a customer's average account age that can be used in an sklearn pipeline.

    ...

    Methods
    -------
    transform(X):
        Takes the input dataframe X and calculates the average account age of a customer.
    """
    def __init__(self):
        None
    # Trivial method to be compatible with Sklearn pipeline
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        """
        Calculates the average account age of a customer.


        Parameters
        ----------
        X : pd.DataFrame

        Returns
        -------
        df (pd.DataFrame): Pandas data frame with customer's average account age appended.
        """
        
        df = X.copy()
        
        average_acct_length = df['AVERAGE_ACCT_AGE'].str.split(' ', expand = True)

        
        months_average_acct_length = pd.Series(average_acct_length[1].str.extract('(\d+)')[0]).astype(int)
        years_average_acct_length = pd.Series(average_acct_length[0].str.extract('(\d+)')[0]).astype(int) * 12
        
        
        df['AVERAGE_ACCT_AGE'] = months_average_acct_length + years_average_acct_length

        return df