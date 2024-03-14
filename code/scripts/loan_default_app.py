# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 18:30:37 2024

@author: H244746
"""

import os
os.chdir('C:\\Users\\H244746\\Desktop\\Deployment Exercise\\code\\scripts')


import streamlit as st
import pandas as pd
import pickle

from datetime import date


# Need to be able to import without changing directory
from feature_engineering_utils import *



st.cache(suppress_st_warning=True)








# cols = ['PERFORM_CNS_SCORE','NO_OF_INQUIRIES','PRI_OVERDUE_ACCTS','STATE_ID','LTV','EMPLOYMENT_TYPE',
#             'VOTERID_FLAG','DELINQUENT_ACCTS_IN_LAST_SIX_MONTHS','PRI_SANCTIONED_AMOUNT','MANUFACTURER_ID',
#             'DATE_OF_BIRTH', 'CREDIT_HISTORY_LENGTH', 'AVERAGE_ACCT_AGE']






# data_path = 'C:/Users/H244746/Desktop/Deployment Exercise/archive_original/train.csv'
# data = pd.read_csv(data_path)






def format_credit_history_length(date_of_first_loan):
    today = date.today()
    time_delta = pd.to_datetime(today) - pd.to_datetime(date_of_first_loan)
    days = time_delta / pd.Timedelta('1 day')
    
    years = int(days // 365)
    months = int((days % 365) // 30)
    
    cred_history_length_str = '{years}yrs {months}mon'.format(years = years, months = months)
    
    return cred_history_length_str



def format_average_account_age(average_loan_tenure_months):
    years = int(average_loan_tenure_months // 12)
    months = int(average_loan_tenure_months % 12)
    
    cred_history_length_str = '{years}yrs {months}mon'.format(years = years, months = months)
    
    return cred_history_length_str






        
        
app_mode = st.sidebar.selectbox('Select Page',['Data Description','Loan Default Prediction']) #two pages



if app_mode == 'Data Description':
        
    data_path = 'C:/Users/H244746/Desktop/Deployment Exercise/archive_original/Data Dictionary.xlsx'
    data_dict = pd.read_excel(data_path, sheet_name = 'Sheet2')
    
    st.subheader('Column name descriptions')
    st.write(data_dict)
    
    
    
    
    


elif app_mode == 'Loan Default Prediction':
    # st.image('slider-short-3.jpg')
    
    # Get input data from app
    st.subheader('Please specify the characteristics of the loan.')
    st.sidebar.header("Informations about the client :")
    DATE_OF_BIRTH = st.sidebar.date_input("When is the applicant's birthday?", min_value = date.fromisoformat('1940-01-01'), format = "DD-MM-YYYY")
    PERFORM_CNS_SCORE=st.sidebar.slider('Bureau score',0,1000,0,)
    NO_OF_INQUIRIES=st.sidebar.slider('Enquries done by customer for loan',0,36,0,)
    PRI_OVERDUE_ACCTS=st.sidebar.slider('Count of default accoutns',0,25,0)
    LTV=st.sidebar.slider('Loan to value of asset',0,100,0,)
    STATE_ID=st.sidebar.selectbox('State ID',tuple(list(range(1,26))))
    EMPLOYMENT_TYPE=st.sidebar.radio('Employment Type',('Salaried', 'Self employed'))
    VOTERID_FLAG=st.sidebar.radio('Was voter shared by customer? No = 0, Yes = 1',(0,1))
    DELINQUENT_ACCTS_IN_LAST_SIX_MONTHS=st.sidebar.slider('Number of delinquent accounts in the last six months',0,20,0,)
    PRI_SANCTIONED_AMOUNT=st.sidebar.slider('Sanctioned amount for all loans at time of disbursement',0,1000000000,0)
    MANUFACTURER_ID=st.sidebar.radio('Manufacturer ID', tuple([45,86,48,51,120,49,145,67,153,156,152]))
    CREDIT_HISTORY_LENGTH=st.sidebar.date_input('Date of first loan', min_value = date.fromisoformat('1940-01-01'))
    AVERAGE_ACCT_AGE = st.sidebar.slider('Average loan tenure in months',0,600,0)



    CREDIT_HISTORY_LENGTH = format_credit_history_length(CREDIT_HISTORY_LENGTH)
    AVERAGE_ACCT_AGE = format_average_account_age(AVERAGE_ACCT_AGE)
    
    
    # Convert date of birth to datetime
    DATE_OF_BIRTH = pd.to_datetime(DATE_OF_BIRTH)
    

    # Create dictionary with input data
    # Need to play with input format
    print('HERE I AM: ', pd.to_datetime(DATE_OF_BIRTH))
    data_from_app = {'PERFORM_CNS_SCORE': PERFORM_CNS_SCORE, 'NO_OF_INQUIRIES': NO_OF_INQUIRIES, 'PRI_OVERDUE_ACCTS': PRI_OVERDUE_ACCTS,
                     'STATE_ID': STATE_ID, 'LTV': LTV, 'EMPLOYMENT_TYPE': EMPLOYMENT_TYPE, 'VOTERID_FLAG': VOTERID_FLAG, 'DELINQUENT_ACCTS_IN_LAST_SIX_MONTHS': DELINQUENT_ACCTS_IN_LAST_SIX_MONTHS,
                     'PRI_SANCTIONED_AMOUNT': PRI_SANCTIONED_AMOUNT, 'MANUFACTURER_ID': MANUFACTURER_ID, 'DATE_OF_BIRTH': DATE_OF_BIRTH,
                     'CREDIT_HISTORY_LENGTH': CREDIT_HISTORY_LENGTH, 'AVERAGE_ACCT_AGE': AVERAGE_ACCT_AGE}
    
    
    
    # Load model pipeline
    pipeline_path = 'C:\\Users\\H244746\\Desktop\\Deployment Exercise\\models\\loan_default_pipeline_classifier.sav'
    with open(pipeline_path, 'rb') as handle:
        model = pickle.load(handle)
      
        
    # Generate prediction for input data
    data_from_app = pd.DataFrame(data_from_app, index = [0])
    prediction = model.predict(data_from_app)
    
    if st.button('Predict'):
        if prediction == 1 :
            st.error('According to the loan default prediction model, this loan is likely to default.')
        
        elif prediction == 0:
            st.success('According to the loan default prediction model, this loan is unlikely to default.')