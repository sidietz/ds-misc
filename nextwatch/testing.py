
# coding: utf-8

# In[121]:


import requests as rq
import pandas as pd
import re
from lxml import html
import json
from datetime import datetime
import csv


# In[122]:


URL = "https://nextbike.net/maps/nextbike-live.json?city=158"


# In[123]:


response = rq.get(URL)


# In[124]:


nxt_json = json.loads(response.text)
ct = datetime.utcnow()


# In[125]:


places = nxt_json['countries'][0]['cities'][0]['places']


# In[126]:


len_p = len(places)


# In[127]:


meta = nxt_json['countries'][0]['cities'][0]


# In[128]:


# metaset = list(map(lambda x: [x['set_point_bikes'], ct], meta))


# In[129]:


def bt2s(x):
    s = ""
    for a, b in x.items():
        s += str(a) + '-' + str(b)
        s += ';'
    return s


# In[130]:


#meta


# In[131]:


z = meta['bike_types']


# In[132]:


#meta['bike_types']


# In[133]:


bikemetaset = [meta['set_point_bikes'], len_p, bt2s(meta['bike_types']), ct]


# In[134]:


#bikemetaset


# In[135]:


#bikes = list(map(lambda x: [x['set_point_bikes'], x['name'], x['bikes'], ct], places))


# In[136]:


#meta


# In[137]:


# dataset = [[i, x['name'], x['bikes'], ct] for i,x in enumerate(places)]


# In[138]:


dataset = list(map(lambda x: [x['number'], x['name'], x['bikes'], x['bike_racks'], x['free_racks'], x['terminal_type'], ct], places))


# In[139]:


#dataset


# In[140]:


def write_ds(dataset, name):
    with open(name + ".csv", 'a+') as f:
        writer = csv.writer(f)
        writer.writerows(dataset)


# In[141]:


write_ds(dataset, "nb")
write_ds([bikemetaset], "bm")


# In[142]:


#places[0]


# In[143]:


#response.text

