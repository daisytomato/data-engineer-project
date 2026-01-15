#!/usr/bin/env python
# coding: utf-8

# In[18]:


import pandas as pd
import requests
import io
from sqlalchemy import create_engine


# In[9]:


url= "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"
response = requests.get(url)


# In[12]:


print(f'status code: {response.status_code}') #check the status of data download 


# In[17]:


df = pd.read_csv(io.BytesIO(response.content))
df


# In[40]:


engine = create_engine('postgresql://postgres:postgres@localhost:5433/ny_taxi')


# In[41]:


engine.connect()


# In[42]:


df.to_sql('zone_lookup',con = engine,if_exists='replace', index=False)


# In[ ]:




