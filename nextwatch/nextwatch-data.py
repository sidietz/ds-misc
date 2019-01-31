
# coding: utf-8

# In[ ]:


import requests as rq
import re
from lxml import html
import json
from datetime import datetime
import csv


# In[ ]:


URL = "https://nextbike.net/maps/nextbike-live.json?city=158"


# In[ ]:


response = rq.get(URL)


# In[ ]:


nxt_json = json.loads(response.text)
ct = datetime.utcnow()


# In[ ]:


places = nxt_json['countries'][0]['cities'][0]['places']


# In[ ]:


len_p = len(places)


# In[ ]:


meta = nxt_json['countries'][0]['cities'][0]


# In[ ]:


# metaset = list(map(lambda x: [x['set_point_bikes'], ct], meta))


# In[ ]:


def bt2s(x):
    s = ""
    for a, b in x.items():
        s += str(a) + '-' + str(b)
        s += ';'
    return s


# In[ ]:


#meta


# In[ ]:


z = meta['bike_types']


# In[ ]:


#meta['bike_types']


# In[ ]:


bikemetaset = [meta['set_point_bikes'], len_p, bt2s(meta['bike_types']), ct]


# In[ ]:


#bikemetaset


# In[ ]:


#bikes = list(map(lambda x: [x['set_point_bikes'], x['name'], x['bikes'], ct], places))


# In[ ]:


#meta


# In[ ]:


# dataset = [[i, x['name'], x['bikes'], ct] for i,x in enumerate(places)]


# In[ ]:


dataset = list(map(lambda x: [x['number'], x['name'], x['bikes'], x['bike_racks'], x['free_racks'], x['terminal_type'], ct], places))


# In[ ]:


#dataset


# In[ ]:


def write_ds(dataset, name):
    with open(name + ".csv", 'a+') as f:
        writer = csv.writer(f)
        writer.writerows(dataset)


# In[ ]:


write_ds(dataset, "nb")
write_ds([bikemetaset], "bm")


# In[ ]:


#places[0]


# In[ ]:


#response.text

