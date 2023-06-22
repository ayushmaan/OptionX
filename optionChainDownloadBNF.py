#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests
import pickle
import time
from datetime import datetime


# In[2]:


url="https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY"
headers={
    "accept-encoding":"gzip, deflate, br",
    "accept-language":"en-GB,en-US;q=0.9,en;q=0.8",
    "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}


# In[3]:
while True:

    session = requests.Session()
    data = session.get(url,headers=headers).json()["records"]["data"]
    # print(data)
    now = datetime.now() 
    filename= str(now).split(".")[0].replace(" ","_")+"bnf.pickle"


    # In[4]:


    dx = pd.DataFrame(data)


    # In[5]:


    oc_data = []
    for i in data:
        for j,k in i.items():
            if j=="CE" or j=="PE":
                info=k
                info["instrumentType"]=j
                oc_data.append(info)



    oc_df = pd.DataFrame(oc_data)


    unique_expiry_list = oc_df["expiryDate"].unique()



    oc_all_exp_data={}
    for exp in unique_expiry_list:
        ocex= oc_df[oc_df["expiryDate"]==exp]



        ocex = ocex[["strikePrice","lastPrice","openInterest","instrumentType"]]

        ocex = pd.merge(ocex[ocex["instrumentType"]=="CE"],ocex[ocex["instrumentType"]=="PE"],on="strikePrice")
        ocex.columns = ['strikePrice', 'CE_LTP', 'CE_OI', 'instrumentType_x',
               'PE_LTP', 'PE_OI', 'instrumentType_y']



        oc_dict = {}
        for stk in ocex.strikePrice:
            # print(stk)
            oc_dict[stk] = {"CE_LTP":ocex[ocex["strikePrice"]==stk]['CE_LTP'].values[0],
        "CE_OI":ocex[ocex["strikePrice"]==stk]['CE_OI'].values[0],
        "PE_LTP":ocex[ocex["strikePrice"]==stk]['PE_LTP'].values[0],
        "PE_OI":ocex[ocex["strikePrice"]==stk]['PE_OI'].values[0]}

        oc_all_exp_data[exp] = oc_dict



    with open("bnf_oc_data/"+filename, 'wb') as handle:
        pickle.dump(oc_all_exp_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    time.sleep(180)






# In[ ]:




