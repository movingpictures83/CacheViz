#!/usr/bin/env python
# coding: utf-8

# In[515]:


import numpy as np
import seaborn as sb
import pandas as pd
import matplotlib.pyplot as plt
import os.path as path
plt.style.use('seaborn-whitegrid')


# In[538]:

class CacheVizPlugin:
 def input(self, inputfile):

  self.data = pd.read_csv(inputfile)
 def run(self):
     pass
 def output(self, outputfile):
  self.data.columns = ['traces','Algorithms','cache_size','hit_rate']
  x = list(path.splitext(tr[-1])[0] for tr in self.data['traces'].str.split('/'))
  y = list(r[-1] for r in self.data['traces'].str.split('/'))
  ls=[]
  for i in y:
    if path.splitext(i)[-1] == '.blk':
        ls.append('VISA')
    if path.splitext(i)[-1] == '.blkparse':
        ls.append('FIU')
    if path.splitext(i)[-1]== '.csv':
        ls.append('MSR')
    if path.splitext(i)[-1]== '.txt':
        ls.append('NEXUS')

  self.data['self.dataset'] = ls
  #print(self.data)
  self.data['Datasets'] = list(zip(self.data['self.dataset'], self.data['cache_size']))
  self.data['workload'] = list(zip(x, self.data['cache_size']))
  self.data['algoritms_self.dataset'] = list(zip(self.data['Algorithms'], self.data['self.dataset']))

  self.data['cache_algorithm'] = list(zip(self.data['Algorithms'], self.data['cache_size']))

  #self.data['workload'] = list(zip(self.data['traces'], self.data['cache_size']))
  #self.data1 = self.data.drop(columns = ['traces','cache_size'])
  mean = self.data.groupby('cache_size').mean()
  self.data_mean_bytraces = self.data.groupby(['cache_size', 'Algorithms']).mean()
  self.data_sets = self.data.groupby(['self.dataset']).mean()
  self.data_mean_bydatasets = self.data.groupby(['self.dataset', 'Algorithms']).mean()
  self.data_mean_bydatasets_cachesize = self.data.groupby(['Datasets', 'Algorithms']).mean()


  # In[539]:


  heatmap_data = pd.pivot_table(self.data_mean_bytraces, values='hit_rate', 
                     index=['Algorithms'], 
                     columns='cache_size')
  #print(heatmap_data)
  plt.figure(figsize=(4, 4))
  heat_map = sb.heatmap(heatmap_data,cmap="coolwarm")
  plt.show()


  # In[540]:


  heatmap_traces = pd.pivot_table(self.data, values='hit_rate', 
                     index=['Algorithms'], 
                     columns='workload')
  #print(heatmap_data)
  plt.figure(figsize=(20, 2))
  heat_map = sb.heatmap(heatmap_traces,cmap="RdBu")
  plt.show()


  # In[541]:


  heatmap_data = pd.pivot_table(self.data_mean_bydatasets, values='hit_rate', 
                     index=['Algorithms'], 
                     columns='self.dataset')
  #print(heatmap_data)
  plt.figure(figsize=(4, 2))
  heat_map = sb.heatmap(heatmap_data,cmap="coolwarm")
  plt.show()


  # In[542]:


  heatmap_data = pd.pivot_table(self.data_mean_bydatasets_cachesize, values='hit_rate', 
                     index=['Algorithms'], 
                     columns='Datasets')
  #print(heatmap_data)
  plt.figure(figsize=(10, 2))
  heat_map = sb.heatmap(heatmap_data,cmap="coolwarm")
  plt.show()


  # In[543]:


  ##########TODO: Normalize by OPT!!!!######
  heatmap_data = pd.pivot_table(self.data_mean_bydatasets_cachesize, values='hit_rate', 
                     index=['Algorithms'], 
                     columns='Datasets')

  label = ["0.0005", "0.001", "0.005", "0.01", "0.05", "0.1","0.0005", "0.001", "0.005", "0.01", "0.05", "0.1","0.0005", "0.001", "0.005", "0.01", "0.05", "0.1","0.0005", "0.001", "0.005", "0.01", "0.05", "0.1"]
  top_label = ["FIU", "MSR", "Nexus", "VISA", ""]
  tick_l = [2.5, 7.5, 12.5, 17.5, 20]
  mid = (self.data_mean_bydatasets_cachesize['hit_rate'].max() - self.data_mean_bydatasets_cachesize['hit_rate'].min()) / 2

  fig, ax1 = plt.subplots(figsize=(10, 2))
  sb.set_style('white')
  ax1 = sb.heatmap(heatmap_data,cmap="RdYlGn", annot=True)

  ax2 = ax1.twiny()
  ax1.set_xticklabels(label)
  ax2.set_xticklabels(top_label)
  ax2.set_xticks(tick_l)

  ax1.set_xlabel("cache size(% of workload footprint)")
  fig.savefig(outputfile, format='eps', bbox_inches = 'tight')
  plt.show()


  # In[544]:


  heatmap_data = pd.pivot_table(self.data_mean_bydatasets_cachesize, values='hit_rate', 
                     index=['Algorithms'], 
                     columns='Datasets')
  #print(heatmap_data)
  mid = (self.data_mean_bydatasets_cachesize['hit_rate'].max() - self.data_mean_bydatasets_cachesize['hit_rate'].min()) / 2
  print(mid)
  plt.figure(figsize=(10, 2))
  #fig.set_size_inches(15, 10)
  heat_map = sb.heatmap(heatmap_data,cmap="RdYlGn", annot=True, center=mid, robust=True, square=True, vmin=1, vmax=42)
  plt.show()


  #   In[545]:


  fig, axes = plt.subplots()

  sb.violinplot(self.data['self.dataset'],self.data['hit_rate'], data = self.data, ax = axes)
  axes.set_title('Average Hit Rate')

  #print (self.data['self.dataset'].head(10))
  #print (self.data['hit_rate'].head(10))
  axes.yaxis.grid(True)
  axes.set_xlabel('self.dataset')
  axes.set_ylabel('Hit Rate')

  plt.show()


  # In[550]:


  fig, axes = plt.subplots()
 
  fig.set_size_inches(10, 4)
  sb.violinplot(self.data['Algorithms'], self.data['hit_rate'], data = self.data, ax = axes)
  axes.set_title('Average Hit Rate')

  axes.yaxis.grid(True)
  axes.set_xlabel('Algorithm')
  axes.set_ylabel('Hit Rate')

  plt.show()


  # In[551]:


  fig, axes = plt.subplots()

  fig.set_size_inches(30, 6)
  sb.violinplot(self.data['algoritms_self.dataset'], self.data['hit_rate'], data = self.data, ax = axes)
  axes.set_title('Average Hit Rate')

  #for i in self.data['hit_rate']:
  #    if i > 100:
  #        print (i)
  #print (self.data.head(10))
  #print (self.data['algorithms_self.dataset'])
  #print (self.data['hit_rate'].head(10))
  axes.yaxis.grid(True)
  axes.set_xlabel('Alg/Dataset')
  axes.set_ylabel('Hit Rate')

  plt.show()


  # In[552]:


  fig, axes = plt.subplots()
  self.data_lru = self.data['cache_size'] == 0.0005
  #print(self.data_lru)
  self.data_lru_hit_rate = self.data[self.data_lru]

  #print (self.data_lru_hit_rate)

  fig.set_size_inches(10, 4)
  sb.violinplot(self.data_lru_hit_rate['Algorithms'], self.data_lru_hit_rate['hit_rate'], data = self.data, ax = axes)
  axes.set_title('Average Hit Rate')
  axes.yaxis.grid(True)
  axes.set_xlabel('LRU/cache_size')
  axes.set_ylabel('Hit Rate')
  plt.show()


  # In[553]:


  fig, axes = plt.subplots()
  self.data_lru = self.data['cache_size'] == 0.001
  #print(self.data_lru)
  self.data_lru_hit_rate = self.data[self.data_lru]

  #print (self.data_lru_hit_rate)

  fig.set_size_inches(10, 4)
  sb.violinplot(self.data_lru_hit_rate['Algorithms'], self.data_lru_hit_rate['hit_rate'], data = self.data, ax = axes)
  axes.set_title('Average Hit Rate')
  axes.yaxis.grid(True)
  axes.set_xlabel('LRU/cache_size')
  axes.set_ylabel('Hit Rate')
  plt.show()


  # In[554]:


  fig, axes = plt.subplots()
  self.data_lru = self.data['cache_size'] == 0.005
  #print(self.data_lru)
  self.data_lru_hit_rate = self.data[self.data_lru]

  #print (self.data_lru_hit_rate)

  fig.set_size_inches(10, 4)
  sb.violinplot(self.data_lru_hit_rate['Algorithms'], self.data_lru_hit_rate['hit_rate'], data = self.data, ax = axes)
  axes.set_title('Average Hit Rate')
  axes.yaxis.grid(True)
  axes.set_xlabel('LRU/cache_size')
  axes.set_ylabel('Hit Rate')
  plt.show()


  # In[557]:


  fig, axes = plt.subplots()
  self.data_lru = self.data['cache_size'] == 0.01
  #print(self.data_lru)
  self.data_lru_hit_rate = self.data[self.data_lru]

  #print (self.data_lru_hit_rate)

  fig.set_size_inches(10, 4)
  sb.violinplot(self.data_lru_hit_rate['Algorithms'], self.data_lru_hit_rate['hit_rate'], data = self.data, ax = axes)
  axes.set_title('Average Hit Rate')
  axes.yaxis.grid(True)
  axes.set_xlabel('LRU/cache_size')
  axes.set_ylabel('Hit Rate')
  plt.show()


  # In[556]:


  fig, axes = plt.subplots()
  self.data_lru = self.data['cache_size'] == 0.05
  #print(self.data_lru)
  self.data_lru_hit_rate = self.data[self.data_lru]

  #print (self.data_lru_hit_rate)

  fig.set_size_inches(10, 4)
  sb.violinplot(self.data_lru_hit_rate['Algorithms'], self.data_lru_hit_rate['hit_rate'], data = self.data, ax = axes)
  axes.set_title('Average Hit Rate')
  axes.yaxis.grid(True)
  axes.set_xlabel('LRU/cache_size')
  axes.set_ylabel('Hit Rate')
  plt.show()


  # In[555]:


  fig, axes = plt.subplots()
  self.data_lru = self.data['cache_size'] == 0.1
  #print(self.data_lru)
  self.data_lru_hit_rate = self.data[self.data_lru]

  #print (self.data_lru_hit_rate)

  fig.set_size_inches(10, 4)
  sb.violinplot(self.data_lru_hit_rate['Algorithms'], self.data_lru_hit_rate['hit_rate'], data = self.data, ax = axes)
  axes.set_title('Average Hit Rate')
  axes.yaxis.grid(True)
  axes.set_xlabel('LRU/cache_size')
  axes.set_ylabel('Hit Rate')
  plt.show()


  # In[558]:


  fig, axes = plt.subplots()
  self.data_lfu = self.data['Algorithms'] == 'lfu'
  self.data_lfu_hit_rate = self.data[self.data_lfu]

  fig.set_size_inches(10, 4)
  sb.violinplot(self.data_lfu_hit_rate['cache_algorithm'], self.data_lfu_hit_rate['hit_rate'], data = self.data, ax = axes)
  axes.set_title('Average Hit Rate')
  axes.yaxis.grid(True)
  axes.set_xlabel('LFU/cache_size')
  axes.set_ylabel('Hit Rate')
  plt.show()


  # In[ ]:




